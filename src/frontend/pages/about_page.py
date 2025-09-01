import flet as ft
from typing import Optional
from datetime import datetime
from src.frontend.components.navigation import Navigation

class AboutPage:
    def __init__(self, page: ft.Page, nav: Navigation) -> None:
        self.page = page
        self.nav = nav
    
    def get_content(self, **kwargs: Optional[dict]) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.ListTile(
                                        leading=ft.Icon(ft.Icons.MEDICAL_SERVICES, color=ft.Colors.BLUE, size=48),
                                        title=ft.Text("Comprehensive Patient Care", size=20, weight=ft.FontWeight.BOLD),
                                        subtitle=ft.Text("A complete solution for managing patient records, appointments, and medical history."),
                                    ),
                                    ft.Divider(),
                                    ft.ListTile(
                                        title=ft.Text("Features", size=18, weight=ft.FontWeight.BOLD),
                                        subtitle=ft.Text("""
• Patient Registration and Management
• Medical Records Management
• Reports and Analytics
"""),
                                    ),
                                    ft.Divider(),
                                    ft.ListTile(
                                        title=ft.Text("Technology Stack", size=18, weight=ft.FontWeight.BOLD),
                                        subtitle=ft.Text("""
• Backend: Python with FastAPI
• Frontend: Flet Framework
• Database: SurrealDB
• UI: Modern Responsive Design
• Platform: Browser-Platform (WEB)
"""),
                                    ),
                                    ft.Divider(),
                                    ft.ListTile(
                                        title=ft.Text("Version Information", size=18, weight=ft.FontWeight.BOLD),
                                        subtitle=ft.Text(f"""
Version: 1.0.0
Developed by: Rohan Cherukuri
Last Updated: {datetime.now().strftime('%Y-%m-%d')}
"""),
                                    ),
                                ]
                            ),
                            padding=20,
                        ),
                        elevation=5,
                    ),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                "Contact Support",
                                icon=ft.Icons.SUPPORT_AGENT,
                                on_click=self.contact_support,
                                style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)
                            )
                        ],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                spacing=20,
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            expand=True,
        )
    
    def contact_support(self, e: ft.ControlEvent) -> None:
        self.page.open(ft.SnackBar(ft.Text("Contact Support: rohan@accurkardia.com")))
        self.page.update()
    