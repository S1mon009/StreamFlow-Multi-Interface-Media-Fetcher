"""
Module for managing a download task list UI using Flet.
Defines the List class which handles task creation, display, filtering, and completion status.
"""

import flet as ft
from src.controls.list.task import Task
from src.db.db import create_services
from src.config import OUTPUT_OPTIONS


class List(ft.Column):
    """
    A UI component representing a task list for downloads.

    Attributes:
        service: Service object for database operations.
        input_task: TextField for entering task names.
        input_link: TextField for entering download links.
        input_quality: Dropdown for selecting download quality.
        input_format: Dropdown for selecting file format.
        rows_container: Column containing all task display rows.
        tasks: List of Task objects.
        filter: Tabs for filtering tasks (Active/Completed).
        items_left: Text displaying count of selected tasks.
        set_completed_button: Button to mark selected tasks as completed.
    """

    def __init__(self):
        """
        Initializes the List component, loads existing tasks from the service,
        and sets up the UI elements including input fields, buttons, and filters.
        """
        super().__init__()

        services = create_services()
        self.service = services['list_service']

        self.input_task = ft.TextField(
            hint_text="What would you like to download?",
            border_color=ft.Colors.SECONDARY_CONTAINER,
            focused_border_color=ft.Colors.PRIMARY,
            expand=True
        )
        self.input_link = ft.TextField(
            label="Link",
            border_color=ft.Colors.SECONDARY_CONTAINER,
            focused_border_color=ft.Colors.PRIMARY,
            expand=True
        )
        self.input_quality = ft.Dropdown(
            label="Quality",
            width=130,
            value="1080p",
            options=[ft.dropdown.Option(o) for o in OUTPUT_OPTIONS["video"]["qualities"]],
            border_color=ft.Colors.SECONDARY_CONTAINER,
            focused_border_color=ft.Colors.PRIMARY
        )
        self.input_format = ft.Dropdown(
            label="Format",
            width=100,
            value="Mkv",
            options=[ft.dropdown.Option(o) for o in ["Mkv", "Mp4"]],
            border_color=ft.Colors.SECONDARY_CONTAINER,
            focused_border_color=ft.Colors.PRIMARY
        )
        add_btn = ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=self.add_clicked)

        inputs = ft.Row(
            spacing=10,
            controls=[self.input_task, self.input_link, self.input_quality, self.input_format, add_btn]
        )

        self.rows_container = ft.Column()
        self.tasks: list[Task] = []

        self.filter = ft.Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[ft.Tab(text="Active"), ft.Tab(text="Completed")]
        )

        self.items_left = ft.Text("0 items left")
        self.set_completed_button = ft.OutlinedButton(text="Set as completed", on_click=self.set_as_completed_clicked)
        footer = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[self.items_left, ft.Row(controls=[self.set_completed_button])]
        )

        self.controls = [inputs, self.filter, self.rows_container, footer]

        for item in self.service.list_all():
            task = Task(
                item.title, item.quality, item.output_format, item.link,
                self.task_status_change, self.task_delete, self.rows_container,
                db_id=item.id, completed=item.completed, service=self.service
            )
            self.tasks.append(task)
            if not task.completed:
                self.rows_container.controls.append(task.display_row)
        self.update_counts()

    def add_clicked(self, e):
        """
        Handles the click event of the add button.
        Creates a new task and updates the UI with the new task.
        """
        name = self.input_task.value
        link = self.input_link.value
        quality = self.input_quality.value
        fmt = self.input_format.value

        if name:
            db_item = self.service.add_item(name, link, quality, fmt)
            task = Task(
                db_item.title, db_item.quality, db_item.output_format, db_item.link,
                self.task_status_change, self.task_delete, self.rows_container,
                db_id=db_item.id, completed=db_item.completed, service=self.service
            )
            self.tasks.append(task)
            self.rows_container.controls.append(task.display_row)
            self.update_counts()

            self.input_task.value = ""
            self.input_link.value = ""
            self.input_quality.value = "1080p"
            self.input_format.value = "Mkv"
            self.update()

    def task_status_change(self, task):
        """
        Updates the display and counts when a task's completion status changes.
        """
        self.apply_filter()
        self.update_counts()
        self.update()

    def set_as_completed_clicked(self, e):
        """
        Marks all selected active tasks as completed and updates the UI accordingly.
        """
        for task in self.tasks:
            if not task.completed and task.checkbox.value:
                task.completed = True
                task.checkbox.value = False
                if task.service and task.db_id:
                    task.service.update_item(task.db_id, completed=True)
                idx = self.rows_container.controls.index(task.display_row)
                self.rows_container.controls[idx] = task.build_display_row()
                task.display_row = self.rows_container.controls[idx]

        self.apply_filter()
        self.update_counts()
        self.update()

    def task_delete(self, task):
        """
        Deletes a task from the task list and updates the UI.
        """
        if task in self.tasks:
            self.tasks.remove(task)
            if task.display_row in self.rows_container.controls:
                self.rows_container.controls.remove(task.display_row)
        self.update_counts()
        self.update()

    def tabs_changed(self, e):
        """
        Updates the display when the filter tab (Active/Completed) is changed.
        """
        self.apply_filter()
        self.update_counts()
        self.update()

    def apply_filter(self):
        """
        Filters the displayed tasks according to the selected tab (Active or Completed).
        """
        mode = self.filter.tabs[self.filter.selected_index].text
        self.rows_container.controls.clear()
        for task in self.tasks:
            if mode == "Active" and not task.completed:
                self.rows_container.controls.append(task.display_row)
            elif mode == "Completed" and task.completed:
                self.rows_container.controls.append(task.display_row)

    def update_counts(self):
        """
        Updates the items_left text and visibility of the set_completed_button
        based on the current tab and selected tasks.
        """
        if self.filter.selected_index == 0:
            selected = sum(1 for task in self.tasks if not task.completed and task.checkbox.value)
            self.items_left.value = f"{selected} item(s) selected"
            self.set_completed_button.visible = True
        else:
            self.items_left.value = ""
            self.set_completed_button.visible = False