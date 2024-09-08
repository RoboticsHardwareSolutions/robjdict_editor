import canopen
import can
from can import Message
import flet as ft


class DevInfoPanel(ft.ResponsiveRow):
    def __init__(self, od):
        super().__init__()
        self.visible = True
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

        self.controls = [
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
