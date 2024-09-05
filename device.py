import os
import canopen
import can
from can import Message
import flet as ft


class CustomTab(ft.UserControl):
    def __init__(self, path_to_od):
        super().__init__()
        self.path_to_od = path_to_od
        self.name_od = os.path.basename(path_to_od)

        self.cssb = ft.CupertinoSlidingSegmentedButton(
            selected_index=0,
            thumb_color=ft.colors.BLUE_400,
            on_change=self.__seg_btm,
            padding=ft.padding.symmetric(0, 10),
            controls=[
                ft.Text("Device info"),
                ft.Text("Common communication"),
                ft.Text("SDO communication"),
                ft.Text("PDO communication"),
            ],
        )

        network = canopen.Network()
        od = network.add_node(1, object_dictionary=self.path_to_od)

        # Device info
        self.text_node_id = ft.Text("Node ID")
        self.text_edit_node_id = ft.TextField(od.id)
        self.text_dev_type = ft.Text("Device Type")
        self.text_edit_dev_type = ft.TextField(od.object_dictionary[0x1000].default)

        self.device_info_panel = ft.Row([
            self.text_node_id,
            self.text_edit_node_id,
            self.text_dev_type,
            self.text_edit_dev_type
        ]
        )

        # Common communication
        self.text_hb = ft.Text("Producer Heartbeat Time, ms:")
        self.text_edit_hb = ft.TextField(od.object_dictionary[0x1017].default)
        self.common_communication_panel = ft.Row([
            self.text_hb,
            self.text_edit_hb
        ],
            visible=False
        )
        self.info_column = ft.Column([
            self.cssb,
            self.device_info_panel,
            self.common_communication_panel
        ])

    def build(self):
        return self.info_column

    def __seg_btm(self, e):
        if e.data == '0':
            self.device_info_panel.visible = True
            self.common_communication_panel.visible = False
        if e.data == '1':
            self.device_info_panel.visible = False
            self.common_communication_panel.visible = True
        self.update()
