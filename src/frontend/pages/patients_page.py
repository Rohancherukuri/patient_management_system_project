import flet as ft
from typing import Dict, Any
from src.frontend.components.navigation import Navigation
from src.frontend.frontend_utils.backend_api_client import (
    get_patients, update_patient, delete_patient
)


class PatientsPage:
    def __init__(self, page: ft.Page, nav: Navigation) -> None:
        self.page: ft.Page = page
        self.nav: Navigation = nav
        self.table: ft.DataTable = ft.DataTable(rows=[], columns=[])
        self.patients: Dict[str, Dict[str, Any]] = {}

    def get_content(self, **kwargs: Dict[str, Any]) -> ft.Container:
        """Display a table of all patients with edit/delete actions."""
        self.load_patients()
        self.table = self.build_table()

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Patients List", size=24, weight=ft.FontWeight.BOLD),
                    self.table,
                ],
                spacing=20,
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=20,
            expand=True,
            alignment=ft.alignment.center,
        )

    # -------------------------
    # Helpers
    # -------------------------
    def load_patients(self) -> None:
        """Fetch patients from backend."""
        self.patients = get_patients()

    def build_table(self) -> ft.DataTable:
        """Build patients table."""

        def make_view_handler(pid: str):
            return lambda e: self.view_patient(pid)

        def make_edit_handler(pid: str):
            return lambda e: self.confirm_edit(pid)

        def make_delete_handler(pid: str):
            return lambda e: self.confirm_delete(pid)

        rows = []
        for pid, pdata in self.patients.items():
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(pid)),
                        ft.DataCell(ft.Text(pdata.get("name", ""))),
                        ft.DataCell(ft.Text(str(pdata.get("age", "")))),
                        ft.DataCell(ft.Text(pdata.get("gender", ""))),
                        ft.DataCell(ft.Text(pdata.get("city", ""))),
                        ft.DataCell(ft.Text(str(pdata.get("bmi", "")))),
                        ft.DataCell(ft.Text(pdata.get("verdict", ""))),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        tooltip="Edit",
                                        on_click=make_edit_handler(pid),
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        tooltip="Delete",
                                        icon_color=ft.Colors.RED,
                                        on_click=make_delete_handler(pid),
                                    ),
                                ]
                            )
                        ),
                    ]
                )
            )

        return ft.DataTable(
            border=ft.border.all(1, ft.Colors.BLACK12),
            border_radius=10,
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=ft.Colors.BLACK12,
            data_row_color={ft.ControlState.HOVERED: "0x30FF0000"},
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Age")),
                ft.DataColumn(ft.Text("Gender")),
                ft.DataColumn(ft.Text("City")),
                ft.DataColumn(ft.Text("BMI")),
                ft.DataColumn(ft.Text("Verdict")),
                ft.DataColumn(ft.Text("Actions")),
            ],
            rows=rows,
        )

    # -------------------------
    # Actions
    # -------------------------
    def view_patient(self, patient_id: str):
        self.nav.navigate_to("patient_detail", patient_id=patient_id)

    def confirm_edit(self, patient_id: str) -> None:
        """Open dialog to update patient details inline."""
        patient = self.patients.get(patient_id, {})

        # Fields to edit
        name_field = ft.TextField(label="Name", value=patient.get("name", ""))
        age_field = ft.TextField(label="Age", value=str(patient.get("age", "")))
        gender_field = ft.Dropdown(label="Gender", options=[ft.dropdown.Option("male"), ft.dropdown.Option("female")],
            value=patient.get("gender", ""))
        city_field = ft.TextField(label="City", value=patient.get("city", ""))
        verdict_field = ft.TextField(label="Verdict", value=patient.get("verdict", ""))

        def save_changes(e):
            payload = {
                "name": name_field.value,
                "age": int(str(age_field.value)) if str(age_field.value).isdigit() else patient.get("age", 0),
                "gender": gender_field.value.lower() if gender_field.value else "",
                "city": city_field.value.title() if city_field.value else "",
                "verdict": verdict_field.value,
            }
            success = update_patient(patient_id, payload)
            self.page.close(dialog)

            if success:
                self.page.open(ft.SnackBar(ft.Text(f"Updated patient {patient_id}")))
                self.load_patients()
                self.table.rows = self.build_table().rows
            else:
                self.page.open(ft.SnackBar(ft.Text("Update failed"), bgcolor=ft.Colors.RED))

            self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Edit Patient {patient_id}"),
            content=ft.Column(
                [name_field, age_field, gender_field, city_field, verdict_field],
                tight=True,
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self.page.close(dialog)),
                ft.TextButton("Save", on_click=save_changes),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.open(dialog)
        self.page.update()

    def confirm_delete(self, patient_id: str) -> None:
        """Ask user confirmation before deleting."""
        def on_delete_click(e):
            self.perform_delete(dialog, patient_id)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirm Delete"),
            content=ft.Text(f"Are you sure you want to delete patient {patient_id}?"),
            actions=[
                ft.TextButton("Cancel", on_click=lambda e: self.page.close(dialog)),
                ft.TextButton(
                    "Delete",
                    style=ft.ButtonStyle(color=ft.Colors.RED),
                    on_click=on_delete_click,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.open(dialog)
        self.page.update()

    def perform_delete(self, dialog: ft.AlertDialog, patient_id: str) -> None:
        """Execute delete and refresh UI."""
        success = delete_patient(patient_id)
        self.page.close(dialog)

        if success:
            self.page.open(ft.SnackBar(ft.Text(f"Deleted patient {patient_id}")))
            self.load_patients()
            self.table.rows = self.build_table().rows
        else:
            self.page.open(
                ft.SnackBar(
                    ft.Text(f"Failed to delete patient {patient_id}"),
                    bgcolor=ft.Colors.RED,
                )
            )

        self.page.update()
