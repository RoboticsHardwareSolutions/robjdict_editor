import flet as ft


class DevInfoPanel(ft.ResponsiveRow):
    def __init__(self, od):
        super().__init__()
        self.visible = True
        self.od = od

        # Define text fields with a helper method
        self.te_fields = {
            "product_name": self._create_text_field("Product Name", od.object_dictionary.device_information.product_name,),
            "product_number": self._create_text_field("Product Number", od.object_dictionary.device_information.product_number),
            "vendor_name": self._create_text_field("Vendor Name", od.object_dictionary.device_information.vendor_name),
            "vendor_number": self._create_text_field("Vendor Number", od.object_dictionary.device_information.vendor_number),
            "node_id": self._create_text_field("Node ID", od.id),
            "device_type": self._create_text_field("Device Type", od.object_dictionary[0x1000].default),
        }
        self.controls = [
            ft.Column(
                [self.te_fields["node_id"], self.te_fields["device_type"]],
                col={"sm": 6},
            ),
            ft.Column(
                [
                    self.te_fields["product_name"],
                    self.te_fields["product_number"],
                    self.te_fields["vendor_name"],
                    self.te_fields["vendor_number"],
                ],
                col={"sm": 6},
            ),
        ]

    def _create_text_field(self, label, value):
        def change(e):
            field_name = e.control.label.lower().replace(" ", "_")
            if field_name in self.te_fields:
                if field_name == "node_id":
                    self.od.id = e.control.value
                elif field_name == "device_type":
                    self.od.object_dictionary.get_variable(0x1000).default_raw = e.control.value
                    self.od.object_dictionary.get_variable(0x1000).default = e.control.value
                else:
                    setattr(self.od.object_dictionary.device_information, field_name, e.control.value)
        """Helper method to create a TextField."""
        return ft.TextField(label=label, value=value, on_change=change)
