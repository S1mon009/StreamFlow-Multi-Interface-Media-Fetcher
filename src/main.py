'''
Main application entry point for the YouTube Downloader UI built with Flet.

This module initializes the Flet app window and renders the sidebar layout.
'''
import flet as ft
from views import route_change

def main(page: ft.Page) -> None:
    """
    Entry point for the Flet GUI application.

    Initializes and configures the main application layout and components,
    and renders them to the provided Flet page.
    
    Args:
        page (Page): The Flet page object used to render the UI.
    """
    def on_route_change(e) -> None:
        route_change(e, page)

    page.title = "YT Downloader"
    page.horizontal_alignment = "start"
    page.vertical_alignment = "start"
    page.padding = 0
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE_GREY_900)
    page.on_route_change = on_route_change
    page.go("/download")