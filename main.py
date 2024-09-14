import flet as ft
from device_tab import DeviceTab


def main(page: ft.Page):
    page.title = "Objdict editor"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.min_height = 600
    page.window.height = 600
    page.window.min_width = 1000
    page.window.width = 1000

    def page_resize(e):
        for tab in devices.tabs:
            tab.life_communication.lv_consumer_hb.height = page.height - 200
            tab.sdo_communication.lv_sdo_client.height = page.height - 200
            page.update()

    page.on_resized = page_resize

    devices = ft.Tabs(
        selected_index=1,
        animation_duration=300,
        expand=1,
    )

    def button_delete(e):
        for device in devices.tabs:
            if device.uid == e.control.parent.parent.uid:
                devices.tabs.remove(device)
                page.update()

    # File picker
    def pick_files_result(e: ft.FilePickerResultEvent):
        names_new_tabs = list(map(lambda f: f.path, e.files))
        for new_tab in names_new_tabs:
            btn = ft.IconButton(
                icon=ft.icons.CLOSE,
                on_click=button_delete,
            )
            new_device = DeviceTab(new_tab, btn)
            devices.tabs.append(new_device)
            page.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)

    def save_od(e):
        device = devices.tabs[devices.selected_index - 1]
        device.save_device()

    # Create the top menu bar
    menubar = ft.AppBar(
        title=ft.Text("Objdict editor"),
        actions=[
            ft.IconButton(ft.icons.FILE_DOWNLOAD_OUTLINED,
                          on_click=lambda e: pick_files_dialog.pick_files(allow_multiple=True,
                                                                          allowed_extensions=["eds", "dcf", "epf"])),
            ft.IconButton(ft.icons.SAVE, on_click=save_od),
        ]
    )
    page.add(
        menubar,
        devices
    )
    page.update()


ft.app(target=main)
