import canopen
import can
from can import Message
import flet as ft
from flet_core import ButtonStyle


class ObjectDictionaryField(ft.ElevatedButton):
    def __init__(self, index, subindex, name, on_click):
        super().__init__()
        self.index = index
        self.subindex = subindex
        self.name = name
        self.text = f'0x{index:04X} 0x{subindex:02X} {name}'


class ObjDictPanel(ft.ResponsiveRow):
    def __init__(self, od):
        super().__init__()
        self.visible = False
        self.__lv_od = ft.ListView(expand=1, spacing=10, padding=20, height=400, col=4)
        self.__settings_conteiner = ft.Container

        def __settings_field(e):
            self.update()

        for obj in od.object_dictionary.values():
            if isinstance(obj, (
            canopen.objectdictionary.ODRecord, canopen.objectdictionary.ODArray, canopen.objectdictionary.ODVariable)):
                for subobj in obj.values():
                    btn = ObjectDictionaryField(obj.index, subobj.subindex, obj.name, __settings_field)
                    self.__lv_od.controls.append(btn)

        self.controls = [
            self.__lv_od
        ]
