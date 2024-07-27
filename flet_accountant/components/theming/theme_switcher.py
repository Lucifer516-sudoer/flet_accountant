import flet as ft


class ThemeSwitcher(ft.IconButton):
    def __init__(self, icon: str | None = None):
        super().__init__(icon=icon, on_click=self._on_click)

    def _on_click(self, e: ft.ControlEvent):
        control_page: ft.Page = e.control.page
        current_theme: ft.ThemeMode = e.control.page.theme_mode

        def change_to_dark():
            control_page.theme_mode = ft.ThemeMode.DARK
            self.icon = ft.icons.LIGHT_MODE
            control_page.update()

        def change_to_light():
            control_page.theme_mode = ft.ThemeMode.LIGHT
            self.icon = ft.icons.DARK_MODE
            control_page.update()

        match current_theme:
            case ft.ThemeMode.DARK:
                change_to_light()
            case ft.ThemeMode.LIGHT:
                change_to_dark()
            case ft.ThemeMode.SYSTEM:
                change_to_light()
            case _:
                pass
