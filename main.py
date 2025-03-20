import flet as ft
from device_tab import DeviceTab
import os
import time

os.environ["FLET_SECRET_KEY"] = os.urandom(12).hex()
UPLOAD_DIR = 'upload'
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1000
TAB_HEIGHT_OFFSET = 200

def main(page: ft.Page):
    page.title = "Objdict editor"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.min_height = WINDOW_HEIGHT
    page.window.height = WINDOW_HEIGHT
    page.window.min_width = WINDOW_WIDTH
    page.window.width = WINDOW_WIDTH

    def page_resize(e):
        for tab in devices.tabs:
            if isinstance(tab, DeviceTab):
                tab.life_communication.lv_consumer_hb.height = page.height - TAB_HEIGHT_OFFSET
                tab.sdo_communication.lv_sdo_client.height = page.height - TAB_HEIGHT_OFFSET
                tab.obj_dict.lv_obj.height = page.height - TAB_HEIGHT_OFFSET
        page.update()

    page.on_resized = page_resize

    devices = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        expand=1,
    )

    def button_delete(e):
        devices.tabs = [device for device in devices.tabs if device.uid != e.control.parent.parent.uid]
        page.update()

    def file_picker_result(e: ft.FilePickerResultEvent):
        if e.files is None:
            return
        files = [
            ft.FilePickerUploadFile(
            file.name,
            upload_url=page.get_upload_url(file.name, 600)
            ) for file in e.files
        ]
        file_picker_dialog.upload(files)

    def file_picker_upload(e: ft.FilePickerUploadEvent):
        if e.progress == 1:
            btn = ft.IconButton(
                icon=ft.Icons.CLOSE,
                on_click=button_delete,
            )
            device_tab = DeviceTab(f"{UPLOAD_DIR}/{e.file_name}", btn)
            devices.tabs.append(device_tab)
        
        time.sleep(2) # flet's magic. app can to request a ui update even before completing the previous ui update request.
        page.update()

    file_picker_dialog = ft.FilePicker(
        on_result=file_picker_result, on_upload=file_picker_upload
    )
    page.overlay.append(file_picker_dialog)
    
    def save_od(e):
        try:
            device = devices.tabs[devices.selected_index - 1]
            if isinstance(device, DeviceTab):
                device.save_device()
        except IndexError:
            return

    menubar = ft.AppBar(
        title=ft.Text("Objdict editor"),
        actions=[
            ft.IconButton(ft.Icons.FILE_DOWNLOAD_OUTLINED,
                          on_click=lambda e: file_picker_dialog.pick_files(allow_multiple=True,
                                                                          allowed_extensions=["eds", "dcf", "epf"])),
            ft.IconButton(ft.Icons.SAVE, on_click=save_od),
        ]
    )
    page.add(
        menubar,
        devices
    )
    page.update()

ft.app(target=main, view=ft.WEB_BROWSER, port=8551, upload_dir=UPLOAD_DIR)
