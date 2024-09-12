import canopen
import can
from can import Message
import flet as ft


class SdoCommunicationPanel(ft.ResponsiveRow):
    def __init__(self, od):
        super().__init__()
        self.visible = False
        self.od = od

        self.controls = [
            ft.Text("TODO sdo_communication_panel")
        ]

    def update_od(self, od):
        return od
