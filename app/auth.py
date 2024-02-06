from flask import render_template, request, flash, redirect, url_for
from .models import User
from app.forms import RegistrationForm, LoginForm
from app.models import User
from . import db, app, bcrypt
from flask_login import login_user, current_user


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='signUp', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit:
        pass
    return render_template('login.html', title='login')    