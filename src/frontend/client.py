import flet as ft
from flet import app
from typing import Dict, Any
from utils.customlogger import CustomLogger
from src.frontend.components.navigation import Navigation

# Pages
from src.frontend.pages.home_page import HomePage
from src.frontend.pages.about_page import AboutPage
from src.frontend.pages.patients_page import PatientsPage
from src.frontend.pages.patient_form_page import PatientFormPage
from src.frontend.pages.patient_detail_page import PatientDetailPage
from src.frontend.frontend_utils.constants import BASE_URL


# Setting up custom logger
logger = CustomLogger(name="AppLogger", log_file="app.log").get_logger()

def main(page: ft.Page) -> None:
    """Initialize the Patient Management System frontend."""

    # -------------------------------
    # Page Config
    # -------------------------------
    page.title = "Patient Management System"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 800
    page.window.min_height = 600
    page.scroll = ft.ScrollMode.AUTO

    # -------------------------------
    # Navigation
    # -------------------------------
    nav: Navigation = Navigation(page)

    # -------------------------------
    # Pages Registration
    # -------------------------------
    pages: Dict[str, Any] = {
        "home": HomePage(page, nav),
        "about": AboutPage(page, nav),
        "patients": PatientsPage(page, nav),
        "patient_form": PatientFormPage(page, nav),
        "patient_detail": PatientDetailPage(page, nav),
    }

    for name, flet_page in pages.items():
        nav.add_page(name=name, page=flet_page)

    # -------------------------------
    # Set initial page
    # -------------------------------
    nav.navigate_to(page_name="home")

    # -------------------------------
    # Add Navigation to Page
    # -------------------------------
    page.add(nav.get_content())

def run_app() -> None:
    """Run the Patient Management System frontend application."""
    try:
        logger.info("Starting the Patient Management System frontend application!")
        logger.info(f"Frontend will connect to backend at: {BASE_URL}")
        app(
            target=main, 
            name="Patients Mangement System", 
            view=ft.AppView.WEB_BROWSER, 
            assets_dir="frontend/assets",
            port=8080
        )
    except Exception as e:
        logger.error(f"Error running the app: {e}")

if __name__ == "__main__":
    run_app()
    

