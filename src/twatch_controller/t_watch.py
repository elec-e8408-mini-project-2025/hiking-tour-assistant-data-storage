from subprocess import check_output
from time import sleep
import socket
import json

from repository.tracking_data_repository import default_tracking_data_repository as repository
from entity.tracking_data import TrackingDataEntry
from twatch_controller.bt_quick import BTQuick

from app import logger


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
        except Exception as e:
            logger.error(f"Exception occured, setting MAC to empty string. Error: {e}")
            mac = ""
            raise Exception(e)
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
        except Exception as e:
            # return_array = "[]"
            logger.error(f"Unhandled exception occured: {e}")
            raise Exception(e)

        all_data_json = json.loads(return_array)

        if return_only_new_trips == True:
            ret = []
            for trip in all_data_json:
                if trip["Data"]["Tag"] == 0 and trip["Data"]["StartTimestamp"] != "0-0-0 0:0:0":
                    ret.append(trip)
        else:
            ret = all_data_json

        return ret