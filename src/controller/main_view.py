import logging
import uuid
from app import app
from flask import render_template

from entity.tracking_data import TrackingDataEntry

from repository.tracking_data_repository import default_tracking_data_repository as repository


@app.route('/')
def hello():
    logging.debug("BEGIN")

    columns, rows = repository.fetch_all_tracking_data()

    top_route = repository.fetch_top_entry()
    print(top_route)

    logging.debug("END")

    return render_template('index.html', columns=columns, rows=rows, top=top_route)
