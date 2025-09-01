from flet.core.border_radius import vertical
import flet as ft
from typing import Any, Dict
from collections import Counter
from src.frontend.components.navigation import Navigation
from src.frontend.frontend_utils.backend_api_client import get_patients


class HomePage:
    def __init__(self, page: ft.Page, nav: Navigation) -> None:
        self.page: ft.Page = page
        self.nav: Navigation = nav

    # -------------------------------
    # Main Page Content
    # -------------------------------
    def get_content(self, **kwargs: Dict[str, Any]) -> ft.Container:
        """Return the dashboard container with stats and charts."""

        # Fetch patient data from backend
        patients: Dict[str, Dict[str, Any]] = get_patients()

        # Aggregate stats
        total_patients: int = len(patients)
        verdict_counts: Counter = Counter(p["verdict"] for p in patients.values())
        gender_counts: Counter = Counter(p["gender"] for p in patients.values())
        city_counts: Counter = Counter(p["city"] for p in patients.values())

        # Layout: Stats cards row
        stats_row: ft.Row = ft.Row(
            controls=[
                self.create_stat_card(
                    "Total Patients", str(total_patients),
                    ft.Icons.PEOPLE, ft.Colors.BLUE
                ),
                self.create_stat_card(
                    "Obese Patients", str(verdict_counts.get("Obese", 0)),
                    ft.Icons.WARNING, ft.Colors.RED
                ),
                self.create_stat_card(
                    "Normal Patients", str(verdict_counts.get("Normal", 0)),
                    ft.Icons.CHECK_CIRCLE, ft.Colors.GREEN
                ),
                self.create_stat_card(
                    "Underweight Patients", str(verdict_counts.get("Underweight", 0)),
                    ft.Icons.FITNESS_CENTER, ft.Colors.ORANGE
                ),
                self.create_stat_card(
                    "Overweight Patients", str(verdict_counts.get("Overweight", 0)),
                    ft.Icons.FITNESS_CENTER, ft.Colors.PURPLE
                ),
            ],
            spacing=5,
            alignment=ft.MainAxisAlignment.SPACE_EVENLY
        )

        # Final page layout
        return ft.Container(
            content=ft.Column(
                controls=[
                    stats_row,
                    ft.Divider(height=20),
                    ft.Text("Quick Actions", size=20, weight=ft.FontWeight.BOLD),
                    self.quick_actions(),
                    ft.Divider(height=20),
                ],
                spacing=20,
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            expand=True,
            alignment=ft.alignment.center
        )

    # -------------------------------
    # Quick Actions
    # -------------------------------
    def quick_actions(self) -> ft.Column:
        """Return quick action buttons in two rows."""
        # First row of buttons
        button_row = ft.Row(
            controls=[
                ft.ElevatedButton(
                    "View All Patients",
                    icon=ft.Icons.LIST,
                    on_click=lambda e: self.nav.navigate_to("patients"),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE),
                ),
                ft.ElevatedButton(
                    "Add New Patient",
                    icon=ft.Icons.PERSON_ADD,
                    on_click=lambda e: self.nav.navigate_to("patient_form"),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE),
                ),
                ft.ElevatedButton(
                    "Delete Patient",
                    icon=ft.Icons.DELETE,
                    on_click=lambda e: self.nav.navigate_to("patients"),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.RED, color=ft.Colors.WHITE),
                ),
                ft.ElevatedButton(
                    "Edit Patient",
                    icon=ft.Icons.EDIT,
                    on_click=lambda e: self.nav.navigate_to("patients"),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.PURPLE, color=ft.Colors.WHITE),
                )
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        
        return ft.Column(
            controls=[button_row],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    # -------------------------------
    # Helpers
    # -------------------------------
    def create_stat_card(
        self, title: str, value: str, icon: str, color: str
    ) -> ft.Card:
        """Return a stat card with a title, value, and icon."""
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.ListTile(
                            leading=ft.Icon(icon, color=color, size=32),
                            title=ft.Text(value, size=24, weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(title),
                        )
                    ]
                ),
                padding=20,
                width=210,
                height=120,
            ),
            elevation=5,
        )

