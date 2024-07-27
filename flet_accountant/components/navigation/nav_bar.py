from dataclasses import dataclass
import flet as ft


@dataclass
class MenuItem:
    """
    Represents a menu item in the navigation rail.

    Attributes:
        nav_destination (ft.NavigationRailDestination): The navigation rail destination.
        nav_content (ft.Control): The content to be displayed when the menu item is selected.
    """

    nav_destination: ft.NavigationRailDestination
    nav_content: ft.Control


class NavRail(ft.UserControl):
    """
    A custom navigation rail control.

    Attributes:
        menu_items (list[MenuItem]): A list of menu items.
        _nav_rail (ft.NavigationRail): The underlying navigation rail control.
        contents (ft.Container): The container to hold the content of the selected menu item.
        expand (bool): Whether the navigation rail should expand to fill the available space.

    Example:
        >>> menu_items = [
        ...     MenuItem(ft.NavigationRailDestination(icon="home"), ft.Text("Home")),
        ...     MenuItem(ft.NavigationRailDestination(icon="settings"), ft.Text("Settings")),
        ... ]
        >>> nav_rail = NavRail(menu_items)
    """

    def __init__(
        self,
        menu_items: list[MenuItem],
    ):
        """
        Initializes the navigation rail control.

        Args:
            menu_items (list[MenuItem]): A list of menu items.
        """
        super().__init__()
        self.menu_items = menu_items

        self._nav_rail = ft.NavigationRail(
            destinations=[each.nav_destination for each in self.menu_items],
            on_change=self._on_nav_rail_change,
            selected_index=0,
        )

        self.contents = ft.Container(expand=True)
        self.expand = True

    def did_mount(self):
        """
        Called when the control is mounted.

        Returns:
            None
        """
        if len(self.menu_items) > 0:
            item = self._get_menu_item()
            if item:
                self.contents.content = item.nav_content
                self.update()
        return super().did_mount()

    def _get_menu_item(self) -> MenuItem | None:
        """
        Gets the currently selected menu item.

        Returns:
            MenuItem: The currently selected menu item.
        """
        for index, each in enumerate(self.menu_items):
            if self._nav_rail.selected_index == index:
                return each

    def _on_nav_rail_change(self, e: ft.ControlEvent):
        """
        Called when the navigation rail selection changes.

        Args:
            e (ft.ControlEvent): The control event.

        Returns:
            None
        """
        item = self._get_menu_item()
        if item:
            self.contents.content = item.nav_content
            self.update()

    def build(self):
        """
        Builds the navigation rail control.

        Returns:
            ft.Row: The navigation rail control.
        """
        return ft.Row(
            controls=[
                self._nav_rail,
                ft.VerticalDivider(width=1, thickness=0.75),
                self.contents,
            ]
        )
