import flet as ft

from accountant.interfaces.config import APP_NAME
from flet_accountant.components.app_bar import TitleBar
from flet_accountant.components.nav_bar import MenuItem, NavRail
from flet_accountant.components.theme_switcher import ThemeSwitcher


def main(page: ft.Page):
    page.title = APP_NAME
    page.theme_mode = ft.ThemeMode.DARK
    default_icon = (
        ft.icons.DARK_MODE
        if page.theme_mode == ft.ThemeMode.LIGHT
        else ft.icons.LIGHT_MODE
    )
    # page.add(ThemeSwitcher(icon=default_icon))
    page.appbar = TitleBar()
    page.add(
        NavRail(
            menu_items=[
                MenuItem(
                    ft.NavigationRailDestination(
                        icon=ft.icons.ABC_OUTLINED,
                        label="Label 1",
                    ),
                    ThemeSwitcher(icon=default_icon),
                ),
                MenuItem(
                    ft.NavigationRailDestination(
                        icon=ft.icons.ABC_OUTLINED,
                        label="Label 2",
                    ),
                    ft.Text("Label 2"),
                ),
                MenuItem(
                    ft.NavigationRailDestination(
                        icon=ft.icons.ABC_OUTLINED,
                        label="Label 3",
                    ),
                    ft.Text("Label 3"),
                ),
            ]
        )
    )

    page.update()


ft.app(target=main)
