import flet as ft

def statistics_view(page: ft.Page) -> ft.Row:
    return ft.Row(
        spacing=0,
        controls=[
            ft.Container(
                content=ft.Text("Statistics View", size=20, weight="bold"),
                margin=ft.margin.only(left=-40),
                expand=True,
            ),
        ],
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True
    )
