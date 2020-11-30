import sys
[sys.path.append(i) for i in ['.', '..']]

from app import app
from flask import render_template, flash, redirect, url_for, request
from app.form import Btn
from app.models import Transaction, terminal_location
from datetime import datetime
from random import randint
from os import getenv
from libs.comms.client import Client
from libs.comms.message import Message

client = Client("0.0.0.0", terminal_location)
client.run()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    route_charge = randint(3, 10)
    route_num = int((request.base_url.split(":")[2]).split("/")[0])
    form = Btn()
    transaction = Transaction()
    if form.validate_on_submit():
        current_balance = transaction.starting_balance - route_charge
        
        flash('Account Number: {}'.format(transaction.account_num))
        flash('Customer starting balance: {}'.format(transaction.starting_balance))
        flash('Customer current balance: {}'.format(current_balance))
        flash('Transaction sent to terminal server for caching')

        data = [route_num, transaction.account_num, transaction.starting_balance, route_charge, datetime.utcnow()]
        data = package_data(data)
        send_transaction(data)

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

def package_data(data):
    values = {}
    values["Tap_Node_id"] = data[0]
    values["Account_Number"] = str(data[1])
    values["Original_Balance"] = data[2]
    values["Trip_Charge"] = data[3]
    values["Transaction_Timestamp"] = str(data[4])
    return values

def send_transaction(data):
    try:
        client.send(Message("Tap_Node", data, "Insert_Transaction").to_json().encode("UTF-8"))
    except:
        print("Error, cannot connect to the server")