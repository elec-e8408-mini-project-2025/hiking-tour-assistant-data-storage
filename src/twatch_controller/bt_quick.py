from subprocess import check_output
from time import sleep
import socket

from repository.tracking_data_repository import default_tracking_data_repository as repository


from app import logger

class BTQuick(object):
    def __init__(self):
        self.bt_controller_mac = ""
        self.bt_connected_device_mac = ""
        self.bt_connected_device_socket = ""
        self.start_bt()
    
    def get_mac_address(self):
        return self.bt_connected_device_mac

    def destroy(self):
        if self.bt_connected_device_socket != "":
            self.bt_connected_device_socket.shutdown(socket.SHUT_RDWR)
            self.bt_connected_device_socket.close()

        if self.bt_connected_device_mac != "":
            sleep(2)
            ret = check_output(["bluetoothctl", "disconnect", self.bt_connected_device_mac], text=True)
            sleep(2)
            ret = check_output(["bluetoothctl", "remove", self.bt_connected_device_mac], text=True)
        
    def start_bt(self):
        ret = check_output(["bluetoothctl", "list"], text=True)
        self.bt_controller_mac = ret.split(" ")[1]
        ret = check_output(["bluetoothctl", "select", f"{self.bt_controller_mac}"], text=True)
        ret = check_output(["bluetoothctl", "power", "on"], text=True)
        assert "power on succeeded" in ret,\
        "Failed to power on BT controller on the operating system."

    def connect_to_device_by_name(self, bt_device_name, bt_device_mac=""):
        logger.debug("BEGIN")
        ret = check_output(["bluetoothctl", "--timeout", "10", "scan", "on"], text=True)
        ret = check_output(["bluetoothctl", "devices"], text=True)
        for found_device in ret.split("\n"):
            if bt_device_name in found_device and bt_device_mac in found_device:
                self.bt_connected_device_mac = found_device.split(" ")[1]
                logger.debug(f'FOUND: {found_device}')
                logger.debug(f'Set bt_connected_device_mac to {self.bt_connected_device_mac}, from {found_device.split(" ")}')
                print("Found:", found_device)
                break
        assert self.bt_connected_device_mac != "",\
        "Unable to connect to usb device"
        ret = check_output(["echo", "yes", "|", "bluetoothctl", "pair", self.bt_connected_device_mac], text=True)
        logger.debug(f"Checking output: {ret}")
        logger.debug("END")

    def connect_device_socket(self):
        self.bt_connected_device_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self.bt_connected_device_socket.connect((self.bt_connected_device_mac, 1))

    def send_data_socket(self, data):
        self.bt_connected_device_socket.send(bytes(data+"\n", 'UTF-8'))
        ret_data = ""
        ret_data=self.bt_connected_device_socket.recv(1024)
        
        return ret_data.decode("utf-8")
