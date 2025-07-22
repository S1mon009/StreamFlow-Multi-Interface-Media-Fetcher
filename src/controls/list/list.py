import flet as ft
from src.controls.list.task import Task

class List(ft.Column):
    def __init__(self):
        super().__init__()
        # New task inputs: Task, Link, Quality, Format, Add button
        self.input_task = ft.TextField(hint_text="What would you like to download?", border_color=ft.Colors.SECONDARY_CONTAINER, focused_border_color=ft.Colors.PRIMARY, expand=True)
        self.input_link = ft.TextField(label="Link", border_color=ft.Colors.SECONDARY_CONTAINER, focused_border_color=ft.Colors.PRIMARY, expand=True)
        self.input_quality = ft.Dropdown(label="Quality", width=130, value="1080p", options=[ft.dropdown.Option(o) for o in ["The best","1440p","1080p","720p",">=480p"]], 
                                        border_color=ft.Colors.SECONDARY_CONTAINER, focused_border_color=ft.Colors.PRIMARY)
        self.input_format = ft.Dropdown(label="Format", width=100, value="Mkv", options=[ft.dropdown.Option(o) for o in ["Mkv","Mp4"]], 
                                        border_color=ft.Colors.SECONDARY_CONTAINER, focused_border_color=ft.Colors.PRIMARY)
        add_btn = ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=self.add_clicked)

        inputs = ft.Row(spacing=10, controls=[
            self.input_task, self.input_link, self.input_quality, self.input_format, add_btn
        ])

        # Container for rows
        self.rows_container = ft.Column()

        # Filter tabs
        self.filter = ft.Tabs(selected_index=0, on_change=self.tabs_changed,
                              tabs=[ft.Tab(text="Active"), ft.Tab(text="Completed"), ft.Tab(text="All")])
        # Footer
        self.items_left = ft.Text("0 items left")
        footer = ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[self.items_left, ft.OutlinedButton(text="Clear completed", on_click=self.clear_clicked)])

        self.controls = [inputs, self.filter, self.rows_container, footer]

    def add_clicked(self, e):
        name = self.input_task.value
        link = self.input_link.value
        quality = self.input_quality.value
        fmt = self.input_format.value
        if name:
            task = Task(name, quality, fmt, link, self.task_status_change, self.task_delete, self.rows_container)
            self.rows_container.controls.append(task.display_row)
            self.update_counts()
            # reset inputs
            self.input_task.value = ""
            self.input_link.value = ""
            self.input_quality.value = "1080p"
            self.input_format.value = "Mkv"
            self.update()

    def task_status_change(self, task):
        self.update_counts()

    def task_delete(self, task):
        self.update_counts()

    def tabs_changed(self, e):
        mode = e.control.tabs[e.control.selected_index].text
        for row in self.rows_container.controls:
            checkbox = row.controls[0]
            row.visible = (mode == "All" or (mode == "Active" and not checkbox.value) or (mode == "Completed" and checkbox.value))
        self.update_counts()

    def clear_clicked(self, e):
        for row in list(self.rows_container.controls):
            checkbox = row.controls[0]
            if checkbox.value:
                self.rows_container.controls.remove(row)
        self.update_counts()

    def update_counts(self):
        active = sum(1 for row in self.rows_container.controls if not row.controls[0].value)
        self.items_left.value = f"{active} active item(s) left"
        self.update()