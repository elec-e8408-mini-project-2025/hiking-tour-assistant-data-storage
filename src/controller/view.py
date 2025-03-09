from app import logger
import uuid
from app import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from twatch_controller.twatch_controller import Twatch
from entity.tracking_data import TrackingDataEntry

from repository.tracking_data_repository import default_tracking_data_repository as repository


@app.route('/')
def main():
    logger.debug("BEGIN")

    top_distance = repository.top_entry_for_distance()
    top_speed = repository.top_entry_for_speed()
    last_route = repository.fetch_last_entry()

    # Averages: distance, speed, steps, calories
    average_values = repository.fetch_avg_data()
    print(top_distance)

    logger.debug("END")

    return render_template('index.html', top_distance=top_distance, top_speed=top_speed, last_route=last_route, average_values=average_values)



@app.route('/hikes')
def hikes_list():
    logger.debug("BEGIN")

    columns, rows = repository.fetch_all_tracking_data()


    logger.debug("END")

    return render_template('hikes.html', columns=columns, rows=rows)


@app.route('/config')
def config():
    logger.debug("BEGIN")

    logger.debug("END")

    return render_template('config.html')


@app.route('/hike/<int:hikeid>', methods=['POST'])
def hikes_views(hikeid):
    logger.debug("BEGIN")

    repository.delete_hike(hikeid)

    logger.debug("END")

    return redirect(url_for('hikes_list'))

@app.route('/bluetooth-setup')
def bluetooth_setup_page():
    logger.debug("BEGIN")
    device_data = repository.fetch_device_data()
    if device_data != None:
        device_mac_address = device_data[0]
        device_name = device_data[1]
        device_status = "setup complete"
    else:
        device_status = "please setup device"
        device_name="None"
        device_mac_address="None"

    messages = get_flashed_messages()


    logger.debug("END")

    return render_template(
        'bluetooth-config.html', 
        SETUP_STATUS=device_status, 
        MACADDRESS=device_mac_address, 
        DEVICE_NAME=device_name,
        messages = messages
        )


@app.route('/bluetooth-setup/start')
def bluetooth_setup_execute():
    logger.debug("BEGIN")

    #repository.setup_watch_device()
    logger.debug("Searching for new device")
    watch = Twatch()
    watch.search_mac_address()

    logger.debug(f'Using watch {watch.bluetooth_id} with MAC: {watch.bluetooth_mac}')

    device_name = watch.get_bluetooth_id()
    device_mac_address = watch.get_bluetooth_mac()
    if device_name == "" or device_mac_address == "":
        logger.debug(f'Unable to find the bluetooth device')

    else:
        logger.debug(f'Updating device entry: {device_name}')
        repository.update_watch_data(device_mac_address, device_name)
        
    logger.debug("END")

    return redirect(url_for('bluetooth_setup_page'))

def bluetooth_sync_routine():

    logger.debug("BEGIN")
    #repository.setup_watch_device()
    watch = Twatch()

    logger.debug(f'Using watch {watch.bluetooth_id} with MAC: {watch.bluetooth_mac}')

    data_json = watch.get_trip_data(return_only_new_trips=True, mark_when_synced=True)

    for trip in data_json:
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
            #print(date)
            #print(avg_speed)
            #print(distance)
            #print(steps)
            #print(calories)
        except:
            #print("failed")
            logger.debug("Failed to add entry for unknown reason.")
            continue

        logger.debug("Entry parsed succesfully. Adding entry.")
        repository.add_entry(entry)
        logger.debug("END")

@app.route('/bluetooth-setup/poll')
def bluetooth_poll_data():
    logger.debug("BEGIN")

    try:
        bluetooth_sync_routine()
        flash("Bluetooth polling finished successfully", "success")
    except Exception as e:
        flash(f'Bluetooth polling failed: {e}', "danger")
    
    logger.debug("END")

    return redirect(url_for('bluetooth_setup_page'))
