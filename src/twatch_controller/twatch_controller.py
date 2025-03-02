from subprocess import check_output
from time import sleep
import socket
import json

class BTQuick(object):
    def __init__(self):
        self.bt_controller_mac = ""
        self.bt_connected_device_mac = ""
        self.bt_connected_device_socket = ""
        self.start_bt()
        
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
        ret = check_output(["bluetoothctl", "--timeout", "5", "scan", "on"], text=True)
        ret = check_output(["bluetoothctl", "devices"], text=True)
        for found_device in ret.split("\n"):
            if bt_device_name in found_device and bt_device_mac in found_device:
                self.bt_connected_device_mac = found_device.split(" ")[1]
                print("Found:", found_device)
                break
        assert self.bt_connected_device_mac != "",\
        "Unable to connect to usb device"
        ret = check_output(["bluetoothctl", "pair", self.bt_connected_device_mac], text=True)

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

    def get_trip_data(self):    
        bt = BTQuick()
        bt.connect_to_device_by_name(self.bluetooth_id, self.bluetooth_mac)
        bt.connect_device_socket()

        get_trip_addresses = bt.send_data_socket("GET")

        data = json.loads(bt.send_data_socket("GET /tripdata"))

        return_array = "["

        for trip_path in data["Paths"]:
            return_array += bt.send_data_socket(f"GET {trip_path}")
            return_array += ","
        
        return_array = return_array[:-1] + "]"

        bt.destroy()

        return json.loads(return_array)


def example_use():
    a = Twatch()

    all_data_json = a.get_trip_data()

    for trip_json in all_data_json:
        print("- - - - - - - - - - - - - - -")
        print("Trip_id:",trip_json["ID"])
        print("Start_timestamp",trip_json["StartTimestamp"])
        print("End_timestamp",trip_json["EndTimestamp"])
        print("Steps", trip_json["Steps"])
        print("Avspeed", trip_json["AvgSpeed"])

example_use()