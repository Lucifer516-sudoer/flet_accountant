import flet as ft
from flet_accountant.config import APP_NAME


class TitleBar(ft.AppBar):
    """
    A custom title bar for the application.

    This title bar displays a centered row of widgets containing an icon and a text
    label.

    Attributes:
        title (ft.Container): The title container with a centered row of widgets.
        adaptive (bool): Whether the app bar is adaptive to screen size.
        bgcolor (str): The background color of the app bar.

    Methods:
        __init__ (): Initializes the title bar.
    """

    def __init__(self, actions: list[ft.Control] | None = None):
        """
        Initializes the title bar.

        Calls the parent class's constructor and sets up the title container with a
        centered row of widgets.
        """
        super().__init__(actions=actions)

        self.title = ft.Container(
            ft.Row(
                controls=[ft.Icon(ft.icons.CURRENCY_RUPEE), ft.Text(value=APP_NAME)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            expand=True,
        )
        self.adaptive = True
        self.bgcolor = ft.colors.SURFACE_VARIANT
