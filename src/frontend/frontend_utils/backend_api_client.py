import requests
from utils.customlogger import CustomLogger
from typing import Dict, Any, Optional
from src.frontend.frontend_utils.constants import BASE_URL

# Setting up custom logger
logger = CustomLogger(name="BackendAPIClientLogger", log_file="backend_api_client.log").get_logger()


def get_patients() -> Dict[str, Dict[str, Any]]:
    """Fetch all patients from the backend API."""
    try:
        r = requests.get(f"{BASE_URL}/view")
        r.raise_for_status()
        logger.info(f"Fetched {len(r.json())} patients successfully")
        return r.json()
    except Exception as e:
        logger.error(f"API Error [get_patients]: {e}")
        return {}


def get_patient(patient_id: str) -> Optional[Dict[str, Any]]:
    """Fetch single patient by ID."""
    try:
        r = requests.get(f"{BASE_URL}/patient/{patient_id}")
        if r.status_code == 200:
            logger.info(f"Fetched patient {patient_id} successfully")
            return r.json()
        logger.warning(f"Patient {patient_id} not found (status {r.status_code})")
        return None
    except Exception as e:
        logger.error(f"API Error [get_patient]: {e}")
        return None


def create_patient(payload: Dict[str, Any]) -> bool:
    """Create a new patient."""
    try:
        r = requests.post(f"{BASE_URL}/create", json=payload)
        if r.status_code == 201:
            logger.info(f"Created patient {payload.get('patient_id')} successfully")
            return True
        logger.warning(f"Failed to create patient {payload.get('patient_id')} (status {r.status_code})")
        return False
    except Exception as e:
        logger.error(f"API Error [create_patient]: {e}")
        return False


def update_patient(patient_id: str, payload: Dict[str, Any]) -> bool:
    """Update an existing patient."""
    try:
        r = requests.put(f"{BASE_URL}/edit/{patient_id}", json=payload)
        if r.status_code == 200:
            logger.info(f"Updated patient {patient_id} successfully")
            return True
        logger.warning(f"Failed to update patient {patient_id} (status {r.status_code})")
        return False
    except Exception as e:
        logger.error(f"API Error [update_patient]: {e}")
        return False


def delete_patient(patient_id: str) -> bool:
    """Delete a patient by ID."""
    try:
        r = requests.delete(f"{BASE_URL}/delete/{patient_id}")
        if r.status_code == 200:
            logger.info(f"Deleted patient {patient_id} successfully")
            return True
        logger.warning(f"Failed to delete patient {patient_id} (status {r.status_code})")
        return False
    except Exception as e:
        logger.error(f"API Error [delete_patient]: {e}")
        return False


def sort_patients(sort_by: str, order: str = "asc") -> Dict[str, Dict[str, Any]]:
    """Sort patients by a given field (age, height, weight, bmi)."""
    try:
        r = requests.get(f"{BASE_URL}/sort", params={"sort_by": sort_by, "order": order})
        r.raise_for_status()
        logger.info(f"Sorted patients by '{sort_by}' in {order} order successfully")
        return r.json()
    except Exception as e:
        logger.error(f"API Error [sort_patients]: {e}")
        return {}
