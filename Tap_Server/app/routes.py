import sys
[sys.path.append(i) for i in ['.', '..']]

from app import app
from app.tap_api import Tap_Handler
from flask import render_template, flash, redirect, url_for, request
from app.form import TapForm
from libs.comms.client import Client
from libs.models.transaction import Transaction


client = Client(port=12458) # decide on terminal port later
client_handler = Tap_Handler("tap")
client.start()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    route_charge = randint(3, 10)
    route_num = int((request.base_url.split(":")[2]).split("/")[0])
    form = TapForm()
    if form.validate_on_submit():
        account_no = int(form.account_no.data)
        flash('Tap Successful, Trip charge: {}'.format(route_charge))
        
        data = client_handler.package_request(account_no, float(route_charge))
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

def send_transaction(data):
    client.send(data)