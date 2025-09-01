import requests
import flet as ft
from typing import Dict, Any, Optional
from src.frontend.components.navigation import Navigation
from src.frontend.frontend_utils.constants import BASE_URL
from src.frontend.frontend_utils.backend_api_client import get_patients


class PatientFormPage:
    def __init__(self, page: ft.Page, nav: Navigation) -> None:
        self.page: ft.Page = page
        self.nav: Navigation = nav

    def get_content(self, patient_id: Optional[str] = None, **kwargs: Dict[str, Any]) -> ft.Container:
        """Display patient form. If patient_id is provided → edit mode."""
        patient: Dict[str, Any] = {}
        if patient_id:
            patient = get_patients().get(patient_id, {})
        
        # Fixed width for form fields
        field_width = 400

        # Form fields
        name = ft.TextField(label="Name", value=patient.get("name", ""), width=field_width, border_radius=50)
        age = ft.TextField(label="Age", value=str(patient.get("age", "")), width=field_width, border_radius=50)
        gender = ft.Dropdown(
            label="Gender",
            options=[ft.dropdown.Option("male"), ft.dropdown.Option("female")],
            value=patient.get("gender", ""),
            width=field_width,
            border_radius=50
        )
        city = ft.TextField(label="City", value=patient.get("city", "") , width=field_width, border_radius=50, autocorrect=True)
        height = ft.TextField(label="Height (m)", value=str(patient.get("height", "")), width=field_width, border_radius=50)
        weight = ft.TextField(label="Weight (kg)", value=str(patient.get("weight", "")), width=field_width, border_radius=50)

        def save_patient(e: ft.ControlEvent) -> None:
            payload = {
                "patient_id": patient_id or f"P{len(get_patients())+1:03d}",
                "name": name.value,
                "age": int(age.value) if age.value and age.value.strip() else 0,
                "gender": gender.value,
                "city": city.value.title() if city.value else "",
                "height": float(height.value) if height.value and height.value.strip() else 0.0,
                "weight": float(weight.value) if weight.value and weight.value.strip() else 0.0,
            }

            try:
                if patient_id:  # Update
                    requests.put(f"{BASE_URL}/edit/{patient_id}", json=payload)
                    self.page.open(ft.SnackBar(ft.Text("Patient updated successfully")))
                else:  # Create
                    requests.post(f"{BASE_URL}/create", json=payload)
                    self.page.open(ft.SnackBar(ft.Text("Patient created successfully")))
            except Exception as err:
                self.page.open(ft.SnackBar(ft.Text(f"Error: {err}")))

            self.page.update()
            self.nav.navigate_to("patients")

        return ft.Container(
            content=ft.Card(
                        content=ft.Column(
                        controls=[
                            ft.Text("Patient Form", size=24, weight=ft.FontWeight.BOLD),
                            name, age, gender, city, height, weight,
                            ft.ElevatedButton("Save", on_click=save_patient),
                        ],
                        spacing=20,
                        expand=False,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        elevation=5,
                        shadow_color="grey",
                        width=500,
                        height=550
                    ),
            padding=20,
            expand=True,
            alignment=ft.alignment.center
        )
