import canopen
import can
from can import Message
import flet as ft


class RPdoCommunicationPanel(ft.ResponsiveRow):
    def __init__(self, od):
        super().__init__()
        self.visible = False

        self.controls = [
            ft.Text("TODO rx_pdo_communication_panel")
        ]
