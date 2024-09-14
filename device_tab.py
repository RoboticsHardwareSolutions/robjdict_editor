import os
import canopen
import flet as ft
from panels.dev_info import DevInfoPanel
from panels.life_communication import LifeCommunicationPanel
from panels.sdo_communication import SdoCommunicationPanel
from panels.tx_pdo_communication import TPdoCommunicationPanel
from panels.rx_pdo_communication import RPdoCommunicationPanel
from panels.object_dictionary import ObjDictPanel


class DeviceTab(ft.Tab):
    CTRL_DEVICE_INFO = "Device info"
    CTRL_LIFE_COMMUNICATION = "Life communication"
    CTRL_SDO_COMMUNICATION = "SDO communication"
    CTRL_TPDO_COMMUNICATION = "TPDO communication"
    CTRL_RPDO_COMMUNICATION = "RPDO communication"
    CTRL_OBJECT_DICTIONARY = "Object Dictionary"

    def __init__(self, path_to_od, ibtn: ft.IconButton):
        super().__init__()

        self.path_to_od = path_to_od
        self.text = os.path.basename(path_to_od)
        self.tab_content = ft.Row([ft.Text(self.text), ibtn])
        self.cssb = ft.CupertinoSlidingSegmentedButton(
            selected_index=0,
            thumb_color=ft.colors.BLUE_400,
            on_change=self.__seg_btn,
            padding=ft.padding.symmetric(0, 10),
            controls=[
                ft.Text(self.CTRL_DEVICE_INFO),
                ft.Text(self.CTRL_LIFE_COMMUNICATION),
                ft.Text(self.CTRL_SDO_COMMUNICATION),
                ft.Text(self.CTRL_TPDO_COMMUNICATION),
                ft.Text(self.CTRL_RPDO_COMMUNICATION),
                ft.Text(self.CTRL_OBJECT_DICTIONARY),
            ],
        )

        network = canopen.Network()
        self.__od = network.add_node(1, object_dictionary=self.path_to_od)

        self.dev_info = DevInfoPanel(self.__od)
        self.life_communication = LifeCommunicationPanel(self.__od)
        self.sdo_communication = SdoCommunicationPanel(self.__od)
        self.tx_pdo_communication = TPdoCommunicationPanel(self.__od)
        self.rx_pdo_communication = RPdoCommunicationPanel(self.__od)
        self.obj_dict = ObjDictPanel(self.__od)
        # Main panel
        self.content = ft.Column([
            self.cssb,
            self.dev_info,
            self.life_communication,
            self.sdo_communication,
            self.tx_pdo_communication,
            self.rx_pdo_communication,
            self.obj_dict
        ])

    def save_device(self):
        od = self.__od
        od = self.dev_info.update_od(od)
        od = self.life_communication.update_od(od)
        od = self.sdo_communication.update_od(od)
        canopen.export_od(od.object_dictionary, self.path_to_od)

    def __seg_btn(self, e):
        target_segment = e.control.controls[int(e.data)].value
        if target_segment == self.CTRL_DEVICE_INFO:
            self.dev_info.visible = True
            self.life_communication.visible = False
            self.sdo_communication.visible = False
            self.tx_pdo_communication.visible = False
            self.rx_pdo_communication.visible = False
            self.obj_dict.visible = False
        elif target_segment == self.CTRL_LIFE_COMMUNICATION:
            self.dev_info.visible = False
            self.life_communication.visible = True
            self.sdo_communication.visible = False
            self.tx_pdo_communication.visible = False
            self.rx_pdo_communication.visible = False
            self.obj_dict.visible = False
        elif target_segment == self.CTRL_SDO_COMMUNICATION:
            self.dev_info.visible = False
            self.life_communication.visible = False
            self.sdo_communication.visible = True
            self.tx_pdo_communication.visible = False
            self.rx_pdo_communication.visible = False
            self.obj_dict.visible = False
        elif target_segment == self.CTRL_TPDO_COMMUNICATION:
            self.dev_info.visible = False
            self.life_communication.visible = False
            self.sdo_communication.visible = False
            self.tx_pdo_communication.visible = True
            self.rx_pdo_communication.visible = False
            self.obj_dict.visible = False
        elif target_segment == self.CTRL_RPDO_COMMUNICATION:
            self.dev_info.visible = False
            self.life_communication.visible = False
            self.sdo_communication.visible = False
            self.tx_pdo_communication.visible = False
            self.rx_pdo_communication.visible = True
            self.obj_dict.visible = False
        elif target_segment == self.CTRL_OBJECT_DICTIONARY:
            self.dev_info.visible = False
            self.life_communication.visible = False
            self.sdo_communication.visible = False
            self.tx_pdo_communication.visible = False
            self.rx_pdo_communication.visible = False
            self.obj_dict.visible = True
        self.update()
