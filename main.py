import flet as ft
from device_tab import DeviceTab
import os

os.environ["FLET_SECRET_KEY"] = os.urandom(12).hex()
UPLOAD_DIR = 'upload'

def main(page: ft.Page):
    page.title = "Objdict editor"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.min_height = 600
    page.window.height = 600
    page.window.min_width = 1000
    page.window.width = 1000
    progressbar = ft.ProgressBar(width=page.width, value=0, visible=False)

    def page_resize(e):
        for tab in devices.tabs:
            if isinstance(tab, DeviceTab):
                tab.life_communication.lv_consumer_hb.height = page.height - 200
                tab.sdo_communication.lv_sdo_client.height = page.height - 200
                tab.obj_dict.lv_obj.height = page.height - 200
            page.update()

    page.on_resized = page_resize

    devices = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        expand=1,
    )

    def button_delete(e):
        for device in devices.tabs:
            if device.uid == e.control.parent.parent.uid:
                devices.tabs.remove(device)
                page.update()

    # File picker
    def file_picker_result(e: ft.FilePickerResultEvent):
        if e.files is None:
            return
        files = []

        for file in e.files:
            files.append(
                ft.FilePickerUploadFile(
                    file.name,
                    upload_url=page.get_upload_url(file.name, 600)
                )
            )

        progressbar.visible = True
        file_picker_dialog.upload(files)
        
        for file in files:
            while not os.path.exists(f"{UPLOAD_DIR}/{file.name}") or progressbar.visible == True:
                pass
            btn = ft.IconButton(
                icon=ft.Icons.CLOSE,
                on_click=button_delete,
            )
            new_device = DeviceTab(f"{UPLOAD_DIR}/{file.name}", btn)
            devices.tabs.append(new_device)
            page.update()

    def file_picker_upload(e: ft.FilePickerUploadEvent):
        progressbar.value = e.progress
        page.update()
        if progressbar.value == 1:
            progressbar.visible = False
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

    # Create the top menu bar
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
        devices,
        progressbar
    )
    page.update()


ft.app(target=main, view=ft.WEB_BROWSER, port=8551, upload_dir=UPLOAD_DIR)
