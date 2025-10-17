"""
This module defines the view responsible for displaying the list
section of the application using Flet components.
"""

import flet as ft
from src.controls.list import List

def list_view(page: ft.Page) -> ft.Row:
    """
    Creates and returns the list view layout.

    Args:
        page (ft.Page): The current Flet page instance.

    Returns:
        ft.Row: A row containing the List component with defined layout settings.
    """
    return ft.Row(
        spacing=0,
        controls=[
            ft.Container(
                content=List(),
                margin=ft.margin.only(left=-40, top=60,right=40, bottom=40),
                expand=True,
            )
        ],
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True
    )
