"""
Modern navigation sidebar for a Flet-based YouTube downloader UI.

This module defines the ModernNavBar class to build a collapsible sidebar with
user information and navigation icons, and includes a layout function to render
the sidebar alongside a toggle button for visibility control.
"""
import time
from math import pi
import flet as ft

class ModernNavBar:
    """
    A modern sidebar navigation component for a Flet-based UI application.
    
    Provides a collapsible sidebar with user info and navigation items.
    """

    def __init__(self, func,page) -> None:
        """
        Initialize the ModernNavBar with a callback function to toggle sidebar visibility.

        Args:
            func (Callable): A function that will be triggered on icon/button interactions.
        """
        self.func = func
        self.page = page

    def user_data(self, initials: str, name: str, description: str) -> ft.Container:
        """
        Creates a container displaying the user's initials, name, and a short description.

        Args:
            initials (str): The user's initials to be shown inside a circle.
            name (str): The user's full name.
            description (str): A short user description or status.

        Returns:
            ft.Container: A container widget with the user's data.
        """
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        width=42, height=42,
                        alignment=ft.alignment.center,
                        border_radius=9,
                        content=ft.Text(value=initials, size=20, weight="bold")
                    ),
                    ft.Column(
                        spacing=1,
                        alignment="center",
                        controls=[
                            ft.Text(value=name, size=11,
                                    weight="bold", opacity=1,
                                    animate_opacity=200),
                            ft.Text(value=description, size=9, 
                                    weight="w400",
                                    opacity=1, animate_opacity=200),
                        ]
                    )
                ]
            )
        )

    def high_light(self, e) -> None:
        """
        Event handler to change the appearance of navigation items on hover.

        Args:
            e (ft.ControlEvent): The event triggered by hovering over a control.
        """
        if e.data == 'true':
            e.control.bgcolor = ft.Colors.PRIMARY_CONTAINER
        else:
            e.control.bgcolor = None
        e.control.update()
        e.control.content.update()

    def contained_icon(self, icon_name: str, text: str, link: str = None) -> ft.Container:
        """
        Creates a container with an icon and label that highlights on hover.

        Args:
            icon_name (str): The name of the icon to display.
            text (str): The label text displayed next to the icon.

        Returns:
            ft.Container: A clickable container with icon and label.
        """
        return ft.Container(
            width=180, height=45, border_radius=10,
            on_hover=self.high_light,
            on_click=lambda e, route=link: self.page.go(route) if route else None,
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=icon_name, icon_size=18, 
                        # icon_color="white54",
                        style=ft.ButtonStyle(
                            shape={"": ft.RoundedRectangleBorder(radius=7)},
                            overlay_color={"": "transparent"},
                        )
                    ),
                    ft.Text(value=text, 
                            # color="white54", 
                            size=12, opacity=1, animate_opacity=200),
                ],
            )
        )

    def build(self) -> ft.Column:
        """
        Builds the complete vertical navigation bar layout.

        Returns:
            ft.Column: A column widget containing user info and navigation buttons.
        """
        return ft.Column(
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment="center",
            controls=[
                self.user_data("YT", "YT-Downloader", "Easy use yt-downloader"),
                ft.Divider(height=5, color=ft.Colors.SECONDARY_CONTAINER),
                self.contained_icon(ft.Icons.DASHBOARD_ROUNDED, "Download", link="/download"),
                self.contained_icon(ft.Icons.BAR_CHART, "Statistics", link="/statistics"),
                self.contained_icon(ft.Icons.CHECKLIST, "List", link="/list"),
                ft.Divider(height=5, color=ft.Colors.SECONDARY_CONTAINER),
                self.contained_icon(ft.Icons.SETTINGS, "Setting", link="/settings"),
            ],
            expand=True
        )


def create_layout(page: ft.Page) -> ft.Row:
    """
    Creates a layout consisting of a collapsible sidebar and a toggle button.

    Returns:
        ft.Row: A horizontal row containing the sidebar and the toggle button.
    """
    sidebar = None

    def animate_sidebar(e) -> None:
        nonlocal sidebar, toggle_btn
        navbar_col = sidebar.content
        user_cont = navbar_col.controls[0]
        text_column = user_cont.content.controls[1]
        menu_items = navbar_col.controls[2:]

        if sidebar.width != 62:
            toggle_btn.rotate = ft.Rotate(angle=pi, alignment=ft.alignment.center)
            for txt in text_column.controls:
                txt.opacity = 0
                txt.update()
            for item in menu_items:
                if isinstance(item, ft.Container):
                    item.content.controls[1].opacity = 0
                    item.content.update()
            sidebar.width = 62
        else:
            toggle_btn.rotate = ft.Rotate(angle=0, alignment=ft.alignment.center)
            sidebar.width = 200
            sidebar.update()
            time.sleep(0.2)
            for txt in text_column.controls:
                txt.opacity = 1
                txt.update()
            for item in menu_items:
                if isinstance(item, ft.Container):
                    item.content.controls[1].opacity = 1
                    item.content.update()

        sidebar.update()
        toggle_btn.update()

    navbar = ModernNavBar(animate_sidebar, page).build()

    sidebar = ft.Container(
        width=200,
        border=ft.border.only(right=ft.border.BorderSide(1, ft.Colors.SECONDARY_CONTAINER)),
        animate=ft.animation.Animation(500, "decelerate"),
        alignment=ft.alignment.top_center,
        padding=10,
        content=navbar,
    )

    toggle_btn = ft.IconButton(
        icon=ft.Icons.ARROW_CIRCLE_LEFT_OUTLINED,
        icon_size=40,
        tooltip="Toggle Sidebar",
        animate_rotation=ft.animation.Animation(500, "decelerate"),
        on_click=animate_sidebar
    )

    return ft.Row(
        spacing=0,
        controls=[sidebar, toggle_btn],
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True
    )