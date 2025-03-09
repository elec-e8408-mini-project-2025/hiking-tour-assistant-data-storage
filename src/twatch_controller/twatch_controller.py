from subprocess import check_output
from time import sleep
import socket
import json

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

class Twatch(object):
    def __init__(self, bluetooth_id = "HIKING_WATCH", bluetooth_mac=""):
        self.bluetooth_id = bluetooth_id
        self.bluetooth_mac = bluetooth_mac 

    # Search for twatch and update mac address
    def search_mac_address(self):
        logger.debug("BEGIN")
        bt = BTQuick()
        try:
            bt.connect_to_device_by_name(self.bluetooth_id)
            mac = bt.get_mac_address()
        except:
            logger.debug("Exception occured, setting MAC to empty string")
            mac = ""
        bt.destroy()
        self.bluetooth_mac = mac
        logger.debug("END")
        return mac

    def get_bluetooth_mac(self):
        return self.bluetooth_mac
    
    def get_bluetooth_id(self):
        return self.bluetooth_id

    # Connect to twatch if available and return a json array of all data
    # If no data is available or the twatch is unreachable it will return a json list with length 0
    def get_trip_data(self, mark_when_synced=True, return_only_new_trips=False):    
        bt = BTQuick()
        try:
            bt.connect_to_device_by_name(self.bluetooth_id, self.bluetooth_mac)
            bt.connect_device_socket()

            get_trip_addresses = bt.send_data_socket("GET")

            data = json.loads(bt.send_data_socket("GET /tripdata"))

            return_array = "["

            for trip_path in data["Paths"]:
                return_array += bt.send_data_socket(f"GET {trip_path}")
                return_array += ","

                if mark_when_synced == True:
                    data = bt.send_data_socket(f"POST {{}} {trip_path}/tagset")
        
            
            return_array = return_array[:-1] + "]"

            bt.destroy()
        except:
            return_array = "[]"

        all_data_json = json.loads(return_array)

        if return_only_new_trips == True:
            ret = []
            for trip in all_data_json:
                if trip["Data"]["Tag"] == 0 and trip["Data"]["StartTimestamp"] != "0-0-0 0:0:0":
                    ret.append(trip)
        else:
            ret = all_data_json

        return ret


def example_use():
    a = Twatch()

    all_data_json = a.get_trip_data(return_only_new_trips=False, mark_when_synced=True)
    if len(all_data_json) != 0:
        for trip_json in all_data_json:
            data_json = trip_json["Data"]
            print("- - - - - - - - - - - - - - -")
            print("Trip_id:",data_json["ID"])
            print("Start_timestamp",data_json["StartTimestamp"])
            print("End_timestamp",data_json["EndTimestamp"])
            print("Steps", data_json["Steps"])
            print("Avspeed", data_json["AvgSpeed"])
            print("Tag", data_json["Tag"])
#example_use()
