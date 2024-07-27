"""
Author: V. Harish (aka) Lucifer516-sudoer

This is the main entry point of the script, handling most of the things
"""

from logging import Handler
from typing import Callable, Literal

import flet as ft
from accountant.database.db import CSVDataBase
from accountant.logging import (
    RichConsoleHandler,
    RichFileHandler,
    app_logger,
    configure_present_loggers,
    create_log_file,
    logging,
)

from flet_accountant.components.navigation.app_bar import TitleBar
from flet_accountant.components.navigation.nav_bar import (
    MenuItem,
    NavRail,
)
from flet_accountant.components.new_entry_tab.new_entry import NewEntry
from flet_accountant.components.theming.theme_switcher import ThemeSwitcher
from flet_accountant.config import (
    APP_NAME,
    DB_FILE_PATH,
    DB_FOLDER,
    HOME,
    LOG_FOLDER,
)


# Flet loggers
flet_core_logger = logging.getLogger("flet_core")
flet_logger = logging.getLogger("flet")

# Setting level of the loggers found
# ? Is it necessary to add these logging related to, the `init_app_logger` method
app_logger.setLevel(logging.DEBUG)
flet_logger.setLevel(logging.DEBUG)
flet_core_logger.setLevel(logging.DEBUG)


def _setup_app_dir() -> bool:
    """
    Sets up the App's directory and stuff, if it doesn't exist.

    Returns:
        bool: Returns the created status, either `True` or `False`
    """
    try:
        Oks: list[bool] = [False] * 4
        app_logger.info("Creating necessary directories if needed")
        if not HOME.exists():
            HOME.mkdir(parents=True)
            app_logger.debug(f"Created Home directory: {HOME}")
            Oks[0] = True
        if not DB_FOLDER.exists():
            DB_FOLDER.mkdir(parents=True)
            app_logger.debug(f"Created Database directory: {DB_FOLDER}")
            Oks[1] = True

        if not DB_FILE_PATH.exists():
            DB_FILE_PATH.touch()
            app_logger.debug(f"Created Database file: {DB_FILE_PATH}")
            Oks[2] = True

        if not LOG_FOLDER.exists():
            LOG_FOLDER.mkdir(parents=True)
            app_logger.debug(f"Created Logs directory: {LOG_FOLDER}")
            Oks[3] = True

        if not (HOME / "config.txt").exists():
            with open((HOME / "config.txt"), "w") as file:
                file.write("Works like Charm\n")
        return all(Oks)

    except Exception:
        return False


def init_app_logging(screen: bool = False) -> bool:
    """
    Initializes logging for the app, based on the args passed, with the `RichHandler`'s

    Args:
        screen (bool, optional): Whether to show logging output on the screen (i.e. `console`). Defaults to `False`.

    Returns:
        bool: Returns `True`, if logging was initialized without any issue, otherwise `False`.
    """
    try:
        handlers: list[Handler] = [
            RichFileHandler(file=create_log_file(LOG_FOLDER), level=logging.DEBUG)
        ]  # Yah, even though it contains mostly RichHandlers
        if screen:
            handlers.append(RichConsoleHandler(level=logging.DEBUG))

        configure_present_loggers(
            loggers=[app_logger, flet_core_logger, flet_logger],
            handlers=handlers,
        )

        return True

    except Exception:
        return False


async def check_for_app_dirs(page: ft.Page) -> None:
    """
    Couroutine, which will be called inside, a main function of flet's target function, that allows showing an `alert dialog`,
    when there are no app directories present.

    Args:
        page (ft.Page): The Page object where the `alert dialog` will be added as an overlay
    """

    async def _internal_alert_dialog(
        wt_to_show: str, on_proceed: Callable[[ft.ControlEvent], None] | None = None
    ):
        page.overlay.append(
            ft.AlertDialog(
                open=True,
                title=ft.Text(f"Application's {wt_to_show} Folder Not Found"),
                elevation=15,
                content=ft.Row(
                    controls=[
                        ft.Column(controls=[ft.Text("Shall we proceed to install ?")]),
                        ft.ElevatedButton(text="Yes, Proceed", on_click=on_proceed),
                        ft.ElevatedButton(
                            text="No, Exit!", on_click=page.window.close()
                        ),
                    ]
                ),
            )
        )
        await page.update_async()

    wt_are_not_found = ""
    if not HOME.exists():
        wt_are_not_found += "Home Directory, "
        print(f"Not Found list: {wt_are_not_found}")
    if not DB_FOLDER.exists():
        wt_are_not_found += "Database Directory, "
        print(f"Not Found list: {wt_are_not_found}")
    if not DB_FILE_PATH.exists():
        wt_are_not_found += "Database File, "
        print(f"Not Found list: {wt_are_not_found}")
    if not LOG_FOLDER.exists():
        wt_are_not_found += "Log Directory, "
        print(f"Not Found list: {wt_are_not_found}")

    await _internal_alert_dialog(wt_are_not_found)


def get_db_connection() -> CSVDataBase:
    """
    Returns a database instance of the `CSVDataBase` interface,  with the default `DB_FILE_PATH`

    Returns:
        CSVDataBase: The CSV DB Interface, with the default DB File Path
    """

    return CSVDataBase(DB_FILE_PATH)


def main(page: ft.Page):
    # Initialising app logging and stuffs, in the very first start
    init_app_logging(screen=True)
    app_logger.info(f"Directory setup result: {_setup_app_dir()}")

    #
    # Page level configs
    #
    page.title = APP_NAME
    page.theme = ft.Theme(color_scheme_seed="#100a7a")
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO
    page.appbar = TitleBar(  # The apps top bar
        actions=[
            ThemeSwitcher(
                icon=(
                    ft.icons.DARK_MODE
                    if page.theme_mode == ft.ThemeMode.LIGHT
                    else ft.icons.LIGHT_MODE
                )
            )
        ]
    )

    #
    # App's Database
    #
    db: CSVDataBase = get_db_connection()

    #
    # Apps Nav bar stuff
    # - New Entry Tab
    # - Dashboard
    #   +-- View Visualisations and stuff
    #   +-- Record of the data entries ( Must also allow to search through entries )
    # - Edit Entries
    #

    #
    # New Entry Tab
    #
    add_entry = MenuItem(
        nav_destination=ft.NavigationRailDestination(
            label="Add entry",
            icon=ft.icons.ADD_TASK,
        ),
        nav_content=ft.Column(controls=[NewEntry(db_connection=db)]),
    )

    #
    # The main Navigation rail control
    #

    navigation_items: list[MenuItem] = [add_entry]
    navigation_rail = ft.Container(
        NavRail(menu_items=navigation_items),
        height=page.width,
    )

    page.add(navigation_rail)
    page.update()


ft.app(target=main)
