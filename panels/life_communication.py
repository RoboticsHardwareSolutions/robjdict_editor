import canopen
import can
from can import Message
import flet as ft


class LifeCommunicationPanel(ft.ResponsiveRow):
    def __init__(self, od):
        super().__init__()
        self.visible = False
        self.expand = True

        self.te_prod_hb = ft.TextField(label="Time, ms:",
                                       col=4,
                                       value=od.object_dictionary.get_variable(0x1017, 0).default)
        self.lv_consumer_hb = ft.ListView(expand=1, spacing=10, padding=20, height=400, col=8)
        self.t_consumer_hb = ft.Text("Consumer Heartbeat")

        def start_chb(e):
            self.lv_consumer_hb.controls.clear()
            self.lv_consumer_hb.controls.append(add_consumer_heartbeat(f'{hex(0x01)}', f'{1000}'))
            self.t_consumer_hb.value = "Consumer Heartbeat :" + str(len(self.lv_consumer_hb.controls))
            self.update()

        self.__btn_first_chb = ft.TextButton("Add Consumer Heartbeat Time", data=True, col=8, on_click=start_chb)

        def button_add(e):
            for item_diss in range(len(self.lv_consumer_hb.controls)):
                objs = self.lv_consumer_hb.controls
                if e.control.parent.parent.uid == objs[item_diss].uid:  # found target obj
                    if int(objs[item_diss].content.controls[0].value, 16) == 0x7f:
                        new_id = 0x7f
                    else:
                        new_id = int(objs[item_diss].content.controls[0].value, 16) + 1
                    self.lv_consumer_hb.auto_scroll = False
                    try:
                        next_obj = objs[item_diss + 1]
                        if int(next_obj.content.controls[0].value, 16) == new_id:
                            self.lv_consumer_hb.auto_scroll = True
                            new_id = 0x7f
                            objs.append(add_consumer_heartbeat(f'{hex(new_id)}', 1000))
                        else:
                            objs.insert(item_diss + 1, add_consumer_heartbeat(f'{hex(new_id)}', 1000))
                    except IndexError:
                        objs.insert(item_diss + 1, add_consumer_heartbeat(f'{hex(new_id)}', 1000))
                self.t_consumer_hb.value = "Consumer Heartbeat :" + str(len(self.lv_consumer_hb.controls))
            self.update()

        def button_delete(e):
            item_delete = 0
            for item_diss in range(len(self.lv_consumer_hb.controls)):
                if e.control.parent.parent.uid == self.lv_consumer_hb.controls[item_diss].uid:
                    item_delete = item_diss
            self.lv_consumer_hb.controls.remove(self.lv_consumer_hb.controls[item_delete])
            self.t_consumer_hb.value = "Consumer Heartbeat :" + str(len(self.lv_consumer_hb.controls))
            if len(self.lv_consumer_hb.controls) == 0:
                self.lv_consumer_hb.controls.append(self.__btn_first_chb)
            self.update()

        def add_consumer_heartbeat(node_id, time):
            return ft.Container(
                content=ft.ResponsiveRow([
                    ft.TextField(
                        label="Node ID",
                        col=5,
                        value=node_id),
                    ft.TextField(
                        label="Time, ms",
                        col=5,
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

        if od.object_dictionary.get_variable(0x1016, 0) is not None:
            for item in range(od.object_dictionary.get_variable(0x1016, 0).default):
                data = od.object_dictionary.get_variable(0x1016, item + 1).default
                self.lv_consumer_hb.controls.append(add_consumer_heartbeat(f'{hex((data >> 16) & 0xFF)}',
                                                                           f'{(data & 0xFFFF)}')
                                                    )
            self.t_consumer_hb.value = "Consumer Heartbeat :" + str(len(self.lv_consumer_hb.controls))
        else:
            self.lv_consumer_hb.controls.append(self.__btn_first_chb)

        self.controls = [
            ft.ResponsiveRow(
                [
                    ft.Container(
                        ft.Text("Producer Heartbeat"),
                        col=4,
                    ),
                    ft.Container(
                        self.t_consumer_hb,
                        col=8,
                    ),
                ],
            ),

            ft.ResponsiveRow(
                [
                    self.te_prod_hb,
                    self.lv_consumer_hb,
                ],
            ),
        ]

    def update_od(self, od):
        # Save Producer Heartbeat Time
        od.object_dictionary.get_variable(0x1017).default = self.te_prod_hb.value

        # Save Consumer Heartbeat Time
        ## clear old times
        try:
            od.object_dictionary.__delitem__(0x1016)
        except:
            print("An exception occurred")

        ## update OD
        if self.lv_consumer_hb.controls[0].content is not None:
            od_cd = canopen.objectdictionary.ODArray("Consumer Heartbeat Time", 0x1016)

            var = canopen.objectdictionary.ODVariable("Number of Entries", 0x1016, 0)
            var.access_type = "ro"
            var.data_type = canopen.objectdictionary.datatypes.UNSIGNED8
            var.default = len(self.lv_consumer_hb.controls)
            od_cd.add_member(var)
            for item in range(len(self.lv_consumer_hb.controls)):
                var = canopen.objectdictionary.ODVariable("Consumer Heartbeat Time", 0x1016, item + 1)
                var.access_type = "rw"
                var.data_type = canopen.objectdictionary.datatypes.UNSIGNED32
                var.default = int(self.lv_consumer_hb.controls[item].content.controls[0].value, 16) << 16 | int(
                    self.lv_consumer_hb.controls[item].content.controls[1].value)
                od_cd.add_member(var)

            od.object_dictionary.add_object(od_cd)

        return od
