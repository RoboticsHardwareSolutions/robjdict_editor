import flet as ft
import device

list_of_devices = []


def main(page: ft.Page):
    page.title = "Objdictedit - ObjDict"
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
            new_device = device.CustomTab(new_tab)
            list_of_devices.append(new_device)
            tab = ft.Tab(text=new_device.name_od, content=new_device)
            devices.tabs.append(tab)
            page.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)

    # Create the top menu bar
    menubar = ft.AppBar(
        title=ft.Text("Objdictedit - ObjDict"),
        actions=[
            ft.IconButton(ft.icons.FILE_DOWNLOAD_OUTLINED,
                          on_click=lambda e: pick_files_dialog.pick_files(allow_multiple=True,
                                                                          allowed_extensions=["eds", "dcf", "epf"])),
            ft.IconButton(ft.icons.EDIT, on_click=lambda e: print("Edit")),
            ft.IconButton(ft.icons.ADD_CIRCLE_OUTLINE, on_click=lambda e: print("Add")),
            ft.IconButton(ft.icons.HELP, on_click=lambda e: print("Help")),
        ]
    )
    page.add(menubar)
    page.update()


ft.app(target=main)
