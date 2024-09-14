import canopen
import can
from can import Message
import flet as ft


class SdoCommunicationPanel(ft.ResponsiveRow):
    def __init__(self, od):
        super().__init__()
        self.visible = False
        self.expand = True

        self.tf_sdo_server_tx = ft.TextField(label="COB ID Tx SDO", value="0x580", col=2)
        self.tf_sdo_server_rx = ft.TextField(label="COB ID Rx SDO", value="0x600", col=2)

        self.lv_sdo_client = ft.ListView(expand=1, spacing=10, padding=20, height=400, col=8)
        self.t_sdo_client = ft.Text("SDO Client")

        def button_first_sdo_cli(e):
            self.lv_sdo_client.controls.clear()
            self.lv_sdo_client.controls.append(add_consumer_heartbeat(f'{hex(0x01)}', f'{hex(0x601)}', f'{hex(0x581)}'))
            self.t_sdo_client.value = "SDO Client :" + str(len(self.lv_sdo_client.controls))
            self.update()

        self.__add_btn = ft.TextButton("Add Consumer Heartbeat Time", data=True, col=8, on_click=button_first_sdo_cli)

        def button_add(e):
            for item_diss in range(len(self.lv_sdo_client.controls)):
                objs = self.lv_sdo_client.controls
                if e.control.parent.parent.uid == objs[item_diss].uid:
                    if int(objs[item_diss].content.controls[0].value, 16) == 0x7f:
                        new_id = 0x7f
                    else:
                        new_id = int(objs[item_diss].content.controls[0].value, 16) + 1

                    self.lv_sdo_client.auto_scroll = False
                    try:
                        next_obj = objs[item_diss + 1]
                        if int(next_obj.content.controls[0].value, 16) == new_id:
                            self.lv_sdo_client.auto_scroll = True
                            new_id = 0x7f
                            objs.append(add_consumer_heartbeat(f'{hex(new_id)}', f'{hex(new_id + 0x600)}',
                                                               f'{hex(new_id + 0x580)}'))
                        else:
                            objs.insert(item_diss + 1,
                                        add_consumer_heartbeat(f'{hex(new_id)}', f'{hex(new_id + 0x600)}',
                                                               f'{hex(new_id + 0x580)}'))

                    except IndexError:
                        objs.insert(item_diss + 1,
                                    add_consumer_heartbeat(f'{hex(new_id)}', f'{hex(new_id + 0x600)}',
                                                           f'{hex(new_id + 0x580)}'))

                self.t_sdo_client.value = "SDO Client :" + str(len(self.lv_sdo_client.controls))
            self.update()

        def button_delete(e):
            item_delete = 0
            for item_diss in range(len(self.lv_sdo_client.controls)):
                if e.control.parent.parent.uid == self.lv_sdo_client.controls[item_diss].uid:
                    item_delete = item_diss
            self.lv_sdo_client.controls.remove(self.lv_sdo_client.controls[item_delete])
            self.t_sdo_client.value = "SDO Client :" + str(len(self.lv_sdo_client.controls))
            if len(self.lv_sdo_client.controls) == 0:
                self.lv_sdo_client.controls.append(self.__add_btn)
            self.update()

        def add_consumer_heartbeat(node_id, tx_cobid, rx_cobid):
            return ft.Container(
                content=ft.ResponsiveRow([
                    ft.TextField(
                        label="Node ID",
                        col=2,
                        value=node_id),
                    ft.TextField(
                        label="COB ID Tx SDO",
                        col=4,
                        value=tx_cobid),
                    ft.TextField(
                        label="COB ID Rx SDO",
                        col=4,
                        value=rx_cobid),
                    ft.IconButton(
                        icon=ft.icons.ADD,
                        icon_color="blue400",
                        tooltip="Add",
                        on_click=button_add,
                        col=1
                    ),
                    ft.IconButton(
                        icon=ft.icons.DELETE,
                        icon_color="pink600",
                        tooltip="Delete",
                        on_click=button_delete,
                        col=1
                    ),
                ], ),
            )

        for index_cli_sdo in range(int(hex(0x1280), 16), int(hex(0x12FF), 16)):
            if od.object_dictionary.get_variable(index_cli_sdo) is not None:
                tx = od.object_dictionary.get_variable(index_cli_sdo, 1).default
                rx = od.object_dictionary.get_variable(index_cli_sdo, 2).default
                node_id = od.object_dictionary.get_variable(index_cli_sdo, 3).default
                self.lv_sdo_client.controls.append(
                    add_consumer_heartbeat(f'{hex(node_id)}', f'{hex(tx)}', f'{hex(rx)}'))
            else:
                break
        if len(self.lv_sdo_client.controls) == 0:
            self.lv_sdo_client.controls.append(self.__add_btn)

        self.controls = [
            ft.ResponsiveRow(
                [
                    ft.Container(
                        ft.Text("SDO Server"),
                        col=4,
                    ),
                    ft.Container(
                        self.t_sdo_client,
                        col=8,
                    ),
                ],
            ),
            ft.ResponsiveRow(
                [
                    self.tf_sdo_server_tx,
                    self.tf_sdo_server_rx,
                    self.lv_sdo_client,
                ],
            ),
        ]

    def update_od(self, od):
        # Save Server SDO
        od.object_dictionary.get_variable(0x1200, 1).default = self.tf_sdo_server_rx.value
        od.object_dictionary.get_variable(0x1200, 2).default = self.tf_sdo_server_tx.value

        # Save Client SDO
        ## clear old
        index = 0x1280
        while od.object_dictionary.get_variable(index) is not None:
            od.object_dictionary.__delitem__(index)
            index += 1

        if self.lv_sdo_client.controls[0].content is not None:
            for item in range(len(self.lv_sdo_client.controls)):
                od_cli_sdo = canopen.objectdictionary.ODArray(f'Client SDO {item + 1} Parameter', 0x1280 + item)
                var = canopen.objectdictionary.ODVariable("Number of Entries", 0x1280 + item, 0)
                var.access_type = "ro"
                var.data_type = canopen.objectdictionary.datatypes.UNSIGNED8
                var.default = 3
                od_cli_sdo.add_member(var)

                var = canopen.objectdictionary.ODVariable("COB ID Client to Server (Transmit SDO)", 0x1280 + item, 1)
                var.access_type = "rw"
                var.data_type = canopen.objectdictionary.datatypes.UNSIGNED32
                var.default = int(self.lv_sdo_client.controls[item].content.controls[1].value, 16)
                od_cli_sdo.add_member(var)

                var = canopen.objectdictionary.ODVariable("COB ID Server to Client (Receive SDO)", 0x1280 + item, 2)
                var.access_type = "rw"
                var.data_type = canopen.objectdictionary.datatypes.UNSIGNED32
                var.default = int(self.lv_sdo_client.controls[item].content.controls[2].value, 16)
                od_cli_sdo.add_member(var)

                var = canopen.objectdictionary.ODVariable("Node ID of the SDO Server", 0x1280 + item, 3)
                var.access_type = "rw"
                var.data_type = canopen.objectdictionary.datatypes.UNSIGNED8
                var.default = int(self.lv_sdo_client.controls[item].content.controls[0].value, 16)
                od_cli_sdo.add_member(var)
                od.object_dictionary.add_object(od_cli_sdo)

        return od
