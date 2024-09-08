import canopen
import can
from can import Message
import flet as ft


class ObjDictPanel(ft.ResponsiveRow):
    def __init__(self, od):
        super().__init__()
        self.visible = False

        self.controls = [
            ft.Text("TODO object_dictionary_panel")
        ]
