from typing import Any, Callable, Dict, List

import flet as ft
from accountant.database.entry import Entry

from flet_accountant.components.data_visualizer.paginated_data_table import (
    PaginatedDataTable,
)


class EntryRow(ft.DataRow):
    def __init__(
        self,
        entry: Entry,
        color: None | str | Dict[ft.ControlState, str] = None,
        selected: bool | None = None,
        on_long_press: Callable[[ft.ControlEvent], None] | None = None,
        on_select_changed: Callable[[ft.ControlEvent], None] | None = None,
        ref=None,
        visible: bool | None = None,
        disabled: bool | None = None,
        data: Any = None,
    ):
        self.entry_data = entry

        super().__init__(
            cells=[
                ft.DataCell(content=ft.Text("1")),
                ft.DataCell(content=ft.Text(str(self.entry_data.date_time))),
                ft.DataCell(content=ft.Text(str(self.entry_data.name))),
                ft.DataCell(
                    content=ft.Text(str("\u20b9 ") + str(self.entry_data.amount)),
                ),
                ft.DataCell(content=ft.Text(str(self.entry_data.reason))),
                ft.DataCell(content=ft.Text(str(self.entry_data.tag))),
                ft.DataCell(content=ft.Text(str(self.entry_data.flow_type))),
            ],
            color=color,
            selected=selected,
            on_long_press=on_long_press,
            on_select_changed=on_select_changed,
            ref=ref,
            visible=visible,
            disabled=disabled,
            data=data,
        )


class EntryTable(ft.DataTable):
    def __init__(self, rows: List[EntryRow]):
        super().__init__(
            columns=[
                ft.DataColumn(label=ft.Text("S.No"), numeric=True),
                ft.DataColumn(label=ft.Text("Date & Time")),
                ft.DataColumn(label=ft.Text("Name")),
                ft.DataColumn(label=ft.Text("Amount"), numeric=True),
                ft.DataColumn(label=ft.Text("Reason")),
                ft.DataColumn(label=ft.Text("Tag")),
                ft.DataColumn(label=ft.Text("Flow Type")),
            ],
            rows=rows,  # type: ignore
        )


class PaginatedEntryTable(PaginatedDataTable):
    def __init__(
        self,
        datatable: ft.DataTable,
        table_title: str = "Default Title",
        rows_per_page: int = 5,
    ):
        super().__init__(datatable, table_title, rows_per_page)
