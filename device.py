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
                ft.Text("Life communication"),
                ft.Text("SDO communication"),
                ft.Text("PDO communication"),
                ft.Text("Object Dictionary"),
            ],
        )

        network = canopen.Network()
        od = network.add_node(1, object_dictionary=self.path_to_od)

        # Device info
        self.t_product_name = ft.Text("Vendor Name")
        self.te_product_name = ft.TextField(od.object_dictionary.device_information.product_name)
        self.t_product_number = ft.Text("Vendor Number")
        self.te_product_number = ft.TextField(od.object_dictionary.device_information.product_number)

        self.t_vendor_name = ft.Text("Vendor Name")
        self.te_vendor_name = ft.TextField(od.object_dictionary.device_information.vendor_name)
        self.t_vendor_number = ft.Text("Vendor Number")
        self.te_vendor_number = ft.TextField(od.object_dictionary.device_information.vendor_number)

        self.t_node_id = ft.Text("Node ID")
        self.te_node_id = ft.TextField(od.id)
        self.t_dev_type = ft.Text("Device Type")
        self.te_dev_type = ft.TextField(od.object_dictionary[0x1000].default)

        self.device_info_panel = ft.Row([
            ft.Column([
                self.t_node_id,
                self.te_node_id,
                self.t_dev_type,
                self.te_dev_type
            ],
            ),
            ft.Column([
                self.t_product_name,
                self.te_product_name,
                self.t_product_number,
                self.te_product_number,
                self.t_vendor_name,
                self.te_vendor_name,
                self.t_vendor_number,
                self.te_vendor_number,
            ]),
        ]
        )

        # Life communication
        # TODO

        # SDO communication
        # TODO
        self.t_prod_hb = ft.Text("Producer Heartbeat Time, ms:")
        self.te_prod_hb = ft.TextField(od.object_dictionary[0x1017].default)

        self.common_communication_panel = ft.Row([
            self.t_prod_hb,
            self.te_prod_hb
        ],
            visible=False
        )
        self.info_column = ft.Column([
            self.cssb,
            self.device_info_panel,
            self.common_communication_panel
        ])

        # PDO communication
        # TODO

        # Object Dictionary
        # TODO

    def build(self):
        return self.info_column

    def __seg_btm(self, e):
        if e.data == '0':
            self.device_info_panel.visible = True
            self.common_communication_panel.visible = False
        if e.data == '1':
            self.device_info_panel.visible = False
            self.common_communication_panel.visible = False
        self.update()
        if e.data == '2':
            self.device_info_panel.visible = False
            self.common_communication_panel.visible = True
        self.update()
        if e.data == '3':
            self.device_info_panel.visible = False
            self.common_communication_panel.visible = False
        self.update()
        if e.data == '4':
            self.device_info_panel.visible = False
            self.common_communication_panel.visible = False
        self.update()
