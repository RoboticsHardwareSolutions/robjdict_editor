import os
import canopen
import flet as ft
from panels.dev_info import DevInfoPanel
from panels.life_communication import LifeCommunicationPanel
from panels.sdo_communication import SdoCommunicationPanel
from panels.pdo_communication import PdoCommunicationPanel
from panels.object_dictionary import ObjDictPanel


class CustomTab(ft.Tab):
    CTRL_DEVICE_INFO = "Device info"
    CTRL_LIFE_COMMUNICATION = "Life communication"
    CTRL_SDO_COMMUNICATION = "SDO communication"
    CTRL_PDO_COMMUNICATION = "PDO communication"
    CTRL_OBJECT_DICTIONARY = "Object Dictionary"

    def __init__(self, path_to_od):
        super().__init__()
        self.path_to_od = path_to_od
        self.text = os.path.basename(path_to_od)
        self.cssb = ft.CupertinoSlidingSegmentedButton(
            selected_index=0,
            thumb_color=ft.colors.BLUE_400,
            on_change=self.__seg_btn,
            padding=ft.padding.symmetric(0, 10),
            controls=[
                ft.Text(self.CTRL_DEVICE_INFO),
                ft.Text(self.CTRL_LIFE_COMMUNICATION),
                ft.Text(self.CTRL_SDO_COMMUNICATION),
                ft.Text(self.CTRL_PDO_COMMUNICATION),
                ft.Text(self.CTRL_OBJECT_DICTIONARY),
            ],
        )

        network = canopen.Network()
        od = network.add_node(1, object_dictionary=self.path_to_od)

        self.dev_info = DevInfoPanel(od)
        self.life_communication = LifeCommunicationPanel(od)
        self.sdo_communication = SdoCommunicationPanel(od)
        self.pdo_communication = PdoCommunicationPanel(od)
        self.obj_dict = ObjDictPanel(od)
        # Main panel
        self.content = ft.Column([
            self.cssb,
            self.dev_info,
            self.life_communication,
            self.sdo_communication,
            self.pdo_communication,
            self.obj_dict
        ])

    def __seg_btn(self, e):
        target_segment = e.control.controls[int(e.data)].value
        if target_segment == self.CTRL_DEVICE_INFO:
            self.dev_info.visible = True
            self.life_communication.visible = False
            self.sdo_communication.visible = False
            self.pdo_communication.visible = False
            self.obj_dict.visible = False
        elif target_segment == self.CTRL_LIFE_COMMUNICATION:
            self.dev_info.visible = False
            self.life_communication.visible = True
            self.sdo_communication.visible = False
            self.pdo_communication.visible = False
            self.obj_dict.visible = False
        elif target_segment == self.CTRL_SDO_COMMUNICATION:
            self.dev_info.visible = False
            self.life_communication.visible = False
            self.sdo_communication.visible = True
            self.pdo_communication.visible = False
            self.obj_dict.visible = False
        elif target_segment == self.CTRL_PDO_COMMUNICATION:
            self.dev_info.visible = False
            self.life_communication.visible = False
            self.sdo_communication.visible = False
            self.pdo_communication.visible = True
            self.obj_dict.visible = False
        elif target_segment == self.CTRL_OBJECT_DICTIONARY:
            self.dev_info.visible = False
            self.life_communication.visible = False
            self.sdo_communication.visible = False
            self.pdo_communication.visible = False
            self.obj_dict.visible = True
        self.update()
