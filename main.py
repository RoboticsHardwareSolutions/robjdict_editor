import flet as ft
from device_tab import DeviceTab
import os
import time

# Constants
os.environ["FLET_SECRET_KEY"] = os.urandom(12).hex()
UPLOAD_DIR = 'upload'
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1000
TAB_HEIGHT_OFFSET = 200

def main(page: ft.Page):
    # Page setup
    page.title = "Objdict editor"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.min_height = page.window.height = WINDOW_HEIGHT
    page.window.min_width = page.window.width = WINDOW_WIDTH

    # Tabs container
    devices = ft.Tabs(selected_index=0, animation_duration=300, expand=1)

    # Resize handler
    def page_resize(e):
        for tab in devices.tabs:
            if isinstance(tab, DeviceTab):
                height = page.height - TAB_HEIGHT_OFFSET
                tab.life_communication.lv_consumer_hb.height = height
                tab.sdo_communication.lv_sdo_client.height = height
                tab.obj_dict.lv_obj.height = height
        page.update()

    page.on_resized = page_resize

    # Delete button handler
    def button_delete(e):
        devices.tabs = [device for device in devices.tabs if device.uid != e.control.parent.parent.uid]
        page.update()

    # File picker handlers
    def file_picker_result(e: ft.FilePickerResultEvent):
        if e.files:
            files = [
                ft.FilePickerUploadFile(
                    file.name,
                    upload_url=page.get_upload_url(file.name, 600)
                ) for file in e.files
            ]
            file_picker_dialog.upload(files)

    def file_picker_upload(e: ft.FilePickerUploadEvent):
        if e.progress == 1:
            device_tab = DeviceTab(f"{UPLOAD_DIR}/{e.file_name}", ft.IconButton(icon=ft.Icons.CLOSE, on_click=button_delete))
            devices.tabs.append(device_tab)
            time.sleep(2)  # Ensures UI update consistency
            page.update()

    # File picker dialog
    file_picker_dialog = ft.FilePicker(on_result=file_picker_result, on_upload=file_picker_upload)
    page.overlay.append(file_picker_dialog)

    # Save handler
    def save_od(e):
        try:
            device = devices.tabs[devices.selected_index - 1]
            if isinstance(device, DeviceTab):
                device.save_device()
        except IndexError:
            pass

    # Menubar
    menubar = ft.AppBar(
        title=ft.Text("Objdict editor"),
        actions=[
            ft.IconButton(
                ft.Icons.FILE_DOWNLOAD_OUTLINED,
                on_click=lambda e: file_picker_dialog.pick_files(
                    allow_multiple=True, allowed_extensions=["eds", "dcf", "epf"]
                )
            ),
            ft.IconButton(ft.Icons.SAVE, on_click=save_od),
        ]
    )

    # Add components to the page
    page.add(menubar, devices)
    page.update()

ft.app(target=main, view=ft.WEB_BROWSER, port=8551, upload_dir=UPLOAD_DIR)
