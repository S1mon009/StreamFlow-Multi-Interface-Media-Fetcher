import flet as ft
from src.controls.list import List

def list_view(page: ft.Page) -> ft.Row:
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
