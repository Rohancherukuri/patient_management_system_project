import flet as ft
from typing import Optional

class Navigation:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.pages = {}
        self.current_page = ""

        # ✅ Set AppBar directly on the page (not inside layout)
        self.page.appbar = ft.AppBar(
            title=ft.Text("Patient Management System", size=24, weight=ft.FontWeight.BOLD),
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE,
            center_title=True,
        )

        # Navigation rail - Remove expand and let it use default sizing
        self.nav_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            height=500,  # ✅ Set explicit height on NavigationRail itself
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.HOME_OUTLINED,
                    selected_icon=ft.Icons.HOME,
                    label="Home",
                ),
                # ft.NavigationRailDestination(
                #     icon=ft.Icons.PEOPLE_OUTLINED,
                #     selected_icon=ft.Icons.PEOPLE,
                #     label="Patients",
                # ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.INFO_OUTLINED,
                    selected_icon=ft.Icons.INFO,
                    label="About",
                ),
            ],
            on_change=self.navigate_rail,
        )

        # Content area (main page body that changes on navigation)
        self.content = ft.Column(
            controls=[ft.Text("Loading...")],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        # Simple layout without nested containers
        self.layout = ft.Row(
            controls=[
                self.nav_rail,  # ✅ Add NavigationRail directly to Row
                ft.VerticalDivider(width=1),
                ft.Container(
                    content=self.content,
                    expand=True,      # make main content fill remaining space
                )
            ],
            expand=True,
        )


    def add_page(self, name: str, page: ft.Page) -> None:
        self.pages[name] = page

    def navigate_to(self, page_name: str, patient_id: str = "", **kwargs: Optional[dict]) -> None:
        if page_name in self.pages:
            self.current_page = page_name
            page_content = self.pages[page_name].get_content(**kwargs)
            self.content.controls = [page_content]

            # Update navigation rail selection
            if page_name == "home":
                self.nav_rail.selected_index = 0
            # elif page_name == "patients":
            #     self.nav_rail.selected_index = 1
            elif page_name == "about":
                self.nav_rail.selected_index = 1
            else:
                self.nav_rail.selected_index = None

            self.page.update()

    def navigate_rail(self, e: ft.ControlEvent) -> None:
        index = e.control.selected_index
        if index == 0:
            self.navigate_to("home")
        # elif index == 1:
        #     self.navigate_to("patients")
        elif index == 1:
            self.navigate_to("about")

    def new_patient(self, e: ft.ControlEvent) -> None:
        self.navigate_to("patient_form")

    def view_patient(self, patient_id: str) -> None:
        self.navigate_to("patient_detail", patient_id=patient_id)

    def edit_patient(self, patient_id: str) -> None:
        self.navigate_to("patient_form", patient_id=patient_id)

    # ✅ Now only return layout (not AppBar)
    def get_content(self) -> ft.Row:
        return self.layout