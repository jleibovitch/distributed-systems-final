"""
routes.py
Author: Umar Ehsan

The purpose of this class is to provide routes functionality for flask server (REST API)
"""

import sys
[sys.path.append(i) for i in ['.', '..']]

from app import app
from app.tap_api import Tap_Handler
from flask import render_template, flash, redirect, url_for, request
from app.form import TapForm
from libs.comms.client import Client
from random import randint
from sys import argv

client_handler = None
client = None
port_number = 12458 if len(argv) < 3 else int(argv[2])

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    global client_handler
    route_charge = -1 * randint(3, 10)
    route_num = int((request.base_url.split(":")[2]).split("/")[0])
    form = TapForm()
    if form.validate_on_submit():
        account_no = int(form.account_no.data)
        flash('Tap Successful, Trip charge: {}'.format(route_charge))
        
        data = client_handler.package_request(account_no, port_number, float(route_charge)) # terminal server port number is used for location number
        send_transaction(data)

        flash('Transaction sent to terminal server for caching')
        return redirect(url_for('index'))

    return render_template('index.html', route_num=route_num, form=form)

@app.route('/stop')
def shutdown():
    shutdown_routine = request.environ.get('werkzeug.server.shutdown')
    if shutdown_routine is None:
        raise RuntimeError('Not running werkzeug')
    shutdown_routine()
    client.shutdown()
    return "Shutting down..."

def start_client():
    global client_handler, client
    client = Client(port=port_number) # decide on terminal port later
    client_handler = Tap_Handler("tap")
    client.start()

def send_transaction(data):
    global client
    client.send(data)

start_client()
