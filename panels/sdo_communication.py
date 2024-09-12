import canopen
import can
from can import Message
import flet as ft


class SdoCommunicationPanel(ft.ResponsiveRow):
    def __init__(self, od):
        super().__init__()
        self.visible = False
        self.expand = True
        self.od = od

        self.sdo_server_tx = ft.TextField(label="COB ID Client to Server", value="$NODEID+0x600", col=2)
        self.sdo_server_rx = ft.TextField(label="COB ID Server to Client", value="$NODEID+0x580", col=2)

        self.lv_sdo_client = ft.ListView(expand=1, spacing=10, padding=20, height=400, col=8)

        def start_chb(e):
            self.lv_sdo_client.controls.clear()
            self.lv_sdo_client.controls.append(add_consumer_heartbeat(f'{hex(0x01)}',
                                                                      f'{1000}'))
            self.update()

        self.__add_btn = ft.TextButton("Add Consumer Heartbeat Time", data=True, col=8, on_click=start_chb)
        self.lv_sdo_client.controls.append(self.__add_btn)

        def button_add(e):
            for item_diss in range(len(self.lv_sdo_client.controls)):
                if e.control.parent.parent.uid == self.lv_sdo_client.controls[item_diss].uid:
                    self.lv_sdo_client.controls.insert(item_diss + 1, add_consumer_heartbeat(f'{hex(0x01)}',
                                                                                             1000))
            self.update()

        def button_delete(e):
            item_delete = 0
            for item_diss in range(len(self.lv_sdo_client.controls)):
                if e.control.parent.parent.uid == self.lv_sdo_client.controls[item_diss].uid:
                    item_delete = item_diss
            self.lv_sdo_client.controls.remove(self.lv_sdo_client.controls[item_delete])
            if len(self.lv_sdo_client.controls) == 0:
                self.lv_sdo_client.controls.append(self.__add_btn)
            self.update()

        def add_consumer_heartbeat(node_id, time):
            return ft.Container(
                content=ft.ResponsiveRow([
                    ft.TextField(
                        label="COB ID Client to Server",
                        col=2,
                        value=node_id),
                    ft.TextField(
                        label="COB ID Server to Client",
                        col=4,
                        value=time),
                    ft.TextField(
                        label="Node ID of the SDO Server",
                        col=4,
                        value=time),
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

        self.container_cli = ft.Container()
        self.controls = [
            ft.ResponsiveRow(
                [
                    ft.Container(
                        ft.Text("SDO Client"),
                        bgcolor=ft.colors.YELLOW,
                        col=4,
                    ),
                    ft.Container(
                        ft.Text("SDO Server"),
                        bgcolor=ft.colors.GREEN,
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
