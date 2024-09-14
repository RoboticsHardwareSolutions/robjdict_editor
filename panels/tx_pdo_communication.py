import canopen
import can
from can import Message
import flet as ft


class TPdoCommunicationPanel(ft.ResponsiveRow):
    def __init__(self, od):
        super().__init__()
        self.visible = False

        self.controls = [
            ft.Text("TODO tx_pdo_communication_panel")
        ]
