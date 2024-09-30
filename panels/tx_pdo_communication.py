import canopen
import can
from can import Message
import flet as ft


def size_data_type(value):
    '''Get data size in bits (dynamic types like DOMAIN, VISIBLE_STRING, etc will return 0)'''
    size = 0

    if value in [canopen.objectdictionary.BOOLEAN, canopen.objectdictionary.INTEGER8,
                 canopen.objectdictionary.UNSIGNED8]:
        size = 8
    elif value in [canopen.objectdictionary.INTEGER16, canopen.objectdictionary.UNSIGNED16]:
        size = 16
    elif value in [canopen.objectdictionary.INTEGER24, canopen.objectdictionary.UNSIGNED24]:
        size = 24
    elif value in [canopen.objectdictionary.INTEGER32, canopen.objectdictionary.UNSIGNED32,
                   canopen.objectdictionary.REAL32]:
        size = 32
    elif value in [canopen.objectdictionary.INTEGER40, canopen.objectdictionary.UNSIGNED40]:
        size = 40
    elif value in [canopen.objectdictionary.INTEGER48, canopen.objectdictionary.UNSIGNED48,
                   canopen.objectdictionary.TIME_OF_DAY,
                   canopen.objectdictionary.TIME_DIFFERENCE]:
        size = 48
    elif value in [canopen.objectdictionary.INTEGER56, canopen.objectdictionary.UNSIGNED56]:
        size = 56
    elif value in [canopen.objectdictionary.INTEGER64, canopen.objectdictionary.UNSIGNED64,
                   canopen.objectdictionary.REAL64]:
        size = 64

    return size


class PDOField(ft.ResponsiveRow):
    def __init__(self, pdo_obj, pdo_map, event):
        super().__init__()

        self.__index = ft.Text(f'0x{pdo_obj.index:04X}', col=1)
        self.__subindex = ft.Text(f'0x{pdo_obj.subindices[1].default:03X}', col=1)
        self.__map = pdo_map

        self.__map_data = ft.Container(
            ft.DragTarget(
                group="tpdo",
                content=ft.Text("Empty", overflow=ft.TextOverflow.ELLIPSIS),
                on_accept=event,
            ), col=1
        )

        def check_item_clicked(e):
            e.control.checked = not e.control.checked
            self.update()

        self.__pb_delete = ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(text="Item 1"),
                ft.PopupMenuItem(icon=ft.icons.POWER_INPUT, text="Check power"),
                ft.PopupMenuItem(
                    content=ft.Row(
                        [
                            ft.Icon(ft.icons.HOURGLASS_TOP_OUTLINED),
                            ft.Text("Item with a custom content"),
                        ]
                    ),
                    on_click=lambda _: print("Button with a custom content clicked!"),
                ),
                ft.PopupMenuItem(),  # divider
                ft.PopupMenuItem(
                    text="Checked item", checked=False, on_click=check_item_clicked
                ),
            ],
            height=20,
            width=10,
            icon_size=15,
            visible=False,
            col=1
        )

        self.controls = [
            self.__index,
            self.__subindex,
            self.__map_data,
            self.__pb_delete
        ]

    def insert(self, obj):
        available = 12
        for field in self.controls:
            available -= field.col
            if available == 0:
                return

        added_col = size_data_type(obj.data_type) / 8
        if available < added_col:
            return
        if available == added_col:
            self.__map_data.visible = False
        self.__pb_delete.visible = True
        self.controls.insert(len(self.controls) - 2,
                             ft.Text(f'0x{obj.index:04X}/{obj.subindex:02X}', overflow=ft.TextOverflow.ELLIPSIS,
                                     col=size_data_type(obj.data_type) / 8))


class TPdoCommunicationPanel(ft.ResponsiveRow):
    def __init__(self, od):
        super().__init__()
        self.visible = False

        self.lv_od = ft.ListView(expand=1, spacing=10, padding=20, height=200, col=8)

        self.__dt_tpdo = ft.ResponsiveRow([
            ft.Text("Index", col=1),
            ft.Text("COB ID", col=1),
            ft.Text("Byte 1", col=1),
            ft.Text("Byte 2", col=1),
            ft.Text("Byte 3", col=1),
            ft.Text("Byte 4", col=1),
            ft.Text("Byte 5", col=1),
            ft.Text("Byte 6", col=1),
            ft.Text("Byte 7", col=1),
            ft.Text("Byte 8", col=1),
        ]
        )
        self.lv_tpdo = ft.ListView(expand=1, spacing=10, padding=20, height=200, col=10)
        self.lv_tpdo.controls.append(self.__dt_tpdo)

        # Check records
        for obj in od.object_dictionary.values():
            if obj.index >= 0x2000:
                if isinstance(obj, (canopen.objectdictionary.ODRecord, canopen.objectdictionary.ODArray)):
                    for subobj in obj.values():
                        if "Number of " not in subobj.name:
                            self.lv_od.controls.append(
                                ft.Draggable(
                                    group="tpdo",
                                    content=
                                    ft.ResponsiveRow([
                                        ft.Text(f'0x{obj.index:04X}', col=1.5),
                                        ft.Text(f'0x{subobj.subindex:02X}', col=1),
                                        ft.Text(f'{subobj.name}', col=6),
                                        ft.Text(f'{size_data_type(subobj.data_type)}', col=2),
                                    ]
                                    ),
                                    content_feedback=ft.Text(
                                        f'0x{obj.index:04X} 0x{subobj.subindex:02X}: {subobj.name}'),
                                ), )

        # Check TPDO
        def drag_accept(e):
            # get draggable (source) control by its ID
            for src in self.lv_od.controls:
                if src.uid == e.src_id:
                    pdo_field = e.control.parent.parent
                    if isinstance(src, ft.Draggable) and isinstance(pdo_field, PDOField):
                        index = int(src.content.controls[0].value, 16)
                        subindex = int(src.content.controls[1].value, 16)
                        name = src.content.controls[2].value
                        pdo_field.insert(od.object_dictionary[index][subindex])
                    break
            self.update()

        # Filling tpdo list
        for tpdo_params in od.object_dictionary.values():
            if 0x1800 <= tpdo_params.index < 0x1900:
                if isinstance(tpdo_params, canopen.objectdictionary.ODRecord):
                    # TODO params panel
                    # for tpdo_param in tpdo_params.values():
                    #     print(f'  {tpdo_param.subindex}: {tpdo_param.name}')
                    tpdo_map = od.object_dictionary[tpdo_params.index + 0x200]
                    tpdo_field = PDOField(tpdo_params, tpdo_map, drag_accept)
                    self.lv_tpdo.controls.append(tpdo_field)

        # main control
        self.controls = [
            self.lv_od,
            self.lv_tpdo
        ]
