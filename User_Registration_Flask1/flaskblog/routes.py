from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

# dummy data
posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


# Web Page routes
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    # if the are logged in they cant register so they are sent back to home (they wont even see the register button anyways)
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    # checking success of form, if successful hash the password and create user
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
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


@app.route("/account")
@login_required
def account():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file)
