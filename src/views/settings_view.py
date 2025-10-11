import flet as ft
from src.db.db import create_services
from src.config import THEME, OUTPUT_OPTIONS

def settings_view(page: ft.Page) -> ft.Row:
    """
    Renders the settings view of the app with editable configuration fields.
    Loads SettingsService automatically from create_services().
    """
    services = create_services()
    service = services["settings_service"]
    settings = service.get_settings()

    def on_theme_change(e: ft.ControlEvent):
        new_theme = e.control.value
        page.theme_mode = ft.ThemeMode.DARK if new_theme == "dark" else ft.ThemeMode.LIGHT
        page.update()
        service.update_settings(theme=new_theme)

    def on_change(e: ft.ControlEvent):
        key = e.control.data
        value = e.control.value
        service.update_settings(**{key: value})

    def on_path_change(e: ft.ControlEvent):
        new_path = e.control.value
        service.update_settings(default_download_path=new_path)

    def on_reset_click(e: ft.ControlEvent):
        service.update_settings(
            theme="light",
            default_quality="The best",
            default_video_format="mp4",
            default_audio_format="mp3",
            default_download_path="C:/Downloads",
        )
        page.snack_bar = ft.SnackBar(ft.Text("Settings reset to defaults"))
        page.snack_bar.open = True
        page.theme_mode = ft.ThemeMode.LIGHT

        theme_radio.value = "light"
        quality_dropdown.value = "The best"
        video_format_dropdown.value = "mp4"
        audio_format_dropdown.value = "mp3"
        path_field.value = "C:/Downloads"
        page.update()

    theme_radio = ft.RadioGroup(
        content=ft.Column(
            [
                ft.Radio(label=t, value=t.lower()) for t in THEME
            ],
            spacing=5,
        ),
        value=settings.theme,
        on_change=on_theme_change,
    )
    personalization_section = ft.Column(
        [
            ft.Text("Personalization", style="headlineMedium"),
            theme_radio,
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
    )
    quality_dropdown = ft.Dropdown(
        label="Default download quality",
        options=[
            ft.dropdown.Option(o) for o in OUTPUT_OPTIONS["video"]["qualities"]
        ],
        value=settings.default_quality,
        width=250,
        on_change=on_change,
        data="default_quality",
    )

    video_format_dropdown = ft.Dropdown(
        label="Default video format",
        options=[ft.dropdown.Option(o) for o in OUTPUT_OPTIONS["video"]["formats"]],
        value=settings.default_video_format,
        width=250,
        on_change=on_change,
        data="default_video_format",
    )

    audio_format_dropdown = ft.Dropdown(
        label="Default audio format",
        options=[ft.dropdown.Option("mp3"), ft.dropdown.Option("FLAC")],
        value=settings.default_audio_format,
        width=250,
        on_change=on_change,
        data="default_audio_format",
    )

    path_field = ft.TextField(
        label="Default download folder",
        value=settings.default_download_path,
        width=400,
        on_change=on_path_change,
    )

    reset_button = ft.ElevatedButton(
        "Reset to defaults",
        icon=ft.icons.RESTART_ALT,
        on_click=on_reset_click,
    )

    general_section = ft.Column(
        [
            ft.Text("General", style="headlineMedium"),
            quality_dropdown,
            video_format_dropdown,
            audio_format_dropdown,
            path_field,
            ft.Row([reset_button]),
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
    )

    # --- LAYOUT ---
    return ft.Row(
        spacing=0,
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        general_section,
                        ft.Divider(),
                        personalization_section,
                    ],
                    spacing=30,
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
                margin=ft.margin.only(left=-40, top=60,right=40, bottom=40),
                expand=True,
            )
        ],
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True,
    )
