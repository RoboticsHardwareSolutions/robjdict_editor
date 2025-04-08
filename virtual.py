import canopen
import can
import logging
import time

import threading
from concurrent.futures import ThreadPoolExecutor

nodes = []

executor = ThreadPoolExecutor(max_workers=10)

#чтобы штатно завершать по ctrl + c
shutdown_event = threading.Event()

class MyListener(can.Listener):
    def on_message_received(self, msg: can.Message):
        if msg.is_remote_frame:
            for node in nodes:
                if node.id == msg.arbitration_id - 0x700:
                    code = node.nmt.state
                    node.nmt.send_command(canopen.nmt.NMT_COMMANDS[code])

# обработчик NMT команды в отдельном потоке
def handle_nmt(node):
    def task():
        logging.debug(f"NMT init task started for node {node.id}")
        time.sleep(1)
        node.nmt.send_command(0)
        logging.debug(f"NMT start command sent to node {node.id}")

    executor.submit(task)

# обработчик SYNC команд в отдельном потоке
def handle_sync_pdo(node):
    def task():
        try:
            logging.debug(f"SYNC handling for node {node.id}")
            for i in range(1, 5):
                if node.tpdo[i].trans_type == 0x01:
                    node.tpdo[i].transmit()
                    logging.debug(f"TPDO {i} transmitted for node {node.id}")
        except Exception as e:
            logging.debug(f"PDO transmit error in node {node.id}: {e}")

    executor.submit(task)

def nnode():
    logging.basicConfig(level=logging.DEBUG)
    # Start with creating a network representing one CAN bus
    network = canopen.Network()
    bus = can.Bus(interface='socketcan', channel='vcan0')
    network.bus = bus

    network.listeners.append(MyListener())

    def append_node(node_id, file):
        node = canopen.LocalNode(node_id, file)
        nodes.append(node)
        network.add_node(node)

    # Add some nodes with corresponding Object Dictionaries
    for i in range(5):
        append_node(0x02 + i, 'upload/ObjDict.eds')

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
        node.nmt.send_command(0x0)  # Send boot up in start
        node.nmt.state = 'PRE-OPERATIONAL'  # To finish Initialing state
        node.tpdo.save()
        node.tpdo.read()

    def nmt_callback(arbitration_id: int, data: bytearray, timestamp: float) -> None:
        for n in nodes:
            if n.nmt.state == 'INITIALISING':
                handle_nmt(n)

    def sync_pdo_callback(arbitration_id: int, data: bytearray, timestamp: float) -> None:
        for n in nodes:
            if n.nmt.state == 'OPERATIONAL':
                handle_sync_pdo(n)

    network.subscribe(0x000, nmt_callback)
    network.subscribe(0x080, sync_pdo_callback)
    # node.nmt.start_heartbeat(node.object_dictionary.get_variable('Producer Heartbeat Time').default)

    try:
        # Ждём сигнал завершения
        shutdown_event.wait()
    except KeyboardInterrupt:
        print("Выход по Ctrl+C...")
    finally:
        network.disconnect()
        executor.shutdown(wait=False)  # Завершаем потоковый пул
    # Disconnect from CAN bus
    network.disconnect()


if __name__ == '__main__':
    nnode()
