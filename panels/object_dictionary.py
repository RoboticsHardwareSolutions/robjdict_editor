import canopen
import can
from can import Message
import flet as ft
from flet_core import ButtonStyle

data_type_map = {
    canopen.objectdictionary.BOOLEAN: "BOOLEAN",
    canopen.objectdictionary.INTEGER8: "INTEGER8",
    canopen.objectdictionary.INTEGER16: "INTEGER16",
    canopen.objectdictionary.INTEGER32: "INTEGER32",
    canopen.objectdictionary.UNSIGNED8: "UNSIGNED8",
    canopen.objectdictionary.UNSIGNED16: "UNSIGNED16",
    canopen.objectdictionary.UNSIGNED32: "UNSIGNED32",
    canopen.objectdictionary.REAL32: "REAL32",
    canopen.objectdictionary.VISIBLE_STRING: "VISIBLE_STRING",
    canopen.objectdictionary.OCTET_STRING: "OCTET_STRING",
    canopen.objectdictionary.UNICODE_STRING: "UNICODE_STRING",
    canopen.objectdictionary.TIME_OF_DAY: "TIME_OF_DAY",
    canopen.objectdictionary.TIME_DIFFERENCE: "TIME_DIFFERENCE",
    canopen.objectdictionary.DOMAIN: "DOMAIN",
    canopen.objectdictionary.INTEGER24: "INTEGER24",
    canopen.objectdictionary.REAL64: "REAL64",
    canopen.objectdictionary.INTEGER40: "INTEGER40",
    canopen.objectdictionary.INTEGER48: "INTEGER48",
    canopen.objectdictionary.INTEGER56: "INTEGER56",
    canopen.objectdictionary.INTEGER64: "INTEGER64",
    canopen.objectdictionary.UNSIGNED24: "UNSIGNED24",
    canopen.objectdictionary.UNSIGNED40: "UNSIGNED40",
    canopen.objectdictionary.UNSIGNED48: "UNSIGNED48",
    canopen.objectdictionary.UNSIGNED56: "UNSIGNED56",
    canopen.objectdictionary.UNSIGNED64: "UNSIGNED64",
    canopen.objectdictionary.PDO_COMMUNICATION_PARAMETER: "PDO_COMMUNICATION_PARAMETER",
    canopen.objectdictionary.PDO_MAPPING: "PDO_MAPPING",
    canopen.objectdictionary.SDO_PARAMETER: "SDO_PARAMETER",
    canopen.objectdictionary.IDENTITY: "IDENTITY",
}


class ObjectDictionaryField(ft.ExpansionPanel):
    def __init__(self, obj: canopen.objectdictionary, column: ft.Column):
        super().__init__()
        self.__obj = obj
        self.index = obj.index
        self.header = ft.ListTile(title=ft.Text(f'0x{self.__obj.index:04X} {self.__obj.name}'))
        self.can_tap_header = True
        self.__build_list_objects()
        self.__column = column

    def __build_settings_variable_panel(self, e: ft.ControlEvent):
        lt = e.control
        obj = e.control.data
        if not isinstance(obj, canopen.objectdictionary.ODVariable):  # I think it may be only ODVariable
            print("obj is no an ODVariable!")
            return
        if not isinstance(lt, ft.ListTile):  # I think it may be only ODVariable
            print("lt is no an ft.ListTile! It's impossible!!!")
            return
        # TODO like settings_panel_ctrl
        self.update()

    # Create new list tile (only Array and Record)
    # Because there are subindexes and they may be deleted
    def __new_list_tile(self, obj: canopen.objectdictionary.ODVariable):
        def handle_delete_subindex(e: ft.ControlEvent):
            self.content.controls.clear()  # Clear all subobj in flet
            if isinstance(self.__obj,
                          canopen.objectdictionary.ODRecord | canopen.objectdictionary.ODArray):  # if object is RECORD
                for subobj in self.__obj.values():
                    if subobj.subindex == 0:  # decrease num of subobj
                        subobj.default = subobj.default - 1
                        subobj.default_raw = str(subobj.default)
                    if subobj.subindex == e.control.data.subindex:  # delete subobj
                        del self.__obj.subindices[subobj.subindex]
                    if subobj.subindex > e.control.data.subindex:  # renumbering the remaining elements
                        del self.__obj.subindices[subobj.subindex]
                        subobj.subindex = subobj.subindex - 1
                        self.__obj.add_member(subobj)

            self.__build_list_objects()
            self.update()

        return ft.ListTile(
            title=ft.Text(f"0x{obj.subindex:02X} {obj.name}"),
            on_click=self.__build_settings_variable_panel,
            data=obj,
            trailing=ft.IconButton(ft.icons.DELETE, on_click=handle_delete_subindex, data=obj),
            subtitle=ft.Text(f"type: {data_type_map[obj.data_type]}\naccess: {obj.access_type}"),
        )

    def __build_list_objects(self):
        if isinstance(self.__obj, canopen.objectdictionary.ODArray | canopen.objectdictionary.ODRecord):
            self.content = ft.Column()
            for subobj in self.__obj.values():
                if subobj.subindex != 0:
                    lt = self.__new_list_tile(subobj)
                    self.content.controls.append(lt)
        if isinstance(self.__obj, canopen.objectdictionary.ODVariable):
            self.content = ft.Column()
            lt = ft.ListTile(
                title=ft.Text(f"0x{self.__obj.subindex:02X} {self.__obj.name}"),
                on_click=self.__build_settings_variable_panel,
                subtitle=ft.Text(f"type: {data_type_map[self.__obj.data_type]}\naccess: {self.__obj.access_type}"),
            )
            self.content.controls.append(lt)

    def build_settings_panel(self, delete_btn: ft.ElevatedButton):
        __tf_name = ft.TextField(label="Name", value=f'{self.__obj.name}')
        __tf_index = ft.TextField(label="Index", value=f'{self.__obj.index}')

        def save_clicked(e):
            self.__obj.name = __tf_name.value
            self.header = ft.ListTile(title=ft.Text(f'0x{self.__obj.index:04X} {self.__obj.name}'))
            self.update()

        def add_clicked(e):
            subindex = canopen.objectdictionary.ODVariable("Undefined", self.__obj.index, len(self.__obj.values()))
            subindex.access_type = "rw"
            subindex.data_type = canopen.objectdictionary.datatypes.UNSIGNED8
            lt = self.__new_list_tile(subindex)
            self.content.controls.append(lt)
            self.__obj.add_member(subindex)
            self.update()

        self.__column.controls.clear()
        self.__column.controls.append(ft.Text(f'0x{self.__obj.index:04X} {self.__obj.name}',
                                              style=ft.TextStyle(weight=ft.FontWeight.BOLD, size=20)))
        self.__column.controls.append(ft.Divider())
        self.__column.controls.append(__tf_name)
        self.__column.controls.append(__tf_index)
        self.__column.controls.append(ft.ElevatedButton(text="Save", on_click=save_clicked))
        if isinstance(self.__obj,
                      canopen.objectdictionary.ODRecord | canopen.objectdictionary.ODArray):  # if object is RECORD
            self.__column.controls.append(ft.ElevatedButton(text="Add subindex", on_click=add_clicked))
        self.__column.controls.append(delete_btn)


class ObjDictPanel(ft.ResponsiveRow):
    def __init__(self, od):
        super().__init__()
        self.visible = False
        self.lv_obj = ft.ListView(expand=1, spacing=10, padding=20, height=400, col=4)
        self.settings_obj = ft.Column(wrap=True, )

        def delete_clicked(e):
            setting_ctrl = e.control.parent.controls  # get control @ObjectDictionaryField
            for i in range(len(setting_ctrl)):  # get all ft controls in panel of @ObjectDictionaryField
                if isinstance(setting_ctrl[i], ft.TextField):  # It's very stupid
                    label = setting_ctrl[i].label  # It's @__tf_name in panel of @ObjectDictionaryField
                    value = setting_ctrl[i].value
                    if label == 'Index':
                        od.object_dictionary.__delitem__(int(value))

                        for element in self.__panel.controls:  # Search element form panel
                            if int(value) == element.index:  # Remove element form panel
                                self.__panel.controls.remove(element)
                                self.settings_obj.controls.clear()
                                self.update()
                                return

        self.__del_obj = ft.ElevatedButton(text="Delete object", on_click=delete_clicked)

        def handle_change(e: ft.ControlEvent):
            i = int(e.data)
            self.__panel.controls[i].build_settings_panel(self.__del_obj)  # view setting panel
            # target = self.__panel.controls[i].get_object()  # get field from OD
            # print(f"target: {target.name}")
            self.update()

        self.__panel = ft.ExpansionPanelList(
            expand_icon_color=ft.colors.AMBER,
            col=4,
            elevation=8,
            divider_color=ft.colors.AMBER,
            on_change=handle_change,
        )

        # Check all object from OD
        for obj in od.object_dictionary.values():
            index = ObjectDictionaryField(obj, self.settings_obj)
            self.__panel.controls.append(index)

        self.lv_obj.controls.append(self.__panel)

        self.controls = [
            ft.ResponsiveRow(
                [
                    ft.Container(
                        self.lv_obj,
                        border=ft.border.all(1, ft.colors.BLUE_400),
                        border_radius=ft.border_radius.all(10),
                        col=4,
                    ),
                    ft.Container(
                        content=ft.Container(
                            margin=ft.margin.all(16),
                            content=self.settings_obj,
                        ),
                        border=ft.border.all(1, ft.colors.BLUE_400),
                        border_radius=ft.border_radius.all(10),
                        col=8
                    )
                ],
            ),
        ]
