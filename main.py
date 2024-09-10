import flet as ft
from device_tab import DeviceTab

list_of_devices = []


def main(page: ft.Page):
    page.title = "Objdict editor"
    page.theme_mode = ft.ThemeMode.LIGHT

    devices = ft.Tabs(
        selected_index=1,
        animation_duration=300,
        expand=1,
    )
    page.add(devices)

    # File picker
    def pick_files_result(e: ft.FilePickerResultEvent):
        names_new_tabs = list(map(lambda f: f.path, e.files))
        for new_tab in names_new_tabs:
            new_device = DeviceTab(new_tab)
            list_of_devices.append(new_device)
            devices.tabs.append(new_device)
            page.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)

    def save_od(e):
        device = list_of_devices[devices.selected_index - 1]
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
    page.add(menubar)
    page.update()


ft.app(target=main)
