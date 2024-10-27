import canopen
import can
from can import Message
import flet as ft
from flet_core import ButtonStyle


class ObjectDictionaryField(ft.ExpansionPanel):
    def __init__(self, obj):
        super().__init__()
        self.__obj = obj
        self.index = obj.index
        self.name = obj.name
        self.header = ft.ListTile(title=ft.Text(f'0x{self.index:04X} {self.name}'))
        self.can_tap_header = True

        if isinstance(obj, canopen.objectdictionary.ODRecord):
            self.content = ft.Column()
            for subobj in obj.values():
                lt = ft.ListTile(
                    title=ft.Text(f"0x{subobj.subindex:02X} {subobj.name}"),
                    # subtitle=ft.Text(f"Press the icon to delete panel"),
                    # trailing=ft.IconButton(ft.icons.DELETE, on_click=handle_delete, data=exp),
                )
                self.content.controls.append(lt)
        if isinstance(obj, canopen.objectdictionary.ODArray):
            self.content = ft.Column()
            for subobj in obj.values():
                lt = ft.ListTile(
                    title=ft.Text(f"0x{subobj.subindex:02X} {subobj.name}"),
                    # subtitle=ft.Text(f"Press the icon to delete panel"),
                    # trailing=ft.IconButton(ft.icons.DELETE, on_click=handle_delete, data=exp),
                )
                self.content.controls.append(lt)
        if isinstance(obj, canopen.objectdictionary.ODVariable):
            self.content = ft.Column()
            lt = ft.ListTile(
                title=ft.Text(f"0x{obj.subindex:02X} {obj.name}"),
                # subtitle=ft.Text(f"Press the icon to delete panel"),
                # trailing=ft.IconButton(ft.icons.DELETE, on_click=handle_delete, data=exp),
            )
            self.content.controls.append(lt)

    def get_object(self):
        return self.__obj


class ObjDictPanel(ft.ResponsiveRow):
    def __init__(self, od):
        super().__init__()
        self.visible = False
        self.lv_obj = ft.ListView(expand=1, spacing=10, padding=20, height=400, col=4)

        def handle_change(e: ft.ControlEvent):
            i = int(e.data)
            print(f"change on panel with index {i}")
            target = self.__panel.controls[i].get_object()
            print(f"target: {target.name}")

        self.__panel = ft.ExpansionPanelList(
            expand_icon_color=ft.colors.AMBER,
            col=4,
            elevation=8,
            divider_color=ft.colors.AMBER,
            on_change=handle_change,
        )

        for obj in od.object_dictionary.values():
            index = ObjectDictionaryField(obj)
            self.__panel.controls.append(index)
        self.lv_obj.controls.append(self.__panel)

        self.controls = [

            ft.ResponsiveRow(
                [
                    ft.Container(
                        self.lv_obj,
                        col=4,
                    ),
                ],
            ),
        ]
