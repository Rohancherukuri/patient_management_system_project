import requests
import flet as ft
from typing import Dict, Any
from src.frontend.components.navigation import Navigation
from src.frontend.frontend_utils.constants import BASE_URL
from src.frontend.frontend_utils.backend_api_client import get_patients


class PatientDetailPage:
    def __init__(self, page: ft.Page, nav: Navigation) -> None:
        self.page: ft.Page = page
        self.nav: Navigation = nav

    def get_content(self, patient_id: str, **kwargs: Dict[str, Any]) -> ft.Container:
        """Show details of a single patient."""
        patient: Dict[str, Any] = get_patients().get(patient_id, {})

        if not patient:
            return ft.Container(
                content=ft.Text("Patient not found", size=20, color=ft.Colors.RED),
                padding=20,
                expand=True,
            )

        def delete_patient(e: ft.ControlEvent) -> None:
            try:
                requests.delete(f"{BASE_URL}/delete/{patient_id}")
                self.page.open(ft.SnackBar(ft.Text("Patient deleted successfully")))
                self.nav.navigate_to("patients")
            except Exception as err:
                self.page.open(ft.SnackBar(ft.Text(f"Error: {err}")))
            self.page.update()

        details = ft.Column(
            controls=[
                ft.Text(f"Patient ID: {patient_id}", size=20, weight=ft.FontWeight.BOLD),
                ft.Text(f"Name: {patient['name']}"),
                ft.Text(f"Age: {patient['age']}"),
                ft.Text(f"Gender: {patient['gender']}"),
                ft.Text(f"City: {patient['city']}"),
                ft.Text(f"Height: {patient['height']} m"),
                ft.Text(f"Weight: {patient['weight']} kg"),
                ft.Text(f"BMI: {patient['bmi']}"),
                ft.Text(f"Verdict: {patient['verdict']}"),
                ft.Row(
                    controls=[
                        ft.ElevatedButton("Edit", on_click=lambda e: self.nav.navigate_to("patient_form", patient_id=patient_id)),
                        ft.ElevatedButton("Delete", on_click=delete_patient, bgcolor=ft.Colors.RED, color=ft.Colors.WHITE),
                    ]
                )
            ],
            spacing=10,
        )

        return ft.Container(content=details, padding=20, expand=True)
