from typing import Annotated, Literal, Optional
from pydantic import BaseModel, Field, computed_field


# ----------------------------------------
# Define Pydantic Model for Patient class
# ----------------------------------------
class Patient(BaseModel):
    patient_id: Annotated[str, Field(default=..., description="Unique identifier for the patient", examples=["P001"])]
    name: Annotated[str, Field(default=..., description="Full name of the patient", examples=["John Doe"])]
    city: Annotated[str, Field(default=..., description="City of residence", examples=["New York"])]
    age: Annotated[int, Field(default=..., gt=0, lt=120, description="Age of the patient", examples=[30])]
    gender: Annotated[Literal["male", "female", "others"], Field(default=..., description="Gender of the patient")]
    height: Annotated[float, Field(default=..., gt=0, description="Height in m of the patient", examples=[1.75])]
    weight: Annotated[float, Field(default=..., gt=0, description="Weight in kg of the patient", examples=[70.5])]

    @computed_field
    @property
    def bmi(self) -> float:
        """Calculate BMI from height and weight."""
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        """Determine health verdict based on BMI."""
        bmi_value = self.bmi
        if bmi_value < 18.5:
            return "Underweight"
        elif 18.5 <= bmi_value < 24.9:
            return "Normal"
        elif 25 <= bmi_value < 30:
            return "Overweight"
        else:
            return "Obese"


# ----------------------------------------------
# Define Pydantic Model for PatientUpdate class
# ----------------------------------------------
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None, description="Full name of the patient", examples=["John Doe"])]
    city: Annotated[Optional[str], Field(default=None, description="City of residence", examples=["New York"])]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=120, description="Age of the patient", examples=[30])]
    gender: Annotated[Optional[Literal["male", "female", "others"]], Field(default=None, description="Gender of the patient")]
    height: Annotated[Optional[float], Field(default=None, gt=0, description="Height in m of the patient", examples=[1.75])]
    weight: Annotated[Optional[float], Field(default=None, gt=0, description="Weight in kg of the patient", examples=[70.5])]