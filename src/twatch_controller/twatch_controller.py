from subprocess import check_output
from time import sleep
import socket
import json

from repository.tracking_data_repository import default_tracking_data_repository as repository
from entity.tracking_data import TrackingDataEntry
from twatch_controller.t_watch import Twatch

from app import logger


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


def parse_json_data(trip):
    logger.debug(f"BEGIN")

    data_json = trip["Data"]
    #print("found new data")
    logger.debug(f"Found new data with id {data_json['ID']}")
    try:
        date_tmp = data_json["StartTimestamp"].split(" ")[0].split("-") # Format: "yyyy-m-d h:m:s" example "2033-2-5 5:4:13"
        date = ""
        date += date_tmp[0]+"-"
        if len(date_tmp[1]) == 2:
            date += date_tmp[1]+"-"
        else:
            date += "0"+date_tmp[1]+"-"
        
        if len(date_tmp[2]) == 2:
            date += date_tmp[2]
        else:
            date += "0"+date_tmp[2]

        avg_speed = round(float(data_json["AvgSpeed"]), 1)

        distance = round(int(data_json["Steps"]) * 0.76 / 1000, 2)

        steps = int(data_json["Steps"])
        
        # SRS documentation for calory calculations
        calories = round( distance * 56 / 1000, 1)

        entry = TrackingDataEntry(date=date, avg_speed=avg_speed,distance=distance,steps=steps,calories=calories)

        logger.debug("Entry parsed succesfully. Adding entry.")
        repository.add_entry(entry)
        logger.debug("END")
        
    except IndexError as e:
        logger.warning(f"Index out of range, skipping data entry and continuing execution. Entry: {trip}. Error: {e}")
        
    except KeyError as e:
        logger.warning(f"Key not found, skipping data entry and continuing execution. Entry: {trip}. Error: {e}")

    except Exception as e:
        logger.error(f"Unhandled exception occured. Aborting: {e}")
        raise Exception(e)
        

    
def bluetooth_sync_routine():

    logger.debug("BEGIN")
    try:
        
        #repository.setup_watch_device()
        watch = Twatch()

        logger.debug(f'Using watch {watch.bluetooth_id} with MAC: {watch.bluetooth_mac}')

        data_json = watch.get_trip_data(return_only_new_trips=True, mark_when_synced=True)

        for trip in data_json:
            parse_json_data(trip)
        
        logger.debug("END")
    except Exception as e:
        logger.error(f"Unhandled exception occured. Aborting. Error: {e}")
        raise Exception(e) 
    
    

