import flet as ft
from src.controls.list.task import Task
from src.db.db import create_services

class List(ft.Column):
    def __init__(self):
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
            options=[ft.dropdown.Option(o) for o in ["The best", "1440p", "1080p", "720p", ">=480p"]],
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

        # Wczytanie istniejących
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
        self.apply_filter()    # filtruje zadania według Active/Completed
        self.update_counts()   # aktualizuje licznik
        self.update()          # odświeża UI
        
    def set_as_completed_clicked(self, e):
        # działa tylko w Active
        for task in self.tasks:
            if not task.completed and task.checkbox.value:
                task.completed = True
                task.checkbox.value = False  # po zmianie odznaczamy
                if task.service and task.db_id:
                    task.service.update_item(task.db_id, completed=True)
                # odbudowa row, aby kosz zniknął
                idx = self.rows_container.controls.index(task.display_row)
                self.rows_container.controls[idx] = task.build_display_row()
                task.display_row = self.rows_container.controls[idx]

        # odśwież widok i liczniki
        self.apply_filter()
        self.update_counts()
        self.update()
    
    def task_delete(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
            if task.display_row in self.rows_container.controls:
                self.rows_container.controls.remove(task.display_row)
        self.update_counts()
        self.update()

    def tabs_changed(self, e):
        self.apply_filter()
        self.update_counts()  # <- odświeżenie stopki po zmianie zakładki
        self.update()

    def apply_filter(self):
        mode = self.filter.tabs[self.filter.selected_index].text
        self.rows_container.controls.clear()
        for task in self.tasks:
            if mode == "Active" and not task.completed:
                self.rows_container.controls.append(task.display_row)
            elif mode == "Completed" and task.completed:
                self.rows_container.controls.append(task.display_row)

    def update_counts(self):
        if self.filter.selected_index == 0:  # Active
            selected = sum(1 for task in self.tasks if not task.completed and task.checkbox.value)
            self.items_left.value = f"{selected} item(s) selected"
            self.set_completed_button.visible = True
        else:  # Completed
            self.items_left.value = ""  # lub np. "Completed"
            self.set_completed_button.visible = False