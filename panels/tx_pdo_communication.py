import canopen
import can
from can import Message
import flet as ft


class TPdoCommunicationPanel(ft.ResponsiveRow):
    def __init__(self, od):
        super().__init__()
        self.visible = False

        self.lv_od = ft.ListView(expand=1, spacing=10, padding=20, height=200, col=8)

        self.dt_tpdo = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Index")),
                ft.DataColumn(ft.Text("COB ID")),
                ft.DataColumn(ft.Text("Data")),
            ],
        )
        self.lv_tpdo = ft.ListView(expand=1, spacing=10, padding=20, height=200, col=8)
        self.lv_tpdo.controls.append(self.dt_tpdo)

        # Check records
        for obj in od.object_dictionary.values():
            if obj.index >= 0x2000:
                if isinstance(obj, (canopen.objectdictionary.ODRecord, canopen.objectdictionary.ODArray)):
                    for subobj in obj.values():
                        if "Number of " not in subobj.name:
                            self.lv_od.controls.append(
                                ft.Draggable(
                                    group="tpdo",
                                    content=ft.Text(f' 0x{obj.index:04X} {subobj.subindex:02X}: {subobj.name}'),
                                    content_feedback=ft.Text(f' 0x{obj.index:04X} {subobj.subindex:02X}: {subobj.name}',
                                                             size=20),
                                ), )

        # Check TPDO
        def drag_accept(e):
            # get draggable (source) control by its ID
            for src in self.lv_od.controls:
                if src.uid == e.src_id:
                    if isinstance(src, ft.Draggable):
                        e.control.content.content.value = "1"
                    break

            self.update()

        for obj in od.object_dictionary.values():
            if 0x1800 <= obj.index < 0x1900:
                if isinstance(obj, canopen.objectdictionary.ODRecord):
                    self.dt_tpdo.rows.append(ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(f'0x{obj.index:04X}')),
                            ft.DataCell(ft.Text(f'0x{obj.subindices[1].default:03X}')),
                            ft.DataCell(
                                ft.DragTarget(
                                    group="tpdo",
                                    content=ft.Container(
                                        content=ft.Text("Empty", size=20),
                                    ),
                                    on_accept=drag_accept,
                                ),
                            ),
                        ],
                    ))

        self.controls = [
            self.lv_od,
            self.lv_tpdo
        ]
