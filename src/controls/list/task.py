import flet as ft

class Task:
    def __init__(self, task_name, quality, output_format, link, task_status_change, task_delete, container):
        self.completed = False
        self.task_name = task_name
        self.quality = quality
        self.output_format = output_format
        self.link = link
        self.task_status_change = task_status_change
        self.task_delete = task_delete
        self.container = container

        # Checkbox control
        self.checkbox = ft.Checkbox(value=False, on_change=self.status_changed)
        # Text controls
        self.name_cell = ft.Text(self.task_name, expand=True)
        self.link_cell = ft.Text(self.link, selectable=True)
        self.quality_cell = ft.Text(self.quality)
        self.format_cell = ft.Text(self.output_format)
        # Action buttons
        self.edit_button = ft.IconButton(icon=ft.Icons.CREATE_OUTLINED, on_click=self.edit_clicked)
        self.delete_button = ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, on_click=self.delete_clicked)

        # Edit fields
        self.edit_name = ft.TextField(value=self.task_name, expand=True)
        self.edit_link = ft.TextField(value=self.link, expand=True)
        self.edit_quality = ft.Dropdown(
            value=self.quality,
            options=[ft.dropdown.Option(o) for o in ["The best","1440p","1080p","720p",">=480p"]]
        )
        self.edit_format = ft.Dropdown(
            value=self.output_format,
            options=[ft.dropdown.Option(o) for o in ["Mkv","Mp4"]]
        )
        self.save_button = ft.IconButton(icon=ft.Icons.DONE_OUTLINE_OUTLINED, on_click=self.save_clicked)

        # Build rows
        self.display_row = self.build_display_row()
        self.edit_row = self.build_edit_row()

    def build_display_row(self):
        return ft.Row(
            spacing=10,
            controls=[
                self.checkbox,
                self.name_cell,
                self.link_cell,
                self.quality_cell,
                self.format_cell,
                ft.Row(controls=[self.edit_button, self.delete_button])
            ]
        )

    def build_edit_row(self):
        return ft.Row(
            spacing=10,
            controls=[
                ft.Text(""),
                self.edit_name,
                self.edit_link,
                self.edit_quality,
                self.edit_format,
                self.save_button
            ]
        )

    def status_changed(self, e):
        self.completed = self.checkbox.value
        self.task_status_change(self)

    def edit_clicked(self, e):
        idx = self.container.controls.index(self.display_row)
        self.container.controls[idx] = self.edit_row
        self.container.page.update()

    def save_clicked(self, e):
        # save edits
        self.task_name = self.edit_name.value
        self.link = self.edit_link.value
        self.quality = self.edit_quality.value
        self.output_format = self.edit_format.value
        # update cells
        self.name_cell.value = self.task_name
        self.link_cell.value = self.link
        self.quality_cell.value = self.quality
        self.format_cell.value = self.output_format
        # swap back row
        idx = self.container.controls.index(self.edit_row)
        self.container.controls[idx] = self.build_display_row()
        # refresh references
        self.display_row = self.container.controls[idx]
        self.container.page.update()

    def delete_clicked(self, e):
        # remove from container
        self.container.controls.remove(self.display_row)
        self.task_delete(self)
        self.container.page.update()