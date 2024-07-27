import datetime
from decimal import Decimal
from typing import Callable

import flet as ft
from accountant.database.db import CSVDataBase
from accountant.database.entry import Entry, FlowType

from flet_accountant.components.common.text_field import TextField


class NewEntry(ft.Container):
    """
    This Control creates an Entry form, that will allow adding entries to CSV DB

    Args:
        db_connection (CSVDataBase): The CSV DB Connection Interface
        on_adding (Callable[[ft.ControlEvent], None] | None, optional): The method, that had to be called on clicking the add entry button. Defaults to `None`.
        tag_list (list[str], optional): List of Pre-Made tag list. Defaults to `["grocery", "bill", "snacks", "milk"]`.
    """

    def __init__(
        self,
        db_connection: CSVDataBase,
        on_adding: Callable[[ft.ControlEvent], None] | None = None,
        *,
        tag_list: list[str] = ["grocery", "bill", "snacks", "milk"],
    ):
        """
        This Control creates an Entry form, that will allow adding entries to CSV DB

        Args:
            db_connection (CSVDataBase): The CSV DB Connection Interface
            on_adding (Callable[[ft.ControlEvent], None] | None, optional): The method, that had to be called on clicking the add entry button. Defaults to `None`.
            tag_list (list[str], optional): List of Pre-Made tag list. Defaults to `["grocery", "bill", "snacks", "milk"]`.
        """
        super().__init__()

        self._db_connection: CSVDataBase = db_connection
        self.on_adding = on_adding
        time_on_init: datetime.datetime = datetime.datetime.now()
        self.tag_list: list[str] = tag_list
        self._entry = Entry(name="", amount=Decimal(0), reason="")

        # The date picker control
        self._date_picker = ft.DatePicker(
            value=datetime.datetime.now(),
            open=False,
            on_change=self._set_date_text,
            on_dismiss=self._set_date_text,
        )

        # The time picker control
        self._time_picker = ft.TimePicker(
            value=datetime.datetime.now().time(),
            open=False,
            on_change=self._set_time_text,
            on_dismiss=self._set_time_text,
        )

        # Tag's drop down control
        self._tag_drop_down = ft.Dropdown(
            hint_text="Tags list",
            options=[
                ft.dropdown.Option(key=each, text=each.title())
                for each in self.tag_list
            ],
        )

        #
        # Widgets
        #
        self.date_text = ft.Container(
            ft.Text(time_on_init.strftime("%d %B, %Y")),
            on_click=self._open_date_picker,
            tooltip="Click to set date",
            padding=ft.padding.all(10),
            border_radius=ft.border_radius.all(5),
            bgcolor=ft.colors.OUTLINE_VARIANT,
        )
        self.time_text = ft.Container(
            ft.Text(time_on_init.strftime("%I:%M:%S %p")),
            on_click=self._open_time_picker,
            tooltip="Click to set time",
            padding=ft.padding.all(10),
            border_radius=ft.border_radius.all(5),
            bgcolor=ft.colors.OUTLINE_VARIANT,
        )
        self.name_text = TextField(
            label="Enter your Name ...", on_submit=self._on_submitting_name_field
        )
        self.amount_text = TextField(
            prefix_icon=ft.icons.CURRENCY_RUPEE,
            label="Enter the Amount ...",
            keyboard_type=ft.KeyboardType.NUMBER,
            on_submit=self._on_submitting_amount_field,
            on_change=self._check_amount_text_field,
        )
        self.reason_text = TextField(
            label="Enter the Reason ...", on_submit=self._on_submitting_reason_field
        )

        self.tag_text = ft.Container(
            ft.Text("Tag"),
            on_click=self._open_tag_list_dropdown,
            padding=ft.padding.all(10),
            border_radius=ft.border_radius.all(5),
        )

        self.flow_type_drop_down = ft.Dropdown(
            label="Flow Type",
            options=[
                ft.dropdown.Option(FlowType.CREDIT),
                ft.dropdown.Option(FlowType.DEBIT),
                ft.dropdown.Option(FlowType.SAVINGS),
            ],
        )

        self.flow_type_text = ft.Container(
            ft.Text("Cash Flow Type"),
            on_click=self._open_flow_type_list_dropdown,
            padding=ft.padding.all(10),
            border_radius=ft.border_radius.all(5),
        )

        # The button that's responsible for the addition of the entry
        self.add_button = ft.ElevatedButton(
            text="Add Entry",
            icon=ft.icons.ADD_CIRCLE,
            on_click=self._add_entry,
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(horizontal=20, vertical=10),
                elevation=6.285714285714286,  # 2PI
            ),
        )

        self.content = ft.Card(
            ft.Container(
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                self._date_picker,
                                self.date_text,
                                self._time_picker,
                                self.time_text,
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                        self.name_text,
                        self.amount_text,
                        self.reason_text,
                        ft.Row(
                            controls=[
                                self.tag_text,
                                self._tag_drop_down,
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Row(
                            controls=[
                                self.flow_type_text,
                                self.flow_type_drop_down,
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        self.add_button,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    spacing=10,
                ),
                padding=20,
                expand=True,
                alignment=ft.alignment.center,
            ),
            elevation=4,
        )

    @property
    def entry(self) -> Entry:
        return self._entry

    def _open_date_picker(self, e) -> None:
        self._date_picker.open = True
        self.update()

    def _open_time_picker(self, e) -> None:
        self._time_picker.open = True
        self.update()

    def _update_tag_choice(self, e) -> None:
        self.tag_text.content.value = self._tag_drop_down.value  # type: ignore
        self._tag_drop_down.visible = False
        self.tag_text.visible = True
        self.update()

    def _open_tag_list_dropdown(self, e) -> None:
        self._tag_drop_down.visible = True
        self.tag_text.visible = False
        self.update()

    def _set_date_text(self, e) -> None:
        self.date_text.content.value = self._date_picker.value.strftime("%d %B, %Y")  # type: ignore
        self.date_text.content.data = self._date_picker.value  # type: ignore
        self.update()

    def _set_time_text(self, e):
        val: datetime.time | None = self._time_picker.value
        hour: int = val.hour % 12  # type: ignore
        if val.hour > 12:  # type: ignore
            session = "PM"
        else:
            session = "AM"
        self.time_text.content.value = (  # type: ignore
            f"{hour:02}:{val.minute:02}:{val.second:02} {session}"  # type: ignore
        )
        self.time_text.content.data = self._time_picker.value  # type: ignore
        self.update()

    #
    # Internal Text field checkers
    #
    def _check_amount_text_field(self, e: ft.ControlEvent) -> None:
        """
        Checks the amount field only contains the digits and .

        Args:
            e (ft.ControlEvent): _description_
        """
        text_field: ft.TextField = e.control
        amount_string = str(text_field.value)

        if not amount_string.isspace():
            if not amount_string == "":  # needs more improvement, its very clear
                if not self._check_amount_data(amount_string):
                    text_field.error_text = f"{amount_string} is Not Valid Amount, Please Enter a Valid Number"
                    self.update()
                else:
                    text_field.error_text = None
                    self.update()

    def _check_amount_data(self, chars: str) -> bool:
        """
        Checks whether the given string contains only Digits

        Args:
            chars (str): The amount string to check

        Returns:
            bool: Returns `True` if the given string is an amount string, otherwise `False`.
        """
        return chars.isdigit()

    def _on_submitting_name_field(self, e) -> None:
        self.amount_text.focus()
        self.update()

    def _on_submitting_amount_field(self, e) -> None:
        self.reason_text.focus()
        self.update()

    def _on_submitting_reason_field(self, e) -> None:
        self._tag_drop_down.focus()
        self.update()

    def _open_flow_type_list_dropdown(self, e) -> None:
        self.flow_type_drop_down.visible = True
        self.flow_type_text.visible = False
        self.update()

    def _add_entry(self, e: ft.ControlEvent) -> None:
        if self._check_amount_data(str(self.amount_text.value)):
            self._entry.amount = Decimal(
                str(self.amount_text.value)
            )  # needs error handling btw

        date_info: datetime.datetime = datetime.datetime.strptime(
            self.date_text.content.value,  # type: ignore
            "%d %B, %Y",
        )
        time_info: datetime.datetime = datetime.datetime.strptime(
            self.time_text.content.value,  # type: ignore
            "%I:%M:%S %p",
        )

        self._entry.date_time = str(
            datetime.datetime(
                year=date_info.year,
                month=date_info.month,
                day=date_info.day,
                hour=time_info.hour,
                minute=time_info.minute,
                second=time_info.second,
            )
        )
        if self.flow_type_text.content.value.lower() in ["credit"]:  # type: ignore
            self._entry.flow_type = FlowType.CREDIT
        if self.flow_type_text.content.value.lower() in ["debit"]:  # type: ignore
            self._entry.flow_type = FlowType.DEBIT
        if self.flow_type_text.content.value.lower() in ["savings"]:  # type: ignore
            self._entry.flow_type = FlowType.SAVINGS

        self._entry.reason = str(self.reason_text.value)
        self._entry.tag = self._tag_drop_down.value
        self._entry.name = str(self.name_text.value)

        result: bool = self._db_connection.write([self._entry])
        if result:
            self._entry = Entry(name="", amount=Decimal(0), reason="")
            self.date_text.content.value = "Date"  # type: ignore
            self.time_text.content.value = "Time"  # type: ignore
            self.name_text.value = None
            self.reason_text.value = None
            self.amount_text.value = None

        self.update()

        if self.on_adding is not None:
            self.on_adding(e)
