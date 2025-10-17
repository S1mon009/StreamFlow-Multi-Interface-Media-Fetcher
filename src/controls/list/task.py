"""
Module for representing individual download tasks in the Flet UI.
Defines the Task class with display, editing, completion, and deletion functionalities.
"""
import flet as ft
from config import OUTPUT_OPTIONS

class Task:
    """
    Represents a single download task with UI elements for display, editing, 
    completion, and deletion.

    Attributes:
        db_id: Optional database ID of the task.
        completed: Boolean indicating if the task is completed.
        service: Optional service object for database operations.
        task_name: Name of the task.
        quality: Download quality of the task.
        output_format: Output format of the download.
        link: Download link.
        task_status_change: Callback function to notify parent List of status changes.
        task_delete: Callback function to notify parent List of deletion.
        container: UI container holding the task rows.
        checkbox: Checkbox for selecting the task.
        name_cell: Text control for task name.
        link_cell: Container for displaying the link.
        quality_cell: Container for displaying the quality.
        format_cell: Container for displaying the output format.
        edit_button: Button to switch to edit mode.
        delete_button: Button to mark the task as completed.
        edit_name: TextField for editing the task name.
        edit_link: TextField for editing the link.
        edit_quality: Dropdown for editing the quality.
        edit_format: Dropdown for editing the format.
        save_button: Button to save edits.
        display_row: UI row for displaying the task.
        edit_row: UI row for editing the task.
    """

    def __init__(self, task_name, quality, output_format, link,
                 task_status_change, task_delete, container,
                 db_id=None, completed=False, service=None):
        """
        Initializes a Task object with given details and sets up its UI elements.

        Args:
            task_name: Name of the task.
            quality: Download quality.
            output_format: Output format (e.g., Mkv, Mp4).
            link: Download link.
            task_status_change: Callback to notify parent List of status change.
            task_delete: Callback to notify parent List of deletion.
            container: Parent UI container for task rows.
            db_id: Optional database ID.
            completed: Initial completion status.
            service: Optional service object for database operations.
        """
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

        self.checkbox = ft.Checkbox(value=self.completed, on_change=self.status_changed)

        self.name_cell = ft.Text(self.task_name, size=16, weight=ft.FontWeight.BOLD, expand=True)
        self.link_cell = ft.Container(content=ft.Text(self.link), padding=ft.padding.only(left=8, bottom=5))
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

        self.edit_button = ft.IconButton(icon=ft.Icons.CREATE_OUTLINED, on_click=self.edit_clicked)
        self.delete_button = ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, on_click=self.delete_clicked)

        self.edit_name = ft.TextField(
            value=self.task_name,
            border_color=ft.Colors.SECONDARY_CONTAINER,
            focused_border_color=ft.Colors.PRIMARY,
            expand=True
        )
        self.edit_link = ft.TextField(
            value=self.link,
            border_color=ft.Colors.SECONDARY_CONTAINER,
            focused_border_color=ft.Colors.PRIMARY,
            expand=True
        )
        self.edit_quality = ft.Dropdown(
            value=self.quality,
            options=[ft.dropdown.Option(o) for o in OUTPUT_OPTIONS["video"]["qualities"]],
            border_color=ft.Colors.SECONDARY_CONTAINER,
            focused_border_color=ft.Colors.PRIMARY
        )
        self.edit_format = ft.Dropdown(
            value=self.output_format,
            options=[ft.dropdown.Option(o) for o in OUTPUT_OPTIONS["video"]["formats"]],
            border_color=ft.Colors.SECONDARY_CONTAINER,
            focused_border_color=ft.Colors.PRIMARY
        )
        self.save_button = ft.IconButton(icon=ft.Icons.DONE_OUTLINE_OUTLINED, on_click=self.save_clicked)

        self.display_row = self.build_display_row()
        self.edit_row = self.build_edit_row()

    def build_display_row(self):
        """
        Builds the UI row for displaying the task in normal mode.

        Returns:
            ft.Card: The Flet card representing the task display row.
        """
        checkbox_value = False
        self.checkbox.value = checkbox_value

        if self.completed:
            action_buttons = []
            display_checkbox = None
        else:
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
        """
        Builds the UI row for editing the task.

        Returns:
            ft.Card: The Flet card representing the task edit row.
        """
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
        """
        Called when the task checkbox is toggled.
        Notifies the parent List to update filters and counts.
        """
        self.task_status_change(self)

    def edit_clicked(self, e):
        """
        Switches the task UI from display mode to edit mode.
        """
        idx = self.container.controls.index(self.display_row)
        self.container.controls[idx] = self.edit_row
        self.container.page.update()

    def save_clicked(self, e):
        """
        Saves changes made to the task, updates the database and UI,
        and notifies the parent List.
        """
        self.task_name = self.edit_name.value
        self.link = self.edit_link.value
        self.quality = self.edit_quality.value
        self.output_format = self.edit_format.value

        if self.service and self.db_id:
            self.service.update_item(
                self.db_id,
                title=self.task_name,
                link=self.link,
                quality=self.quality,
                output_format=self.output_format
            )

        self.name_cell.value = self.task_name
        self.link_cell.content.value = self.link
        self.quality_cell.content.controls[1].value = f"Quality: {self.quality}"
        self.format_cell.content.controls[1].value = f"Format: {self.output_format}"

        idx = self.container.controls.index(self.edit_row)
        self.container.controls[idx] = self.display_row
        self.container.page.update()

        self.task_status_change(self)

    def delete_clicked(self, e):
        """
        Marks the task as completed, updates the database, rebuilds the display row,
        and notifies the parent List.
        """
        self.completed = True
        self.checkbox.value = False

        if self.service and self.db_id:
            self.service.update_item(self.db_id, completed=True)

        idx = self.container.controls.index(self.display_row)
        self.container.controls[idx] = self.build_display_row()
        self.display_row = self.container.controls[idx]

        self.task_status_change(self)

    def is_completed(self):
        """
        Returns:
            bool: True if the task is marked as completed, else False.
        """
        return self.completed
