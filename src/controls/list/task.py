import flet as ft

class Task:
    def __init__(self, task_name, quality, output_format, link,
                 task_status_change, task_delete, container,
                 db_id=None, completed=False, service=None):

        self.db_id = db_id
        self.completed = completed
        self.service = service

        self.task_name = task_name
        self.quality = quality
        self.output_format = output_format
        self.link = link
        self.task_status_change = task_status_change
        self.task_delete = task_delete
        self.container = container

        # Checkbox (zmienia status)
        self.checkbox = ft.Checkbox(value=self.completed, on_change=self.status_changed)

        # Text controls
        self.name_cell = ft.Text(self.task_name, size=16, weight=ft.FontWeight.BOLD, expand=True)
        self.link_cell = ft.Container(
            content=ft.Text(self.link),
            padding=ft.padding.only(left=8, bottom=5)
        )
        self.quality_cell = ft.Container(
            content=ft.Row(
                spacing=5,
                controls=[
                    ft.Icon(ft.icons.HIGH_QUALITY_OUTLINED, size=16),
                    ft.Text(f"Quality: {self.quality}", size=12)
                ]
            ),
            padding=ft.padding.only(left=7)
        )
        self.format_cell = ft.Container(
            content=ft.Row(
                spacing=5,
                controls=[
                    ft.Icon(ft.icons.FILE_PRESENT_OUTLINED, size=16),
                    ft.Text(f"Format: {self.output_format}", size=12)
                ]
            ),
        )

        # Action buttons
        self.edit_button = ft.IconButton(icon=ft.Icons.CREATE_OUTLINED, on_click=self.edit_clicked)
        self.delete_button = ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, on_click=self.delete_clicked)

        # Edit fields
        self.edit_name = ft.TextField(value=self.task_name, border_color=ft.Colors.SECONDARY_CONTAINER,
            focused_border_color=ft.Colors.PRIMARY, expand=True)
        self.edit_link = ft.TextField(value=self.link, border_color=ft.Colors.SECONDARY_CONTAINER,
            focused_border_color=ft.Colors.PRIMARY, expand=True)
        self.edit_quality = ft.Dropdown(
            value=self.quality,
            options=[ft.dropdown.Option(o) for o in ["The best", "1440p", "1080p", "720p", ">=480p"]],
            border_color=ft.Colors.SECONDARY_CONTAINER,
            focused_border_color=ft.Colors.PRIMARY
        )
        self.edit_format = ft.Dropdown(
            value=self.output_format,
            options=[ft.dropdown.Option(o) for o in ["Mkv", "Mp4"]],
            border_color=ft.Colors.SECONDARY_CONTAINER,
            focused_border_color=ft.Colors.PRIMARY
        )
        self.save_button = ft.IconButton(icon=ft.Icons.DONE_OUTLINE_OUTLINED, on_click=self.save_clicked)

        # Build rows
        self.display_row = self.build_display_row()
        self.edit_row = self.build_edit_row()

    def build_display_row(self):
        # checkbox jest widoczny tylko w Active
        checkbox_value = False
        self.checkbox.value = checkbox_value

        if self.completed:
            # Completed: brak checkboxa i przycisków akcji
            action_buttons = []
            display_checkbox = None
        else:
            # Active: checkbox + przyciski Edit i Delete
            action_buttons = [self.edit_button, self.delete_button]
            display_checkbox = self.checkbox

        return ft.Card(
            expand=True,
            content=ft.Container(
                padding=10,
                expand=True,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    spacing=5,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Row(spacing=10, controls=[c for c in [display_checkbox, self.name_cell] if c]),
                                ft.Row(spacing=0, controls=action_buttons),
                            ]
                        ),
                        self.link_cell,
                        ft.Row(spacing=20, controls=[self.quality_cell, self.format_cell]),
                    ]
                )
            )
        )




    def build_edit_row(self):
        return ft.Card(
            expand=True,
            content=ft.Container(
                padding=10,
                expand=True,
                content=ft.Row(
                    spacing=10,
                    controls=[self.edit_name, self.edit_link, self.edit_quality, self.edit_format, self.save_button]
                )
            )
        )

    def status_changed(self, e):
    # checkbox służy tylko do zaznaczania w Active
    # powiadamiamy List, aby zaktualizował licznik
        self.task_status_change(self)
        # self.completed = self.checkbox.value
        # if self.service and self.db_id:
        #     self.service.update_item(self.db_id, completed=self.completed)

        # # odśwież UI w List (przesuwa elementy między zakładkami)
        # self.task_status_change(self)

    def edit_clicked(self, e):
        idx = self.container.controls.index(self.display_row)
        self.container.controls[idx] = self.edit_row
        self.container.page.update()

    def save_clicked(self, e):
        # aktualizacja wartości
        self.task_name = self.edit_name.value
        self.link = self.edit_link.value
        self.quality = self.edit_quality.value
        self.output_format = self.edit_format.value

        # update DB
        if self.service and self.db_id:
            self.service.update_item(
                self.db_id,
                title=self.task_name,
                link=self.link,
                quality=self.quality,
                output_format=self.output_format
            )

        # update UI cells
        self.name_cell.value = self.task_name
        self.link_cell.content.value = self.link
        self.quality_cell.content.controls[1].value = f"Quality: {self.quality}"
        self.format_cell.content.controls[1].value = f"Format: {self.output_format}"

        # swap back row
        idx = self.container.controls.index(self.edit_row)
        self.container.controls[idx] = self.display_row  # <-- nie twórz nowego
        self.container.page.update()

        # informuj List, aby sprawdził filtr i counts
        self.task_status_change(self)

    def delete_clicked(self, e):
        # ustaw status completed = True w bazie
        self.completed = True

        # checkbox w Completed ma pozostać odznaczony
        self.checkbox.value = False

        if self.service and self.db_id:
            self.service.update_item(self.db_id, completed=True)

        # odbudowa display_row, aby przycisk kosza zniknął
        idx = self.container.controls.index(self.display_row)
        self.container.controls[idx] = self.build_display_row()
        self.display_row = self.container.controls[idx]

        # odśwież widok w List
        self.task_status_change(self)  # <- wywołuje apply_filter() i update_counts()

    def is_completed(self):
        return self.completed
