"""
This module handles routing in the Flet application.

Based on the current `page.route`, it generates the appropriate view
and adds it to `page.views`, combining the selected view with the sidebar layout.
"""
import flet as ft
from src.controls.sidebar import create_layout
from src.views import download_view
from src.views import list_view
from src.views import settings_view
from src.views import statistics_view

def route_change(e: ft.RouteChangeEvent, page: ft.Page):
    """
    Handles route changes in the Flet application.

    Depending on the value of `page.route`, renders the appropriate view
    (e.g., download, list, settings, statistics) and updates `page.views`.

    Args:
        e (ft.RouteChangeEvent): The event object representing the route change.
        page (ft.Page): The main Flet page where views are managed and rendered.
    """
    page.views.clear()
    sidebar_row = create_layout(page)
    view = None

    if page.route == "/download":
        controls = [*sidebar_row.controls, download_view(page)]
        route_name = "/download"
    elif page.route == "/list":
        controls = [*sidebar_row.controls, list_view(page)]
        route_name = "/list"
    elif page.route == "/settings":
        controls = [*sidebar_row.controls, settings_view(page)]
        route_name = "/settings"
    elif page.route == "/statistics":
        controls = [*sidebar_row.controls, statistics_view(page)]
        route_name = "/statistics"
    else:
        controls = [*sidebar_row.controls]
        route_name = page.route

    view_row = ft.Row(
        spacing=0,
        controls=controls,
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True
    )

    view = ft.View(route_name, [view_row], padding=0)
    page.views.append(view)
    page.update()
