import canopen
import can
import logging

nodes = []

def nnode(od_file):
    logging.basicConfig(level=logging.DEBUG)
    # Start with creating a network representing one CAN bus
    network = canopen.Network()
    bus = can.Bus(interface='socketcan', channel='vcan1')
    network.bus = bus

    # Add some nodes with corresponding Object Dictionaries
    node_id = 0x03
    node = canopen.LocalNode(node_id, od_file)
    nodes.append(node)
    network.add_node(node)

    network.connect()

    # Read a variable using SDO
    # device_name = node.sdo['Manufacturer device name'].raw
    # vendor_id = node.sdo[0x1018][1].raw

    # Write a variable using SDO
    # node.sdo['Producer heartbeat time'].raw = 1000

    # Read PDO configuration from node and start
    node.tpdo.read()
    node.rpdo.read()
    node.nmt.send_command(0x0) # Send boot up in start
    node.nmt.state = 'PRE-OPERATIONAL' # To finish Initialing state
    # node.tpdo.save()
    # node.tpdo.read()

    def nmt_callback(id: int, bytearray, timestamp: float) -> None:
        for node in nodes:
            if(node.nmt.state == 'INITIALISING'):
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
