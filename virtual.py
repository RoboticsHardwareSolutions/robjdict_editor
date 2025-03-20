import canopen
import can
import logging
import time

nodes = []

class MyListener(can.Listener):
    def on_message_received(self, msg: can.Message):
        if msg.is_remote_frame:
            for node in nodes:
                if node.id == msg.arbitration_id - 0x700:
                    code = node.nmt.state
                    node.nmt.send_command(canopen.nmt.NMT_COMMANDS[code])

def nnode():
    logging.basicConfig(level=logging.DEBUG)
    # Start with creating a network representing one CAN bus
    network = canopen.Network()
    bus = can.Bus(interface='socketcan', channel='vcan1')
    network.bus = bus

    network.listeners.append(MyListener())

    def append_node(node_id, file):
        node = canopen.LocalNode(node_id, file)
        nodes.append(node)
        network.add_node(node)
        

    # Add some nodes with corresponding Object Dictionaries
    for i in range(2):
        append_node(0x02 + i, 'ObjDict1.eds')
    for i in range(2):
        append_node(0x06 + i, 'ObjDict2.eds')
    for i in range(1):
        append_node(0x20 + i, 'ObjDict3.eds')
    for i in range(1):
        append_node(0x10 + i, 'ObjDict4.eds')
    for i in range(3):
        append_node(0x14 + i, 'ObjDict5.eds')

    network.connect()

    # Read a variable using SDO
    # device_name = node.sdo['Manufacturer device name'].raw
    # vendor_id = node.sdo[0x1018][1].raw

    # Write a variable using SDO
    # node.sdo['Producer heartbeat time'].raw = 1000

    # Read PDO configuration from node and start
    for node in nodes:
        # node.tpdo.read()
        # node.rpdo.read()
        node.nmt.send_command(0x0) # Send boot up in start
        node.nmt.state = 'PRE-OPERATIONAL' # To finish Initialing state
    # node.tpdo.save()
    # node.tpdo.read()

    def nmt_callback(id: int, bytearray, timestamp: float) -> None:
        for node in nodes:
            if(node.nmt.state == 'INITIALISING'):
                time.sleep(1)
                node.nmt.send_command(0)

    def sync_pdo_callback(id: int, bytearray, timestamp: float) -> None:
        for node in nodes:
            if(node.nmt.state == 'OPERATIONAL'):
                try:
                    if(node.tpdo[1].trans_type == 0x01):
                        node.tpdo[1].transmit()
                    if(node.tpdo[2].trans_type == 0x01):
                        node.tpdo[2].transmit()
                    if(node.tpdo[3].trans_type == 0x01):
                        node.tpdo[3].transmit()
                    if(node.tpdo[4].trans_type == 0x01):
                        node.tpdo[4].transmit()
                except:
                    pass

    network.subscribe(0x000, nmt_callback)
    network.subscribe(0x080, sync_pdo_callback)
    # node.nmt.start_heartbeat(node.object_dictionary.get_variable('Producer Heartbeat Time').default)

    while True:
        # for node_id in network.scanner.nodes:
            # print(f"Found node {hex(node_id)}!")
        pass
    # Disconnect from CAN bus
    network.disconnect()


if __name__ == '__main__':
    nnode()
