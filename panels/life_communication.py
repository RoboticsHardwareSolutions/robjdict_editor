import canopen
import can
from can import Message
import flet as ft


class LifeCommunicationPanel(ft.ResponsiveRow):
    def __init__(self, od):
        super().__init__()
        self.te_prod_hb = ft.TextField(label="Producer Heartbeat Time, ms:",
                                       width=300,
                                       value=od.object_dictionary[0x1017].default)
        self.visible = False

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
                on_update=handle_update,
                on_confirm_dismiss=handle_confirm_dismiss,
                dismiss_thresholds={
                    ft.DismissDirection.END_TO_START: 0.2,
                    ft.DismissDirection.START_TO_END: 0.2,
                },
            )

        def handle_dlg_del_action_clicked(e):
            e.page.close(dlg_del)
            dlg_del.data.confirm_dismiss(e.control.data)

        dlg_del = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please confirm"),
            content=ft.Text("Do you really want to delete this item?"),
            actions=[
                ft.TextButton("Yes", data=True, on_click=handle_dlg_del_action_clicked),
                ft.TextButton("No", data=False, on_click=handle_dlg_del_action_clicked),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )

        def handle_dlg_add_action_clicked(e):
            e.page.close(dlg_add)
            dlg_add.data.controls.append(
                add_consumer_heartbeat("0x" + dlg_add.actions[0].value, dlg_add.actions[1].value))
            self.update()
            # dlg.data.confirm_dismiss(False)

        dlg_add = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please confirm"),
            content=ft.Text("Set new consumer heartbeat"),
            actions=[
                ft.TextField(
                    height=70,
                    label="Node ID, hex",
                    value="1"),
                ft.TextField(
                    height=70,
                    label="Time, ms",
                    value="1000"),
                ft.TextButton("OK", data=True, on_click=handle_dlg_add_action_clicked),
                ft.TextButton("Cancel", data=False, on_click=handle_dlg_add_action_clicked),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )

        def handle_confirm_dismiss(e: ft.DismissibleDismissEvent):
            if e.direction == ft.DismissDirection.END_TO_START:  # right-to-left slide
                # save current dismissible to dialog's data, for confirmation in handle_dlg_action_clicked
                dlg_del.data = e.control
                e.page.open(dlg_del)
            else:  # left-to-right slide
                dlg_add.data = e.control.parent
                e.page.open(dlg_add)
                e.control.confirm_dismiss(False)

        def handle_dismiss(e):
            print('on_dismiss')
            e.control.parent.controls.remove(e.control)
            self.update()

        def handle_update(e: ft.DismissibleUpdateEvent):
            print(
                f"Update - direction: {e.direction}, progress: {e.progress}, reached: {e.reached}, previous_reached: {e.previous_reached}"
            )

        self.list_view = ft.ListView(expand=1, spacing=10, padding=20, height=300, width=500)
        for item in od.object_dictionary[0x1016].values():
            if item.subindex != 0:
                self.list_view.controls.append(add_consumer_heartbeat(f'{hex((item.default >> 16) & 0xFF)}',
                                                                      f'{(item.default & 0xFFFF)}')
                                               )

        self.controls = [ft.Row([
            ft.Column([
                ft.Text("Consumer Heartbeat Time, ms"),
                self.list_view,
            ]),
            self.te_prod_hb,
        ])]
