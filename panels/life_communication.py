import canopen
import can
from can import Message
import flet as ft


class LifeCommunicationPanel(ft.ResponsiveRow):
    def __init__(self, od):
        super().__init__()
        self.t_prod_hb = ft.Text("Producer Heartbeat Time, ms:")
        self.te_prod_hb = ft.TextField(od.object_dictionary[0x1017].default)
        self.visible = False

        def handle_dlg_action_clicked(e):
            e.page.close(dlg)
            dlg.data.confirm_dismiss(e.control.data)

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please confirm"),
            content=ft.Text("Do you really want to delete this item?"),
            actions=[
                ft.TextButton("Yes", data=True, on_click=handle_dlg_action_clicked),
                ft.TextButton("No", data=False, on_click=handle_dlg_action_clicked),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )

        def handle_dlg1_action_clicked(e):
            e.page.close(dlg1)
            dlg1.data.controls.append(ft.Text("1234567890"))
            self.update()
            # dlg.data.confirm_dismiss(False)

        dlg1 = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please confirm"),
            content=ft.Text("Do you really want to delete this item?"),
            actions=[
                ft.TextButton("Yes", data=True, on_click=handle_dlg1_action_clicked),
                ft.TextButton("No", data=False, on_click=handle_dlg1_action_clicked),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )

        def handle_confirm_dismiss(e: ft.DismissibleDismissEvent):
            if e.direction == ft.DismissDirection.END_TO_START:  # right-to-left slide
                # save current dismissible to dialog's data, for confirmation in handle_dlg_action_clicked
                dlg.data = e.control
                e.page.open(dlg)
            else:  # left-to-right slide
                dlg1.data = e.control.parent
                e.page.open(dlg1)
                e.control.confirm_dismiss(False)

        def handle_dismiss(e):
            print('on_dismiss')
            e.control.parent.controls.remove(e.control)
            self.update()

        def handle_update(e: ft.DismissibleUpdateEvent):
            print(
                f"Update - direction: {e.direction}, progress: {e.progress}, reached: {e.reached}, previous_reached: {e.previous_reached}"
            )

        list_view = ft.ListView(expand=1, height=300, width=500)
        for item in od.object_dictionary[0x1016].values():
            if item.subindex != 0:
                list_view.controls.append(
                    ft.Dismissible(
                        content=
                        ft.Row([
                            ft.Text(f'{hex((item.default >> 16) & 0xFF)}'),
                            ft.TextField(f'{(item.default & 0xFFFF)}'),
                        ], ),
                        dismiss_direction=ft.DismissDirection.HORIZONTAL,
                        background=ft.Container(bgcolor=ft.colors.GREEN),
                        secondary_background=ft.Container(bgcolor=ft.colors.RED),
                        on_dismiss=handle_dismiss,
                        on_update=handle_update,
                        on_confirm_dismiss=handle_confirm_dismiss,
                        dismiss_thresholds={
                            ft.DismissDirection.END_TO_START: 0.2,
                            ft.DismissDirection.START_TO_END: 0.2,
                        },
                    )
                )
            else:
                print("q12345t")

        self.controls = [ft.Column([
            self.t_prod_hb,
            self.te_prod_hb,
            list_view,
        ])]
