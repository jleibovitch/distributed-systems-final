import sys

[sys.path.append(i) for i in ['.', '..']]

import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from . import app, db, bcrypt
from .forms import RegistrationForm, LoginForm, UpdateAccountForm, CardForm
from .models import User, Cards, Transactions
from flask_login import login_user, current_user, logout_user, login_required
from .web_api import Web_Handler
from random import randint
from time import sleep
from libs.comms.client import Client
from uuid import uuid1
from threading import Thread

api: Web_Handler = Web_Handler("web", db)
client: Client = Client(port=12457)


# Web Page routes
@app.route("/")
@app.route("/home")
def home():
    cards = Cards.query.all()
    return render_template('home.html', cards=cards)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    # if the are logged in they cant register so they are sent back to home (they wont even see the register button anyways)
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    print(form.validate_on_submit())
    print(form.errors)
    # checking success of form, if successful hash the password and create user
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # geneate a random id
        account_no = randint(10000, 500000)
        client.send(api.push_account(account_no))

        user = User(account_no=account_no, first_name=form.first_name.data, last_name=form.last_name.data, phone_number=form.phone_number.data, email=form.email.data, password=hashed_password)

        db.session.add(user)
        db.session.commit()
        user_card = Cards(card_name=(user.first_name + " " + user.last_name + "'s Card"), funds=0, author=user)
        db.session.add(user_card)
        db.session.commit()
        # initial_transaction = Transactions(transaction_id=uuid1(), transaction_value=0, account_no=user.account_no)
        # db.session.add(initial_transaction)
        db.session.commit()
        # Green message displayed on top if successful
        flash(f'Account created, now you can log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    # if the are logged in they cant relogin so they are sent back to home (they wont even see the login button anyways)
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()

    if form.validate_on_submit():
        # since email is unique it finds the first email tht matches as there is only one email tht does match
        user = User.query.filter_by(email=form.email.data).first()
        # if the password matches the password of the unique email they are logged in
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # this line redirects them to the page they were previously if they were not logged, takes info from url
            next_page = request.args.get('next')
            # default redirection is home
            return redirect(next_page) if next_page else redirect(url_for('home'))

        else:
            # Red message displayed on top if Unsuccessful
            flash('Login Unsuccessful. Please check your credentials', 'danger')
    # takes em back to login page if unsuccessful
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    # generates a random hex to use as the file name
    random_hex = secrets.token_hex(8)
    # receiving the file extension
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    # setting the path to the profile pics folder wit the filename
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # resizing image so it takes less space
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    # savin the pic
    i.save(picture_path)
    # returning the pictures name (with the extension as well)
    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # if user adds a new profile pic
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        # Updating Username and email
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('you account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/card/new", methods=['GET', 'POST'])
@login_required
def new_card():
    form = CardForm()
    if form.validate_on_submit():
        card = Cards(card_name=form.card_name.data, funds=form.funds.data, author=current_user)
        db.session.add(card)
        db.session.commit()
        flash('Your card has been created', 'success')
        return redirect(url_for('home'))
    return render_template('create_card.html', card_name='New Card', form=form, legend='Add New Card')


@app.route("/card/<card_id>")
def card(card_id):
    card = Cards.query.get_or_404(card_id)
    return render_template('card.html', card_name=card.card_name, card=card)


@app.route("/card/<card_id>/update", methods=['GET', 'POST'])
@login_required
def update_card(card_id):
    card = Cards.query.get_or_404(card_id)
    if card.author != current_user:
        abort(403)
    form = CardForm()
    if form.validate_on_submit():
        # card.card_name = form.card_name.data
        card.funds = card.funds + form.funds.data
        db.session.commit()

        add_transaction = Transactions(transaction_id=str(uuid1()), transaction_value=form.funds.data, account_no=current_user.account_no)
        db.session.add(add_transaction)
        db.session.commit()


        flash('Your funds has been updated', 'success')
        return redirect(url_for('user_cards', first_name=card.author.first_name, last_name=card.author.last_name))

    return render_template('create_card.html', title='Update Card', form=form, legend='Please enter the amount of funds to add')


@app.route("/card/<card_id>/delete", methods=['POST'])
@login_required
def delete_card(card_id):
    card = Cards.query.get_or_404(card_id)
    if card.author != current_user:
        abort(403)
    db.session.delete(card)
    db.session.commit()
    flash('Your card (post) has been deleted', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:first_name> + ' ' + <string:last_name>")
def user_cards(first_name, last_name):
    cards = Cards.query.all()
    user = User.query.filter_by(first_name=first_name, last_name=last_name).first_or_404()
    cards = Cards.query.filter_by(author=user)
    # transactions = Transactions.query.filter_by(account_no=current_user.account_no)
    # transactions = transactions
    return render_template('user_cards.html', cards=cards, user=user )


def start_client():
    client.rx_callback = api.handle_incoming
    client.start()
    client_proc = Thread(target=query_transactions, args=(client, api,))
    client_proc.daemon = True 
    client_proc.start()


def query_transactions(client: Client, api: Web_Handler):
    while True:
        sleep(10)
        users = User.query.all()
        print("getting user transactions")
        for user in users:
            data = api.request_transactions(user.account_no)
            client.send(data)
