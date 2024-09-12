import canopen
import can
from can import Message
import flet as ft


class SdoCommunicationPanel(ft.ResponsiveRow):
    def __init__(self, od):
        super().__init__()
        self.visible = False
        self.expand = True

        self.sdo_server_tx = ft.TextField(label="COB ID Rx SDO", value="0x600", col=2)
        self.sdo_server_rx = ft.TextField(label="COB ID Tx SDO", value="0x580", col=2)

        self.lv_sdo_client = ft.ListView(expand=1, spacing=10, padding=20, height=400, col=8)
        self.t_sdo_client = ft.Text("SDO Client")

        def button_first_sdo_cli(e):
            self.lv_sdo_client.controls.clear()
            self.lv_sdo_client.controls.append(add_consumer_heartbeat(f'{hex(0x01)}', f'{hex(0x01)}', f'{hex(0x01)}'))
            self.t_sdo_client.value = "SDO Client :" + str(len(self.lv_sdo_client.controls))
            self.update()

        self.__add_btn = ft.TextButton("Add Consumer Heartbeat Time", data=True, col=8, on_click=button_first_sdo_cli)

        def button_add(e):
            for item_diss in range(len(self.lv_sdo_client.controls)):
                objs = self.lv_sdo_client.controls
                if e.control.parent.parent.uid == objs[item_diss].uid:
                    id = int(objs[item_diss].content.controls[0].value, 16) + 1
                    objs.insert(item_diss + 1,
                                add_consumer_heartbeat(f'{hex(id)}', f'{hex(id + 0x600)}', f'{hex(id + 0x580)}'))
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
                    self.sdo_server_tx,
                    self.sdo_server_rx,
                    self.lv_sdo_client,
                ],
            ),
        ]

    def update_od(self, od):
        return od
