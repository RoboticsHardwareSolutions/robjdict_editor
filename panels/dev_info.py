import canopen
import can
from can import Message
import flet as ft


class DevInfoPanel(ft.ResponsiveRow):
    def __init__(self, od):
        super().__init__()
        self.visible = True
        self.te_product_name = ft.TextField(label="Vendor Name",
                                            value=od.object_dictionary.device_information.product_name)
        self.te_product_number = ft.TextField(label="Vendor Number",
                                              value=od.object_dictionary.device_information.product_number)

        self.te_vendor_name = ft.TextField(label="Vendor Name",
                                           value=od.object_dictionary.device_information.vendor_name)
        self.te_vendor_number = ft.TextField(label="Vendor Number",
                                             value=od.object_dictionary.device_information.vendor_number)

        self.te_node_id = ft.TextField(label="Node ID", value=od.id)
        self.te_dev_type = ft.TextField(label="Device Type", value=od.object_dictionary[0x1000].default)

        self.controls = [
            ft.Column([
                self.te_node_id,
                self.te_dev_type
            ],
                col={"sm": 6},
            ),
            ft.Column([
                self.te_product_name,
                self.te_product_number,
                self.te_vendor_name,
                self.te_vendor_number,
            ],
                col={"sm": 6}, ),
        ]

    def update_od(self, od):
        od.object_dictionary.device_information.product_name = self.te_product_name.value
        od.object_dictionary.device_information.product_number = self.te_product_number.value
        od.object_dictionary.device_information.vendor_name = self.te_vendor_name.value
        od.object_dictionary.device_information.vendor_number = self.te_vendor_number.value

        od.id = self.te_node_id.value
        od.object_dictionary[0x1000].default = self.te_dev_type.value

        return od
