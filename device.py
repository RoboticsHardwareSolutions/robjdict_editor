import os
import canopen
import can
from can import Message
import flet as ft


class CustomTab(ft.UserControl):
    CTRL_DEVICE_INFO = "Device info"
    CTRL_LIFE_COMMUNICATION = "Life communication"
    CTRL_SDO_COMMUNICATION = "SDO communication"
    CTRL_PDO_COMMUNICATION = "PDO communication"
    CTRL_OBJECT_DICTIONARY = "Object Dictionary"

    def __init__(self, path_to_od):
        super().__init__()
        self.path_to_od = path_to_od
        self.name_od = os.path.basename(path_to_od)
        self.cssb = ft.CupertinoSlidingSegmentedButton(
            selected_index=0,
            thumb_color=ft.colors.BLUE_400,
            on_change=self.__seg_btn,
            padding=ft.padding.symmetric(0, 10),
            controls=[
                ft.Text(self.CTRL_DEVICE_INFO),
                ft.Text(self.CTRL_LIFE_COMMUNICATION),
                ft.Text(self.CTRL_SDO_COMMUNICATION),
                ft.Text(self.CTRL_PDO_COMMUNICATION),
                ft.Text(self.CTRL_OBJECT_DICTIONARY),
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

        self.device_info_panel = ft.ResponsiveRow([
            ft.Column([
                self.t_node_id,
                self.te_node_id,
                self.t_dev_type,
                self.te_dev_type
            ],
                col={"sm": 6},
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
            ],
                col={"sm": 6}, ),
        ]
        )

        # Life communication
        self.life_communication_panel = ft.ResponsiveRow([
            ft.Text("TODO life_communication_panel")
        ],
            visible=False
        )

        # SDO communication
        # TODO
        self.t_prod_hb = ft.Text("Producer Heartbeat Time, ms:")
        self.te_prod_hb = ft.TextField(od.object_dictionary[0x1017].default)

        self.sdo_communication_panel = ft.ResponsiveRow([
            self.t_prod_hb,
            self.te_prod_hb
        ],
            visible=False
        )

        # PDO communication
        self.pdo_communication_panel = ft.ResponsiveRow([
            ft.Text("TODO pdo_communication_panel")
        ],
            visible=False
        )

        # Object Dictionary
        self.object_dictionary_panel = ft.ResponsiveRow([
            ft.Text("TODO object_dictionary_panel")
        ],
            visible=False
        )

        # Main panel
        self.info_column = ft.Column([
            self.cssb,
            self.device_info_panel,
            self.life_communication_panel,
            self.sdo_communication_panel,
            self.pdo_communication_panel,
            self.object_dictionary_panel
        ])

    def build(self):
        return self.info_column

    def __seg_btn(self, e):
        target_segment = e.control.controls[int(e.data)].value
        if target_segment == self.CTRL_DEVICE_INFO:
            self.device_info_panel.visible = True
            self.life_communication_panel.visible = False
            self.sdo_communication_panel.visible = False
            self.pdo_communication_panel.visible = False
            self.object_dictionary_panel.visible = False
        elif target_segment == self.CTRL_LIFE_COMMUNICATION:
            self.device_info_panel.visible = False
            self.life_communication_panel.visible = True
            self.sdo_communication_panel.visible = False
            self.pdo_communication_panel.visible = False
            self.object_dictionary_panel.visible = False
        elif target_segment == self.CTRL_SDO_COMMUNICATION:
            self.device_info_panel.visible = False
            self.life_communication_panel.visible = False
            self.sdo_communication_panel.visible = True
            self.pdo_communication_panel.visible = False
            self.object_dictionary_panel.visible = False
        elif target_segment == self.CTRL_PDO_COMMUNICATION:
            self.device_info_panel.visible = False
            self.life_communication_panel.visible = False
            self.sdo_communication_panel.visible = False
            self.pdo_communication_panel.visible = True
            self.object_dictionary_panel.visible = False
        elif target_segment == self.CTRL_OBJECT_DICTIONARY:
            self.device_info_panel.visible = False
            self.life_communication_panel.visible = False
            self.sdo_communication_panel.visible = False
            self.pdo_communication_panel.visible = False
            self.object_dictionary_panel.visible = True
        self.update()
