import canopen
import can
from can import Message
import flet as ft


class LifeCommunicationPanel(ft.ResponsiveRow):
    def __init__(self, od):
        super().__init__()
        self.te_prod_hb = ft.TextField(label="Producer Heartbeat Time, ms:",
                                       width=300,
                                       value=od.object_dictionary.get_variable(0x1017, 0).default)
        self.visible = False

        def handle_confirm_dismiss(e: ft.DismissibleDismissEvent):
            if e.direction == ft.DismissDirection.END_TO_START:  # right-to-left slide
                # save current dismissible to dialog's data, for confirmation in handle_dlg_action_clicked
                if len(self.list_view.controls) == 1:
                    self.list_view.controls.append(
                        ft.TextButton("Add Consumer Heartbeat Time", data=True, on_click=start_chb))
                e.control.confirm_dismiss(True)
            else:  # left-to-right slide
                for item_diss in range(len(self.list_view.controls)):
                    if e.control.uid == self.list_view.controls[item_diss].uid:
                        self.list_view.controls.insert(item_diss + 1, add_consumer_heartbeat(f'{hex(0x01)}',
                                                                                             1000))

                e.control.confirm_dismiss(False)
                self.update()

        def handle_dismiss(e):
            print('on_dismiss')
            e.control.parent.controls.remove(e.control)
            self.update()

        def add_consumer_heartbeat(node_id, time):

            return ft.Dismissible(
                content=ft.Row([
                    ft.TextField(
                        width=200,
                        label="Node ID",
                        value=node_id),
                    ft.TextField(
                        width=200,
                        label="Time, ms",
                        value=time),
                ], ),
                dismiss_direction=ft.DismissDirection.HORIZONTAL,
                background=ft.Container(ft.Icon(ft.icons.ADD), bgcolor=ft.colors.GREEN,
                                        alignment=ft.alignment.center_left, padding=ft.padding.only(left=10)),
                secondary_background=ft.Container(ft.Icon(ft.icons.DELETE), bgcolor=ft.colors.RED,
                                                  alignment=ft.alignment.center_right,
                                                  padding=ft.padding.only(right=10)),
                on_dismiss=handle_dismiss,
                on_confirm_dismiss=handle_confirm_dismiss,
                dismiss_thresholds={
                    ft.DismissDirection.END_TO_START: 0.2,
                    ft.DismissDirection.START_TO_END: 0.2,
                },
            )

        self.list_view = ft.ListView(expand=1, spacing=10, padding=20, height=300, width=500)

        def start_chb(e):
            self.list_view.controls.clear()
            self.list_view.controls.append(add_consumer_heartbeat(f'{hex(0x01)}',
                                                                  f'{1000}'))
            self.update()

        if od.object_dictionary.get_variable(0x1016, 0) is not None:
            for item in range(od.object_dictionary.get_variable(0x1016, 0).default):
                data = od.object_dictionary.get_variable(0x1016, item + 1).default
                self.list_view.controls.append(add_consumer_heartbeat(f'{hex((data >> 16) & 0xFF)}',
                                                                      f'{(data & 0xFFFF)}')
                                               )
        else:
            self.list_view.controls.append(
                ft.TextButton("Add Consumer Heartbeat Time", data=True, on_click=start_chb))

        self.controls = [ft.Row([
            ft.Column([
                ft.Text("Consumer Heartbeat Time, ms"),
                self.list_view,
            ]),
            self.te_prod_hb,
        ])]

    def update_od(self, od):
        od.object_dictionary.get_variable(0x1017).default = self.te_prod_hb.value

        try:
            od.object_dictionary.__delitem__(0x1016)
        except:
            print("An exception occurred")

        od_cd = canopen.objectdictionary.ODArray("Consumer Heartbeat Time", 0x1016)

        var = canopen.objectdictionary.ODVariable("Number of Entries", 0x1016, 0)
        var.access_type = "ro"
        var.data_type = canopen.objectdictionary.datatypes.UNSIGNED8
        var.default = len(self.list_view.controls)
        od_cd.add_member(var)
        for item in range(len(self.list_view.controls)):
            var = canopen.objectdictionary.ODVariable("Consumer Heartbeat Time", 0x1016, item + 1)
            var.access_type = "rw"
            var.data_type = canopen.objectdictionary.datatypes.UNSIGNED32
            var.default = int(self.list_view.controls[item].content.controls[0].value, 16) << 16 | int(
                self.list_view.controls[item].content.controls[1].value)
            od_cd.add_member(var)

        od.object_dictionary.add_object(od_cd)

        return od
