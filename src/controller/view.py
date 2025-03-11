from app import logger
import uuid
from app import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from twatch_controller.twatch_controller import bluetooth_sync_routine
from twatch_controller.t_watch import Twatch


from repository.tracking_data_repository import default_tracking_data_repository as repository


@app.route('/')
def main():
    """
        Prepares and renders the main view template of the web application

        The function fetches top hiking trip data from repository
        which is then populated in the rendered view
    """
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
    """
        Prepares and renders the hikes template. The view
        contains data from all hikes in persistent memory
    """
    logger.debug("BEGIN")

    columns, rows = repository.fetch_all_tracking_data()


    logger.debug("END")

    return render_template('hikes.html', columns=columns, rows=rows)


@app.route('/hike/<int:hikeid>', methods=['POST'])
def hikes_views(hikeid):
    """
        Handles deletion of a selected hike
        The delete request is sent with a POST request
    """
    logger.debug("BEGIN")

    repository.delete_hike(hikeid)

    logger.debug("END")

    return redirect(url_for('hikes_list'))

@app.route('/bluetooth-setup')
def bluetooth_setup_page():
    """
        Renders the bluetooth configuration template view
    """
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
    """Handles the pairing of a new LilyGO T-Watch"""
    
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

@app.route('/bluetooth-setup/poll')
def bluetooth_poll_data():
    """
        Handles the synchronization of hiking session data from 
        the LilyGO T-Watch to the persistent storage of the 
        Web Application
    """
    logger.debug("BEGIN")

    try:
        bluetooth_sync_routine()
        flash("Bluetooth polling finished successfully", "success")
    except Exception as e:
        flash(f'Bluetooth polling failed: {e}', "danger")
    
    logger.debug("END")

    return redirect(url_for('bluetooth_setup_page'))
