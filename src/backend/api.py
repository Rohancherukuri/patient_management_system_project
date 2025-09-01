import json
import asyncio
import pandas as pd
from typing import Any
from pathlib import Path
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from utils.customlogger import CustomLogger
from fastapi import FastAPI, HTTPException
from src.backend.database import SurrealDataBase
from concurrent.futures import ThreadPoolExecutor
from src.backend.orm import Patient, PatientUpdate


# Setting up custom logger
logger = CustomLogger(name="APIClientLogger", log_file="apiclient.log").get_logger()


class APIClient:
    def __init__(self, app: FastAPI, data_file: str | None=None) -> None:
        self.app = app

        # Resolve data_file relative to project root
        ROOT_DIR = Path(__file__).resolve().parents[2]
        self.data_file: Path = Path(data_file) if data_file else ROOT_DIR / "data" / "patients.json"

        self.executor: ThreadPoolExecutor = ThreadPoolExecutor(max_workers=1)
        self.register_routes()
        logger.info(f"APIClient initialized. Using data file at {self.data_file}")

    # ---- Helpers ----
    def load_data(self) -> pd.DataFrame:
        """Load patients data from JSON file into DataFrame."""
        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                content = json.load(file)
            logger.info("Patient data loaded successfully.")
            return pd.DataFrame.from_dict(content, orient="index")
        except FileNotFoundError:
            logger.error(f"Data file not found: {self.data_file}")
            raise HTTPException(status_code=404, detail="Data file not found")
        except Exception as e:
            logger.error(f"Unexpected error loading data: {e}")
            raise HTTPException(status_code=500, detail="Failed to load data")

    def save_data_to_json(self, data: pd.DataFrame) -> None:
        """Save DataFrame back to JSON file."""
        try:
            data.to_json(self.data_file, orient="index", indent=4)
            logger.info("Data successfully saved to JSON.")
        except Exception as e:
            logger.error(f"Error saving to JSON: {e}")
            raise HTTPException(status_code=500, detail="Failed to save data")

    async def save_data_to_db_async(self, data: pd.DataFrame) -> None:
        """Async method to save data to SurrealDB."""
        patients_dict: dict[str, dict[str, Any]] = data.to_dict(orient="index")
        db = SurrealDataBase()
        try:
            await db.use_connection()
            await db.import_patients(patients_dict)
            await db.close_connection()
            logger.info("Data successfully saved to SurrealDB.")
        except Exception as e:
            logger.error(f"Error saving to SurrealDB: {e}")

    def save_data_to_db(self, data: pd.DataFrame) -> None:
        """Non-blocking DB save using thread pool."""
        self.executor.submit(lambda: asyncio.run(self.save_data_to_db_async(data)))

    def persist(self, data: pd.DataFrame) -> None:
        """Save to JSON and DB."""
        self.save_data_to_json(data)
        self.save_data_to_db(data)

    # ---- Routes ----
    def register_routes(self) -> None:
        @self.app.get("/")
        def home_page() -> JSONResponse:
            return JSONResponse(status_code=200, content={"message": "Patient Management System API"})

        @self.app.get("/about")
        def about_page() -> JSONResponse:
            return JSONResponse(status_code=200, content={"message": "A fully functional Patient Management System API"})

        @self.app.get("/view")
        def get_patients_data() -> JSONResponse:
            data = self.load_data()
            return JSONResponse(status_code=200, content=data.to_dict(orient="index"))

        @self.app.get("/patient/{patient_id}")
        def get_patients_by_id(patient_id: str) -> JSONResponse:
            data = self.load_data()
            if patient_id in data.index:
                logger.info(f"Patient fetched: {patient_id}")
                return JSONResponse(status_code=200, content=data.loc[patient_id].to_dict())
            else:
                logger.warning(f"Patient not found: {patient_id}")
                raise HTTPException(status_code=404, detail="Patient not found")

        @self.app.get("/sort")
        def sort_patients(sort_by: str, order: str = "asc") -> JSONResponse:
            valid_fields = ["height", "weight", "bmi", "age"]
            if sort_by not in valid_fields:
                logger.warning(f"Invalid sort attempt: {sort_by}")
                raise HTTPException(status_code=400, detail=f"Invalid sort column, select from {valid_fields}")
            if order not in ["asc", "desc"]:
                raise HTTPException(status_code=400, detail="Order must be 'asc' or 'desc'")

            data = self.load_data()
            ascending = order == "asc"
            sorted_data = data.sort_values(by=sort_by, ascending=ascending)
            logger.info(f"Patients sorted by {sort_by} ({order}).")
            return JSONResponse(status_code=200, content=sorted_data.to_dict(orient="index"))

        @self.app.post("/create")
        def create_patient(patient: Patient) -> JSONResponse:
            data = self.load_data()
            if patient.patient_id in data.index:
                logger.warning(f"Create failed: Patient ID already exists ({patient.patient_id})")
                raise HTTPException(status_code=400, detail="Patient ID already exists")
            data.loc[patient.patient_id] = patient.model_dump(exclude=["patient_id"])
            self.persist(data)
            logger.info(f"Patient created: {patient.patient_id}")
            return JSONResponse(status_code=201, content={"message": "Patient created successfully", "patient": patient.model_dump()})

        @self.app.put("/edit/{patient_id}")
        def update_patient(patient_id: str, patient_update: PatientUpdate) -> JSONResponse:
            data = self.load_data()
            if patient_id not in data.index:
                logger.warning(f"Update failed: Patient not found ({patient_id})")
                raise HTTPException(status_code=404, detail="Patient not found")

            existing_patient_info = data.loc[patient_id].to_dict()
            update_patient_info = patient_update.model_dump(exclude_unset=True)
            existing_patient_info.update(update_patient_info)
            existing_patient_info["patient_id"] = patient_id

            try:
                validated = Patient(**existing_patient_info)
                data.loc[patient_id] = validated.model_dump(exclude=["patient_id"])
                self.persist(data)
                logger.info(f"Patient updated: {patient_id}")
                return JSONResponse(status_code=200, content={"message": "Patient updated successfully", "patient": validated.model_dump()})
            except ValidationError as e:
                logger.error(f"Validation error while updating {patient_id}: {e}")
                raise HTTPException(status_code=400, detail=f"Validation error: {e}")

        @self.app.delete("/delete/{patient_id}")
        def delete_patient(patient_id: str) -> JSONResponse:
            data = self.load_data()
            if patient_id in data.index:
                data = data.drop(index=patient_id)
                self.persist(data)
                logger.info(f"Patient deleted: {patient_id}")
                return JSONResponse(status_code=200, content={"message": "Patient deleted successfully", "patient_id": patient_id})
            else:
                logger.warning(f"Delete failed: Patient not found ({patient_id})")
                raise HTTPException(status_code=404, detail="Patient not found")

    def shutdown(self) -> None:
        """Cleanup method to shutdown the thread pool."""
        logger.info("Shutting down APIClient executor...")
        self.executor.shutdown(wait=False)
