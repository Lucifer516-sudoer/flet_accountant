from datetime import datetime
import flet as ft
from accountant.database.entry import Entry


class EntryData(ft.Container):
    def __init__(self):
        super().__init__()
        self.adaptive = True

        self.date_picker = ft.DatePicker(value=datetime.now())
        self.date_time = ft.Text(str(self.date_picker.value))
        self.name = ft.Text()
        self.amount = ft.Text()
        self.reason = ft.Text()
        self.tag = ft.Text()
        self.flow_type = ft.Text()


def main(page):
    page.add(EntryData())


ft.app(target=main)
