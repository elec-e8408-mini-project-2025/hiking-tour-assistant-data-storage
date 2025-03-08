import logging
import uuid
from app import app
from flask import render_template, redirect, url_for

from entity.tracking_data import TrackingDataEntry

from repository.tracking_data_repository import default_tracking_data_repository as repository


@app.route('/')
def main():
    logging.debug("BEGIN")

    top_distance = repository.top_entry_for_distance()
    top_speed = repository.top_entry_for_speed()
    last_route = repository.fetch_last_entry()

    # Averages: distance, speed, steps, calories
    average_values = repository.fetch_avg_data()
    print(top_distance)

    logging.debug("END")

    return render_template('index.html', top_distance=top_distance, top_speed=top_speed, last_route=last_route, average_values=average_values)



@app.route('/hikes')
def hikes_list():
    logging.debug("BEGIN")

    columns, rows = repository.fetch_all_tracking_data()


    logging.debug("END")

    return render_template('hikes.html', columns=columns, rows=rows)


@app.route('/config')
def config():
    logging.debug("BEGIN")

    logging.debug("END")

    return render_template('config.html')


@app.route('/hike/<int:hikeid>', methods=['POST'])
def hikes_views(hikeid):
    logging.debug("BEGIN")

    repository.delete_hike(hikeid)

    logging.debug("END")

    return redirect(url_for('hikes_list'))

@app.route('/bluetooth-setup')
def bluetooth_setup():
    logging.debug("BEGIN")
    device_data = repository.fetch_device_data()
    if device_data != None:
        device_mac_address = device_data[0]
        device_name = device_data[1]
        device_status = "setup complete"
    else:
        device_status = "please setup device"
        device_name="None"
        device_mac_address="None"


    logging.debug("END")

    return render_template('bluetooth-config.html', SETUP_STATUS=device_status, MACADDRESS=device_mac_address, DEVICE_NAME=device_name)


@app.route('/bluetooth-setup/start')
def bluetooth_setup_execute():
    logging.debug("BEGIN")

    repository.setup_watch_device()

    logging.debug("END")

    return redirect(url_for('bluetooth_setup'))