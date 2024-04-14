from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User, Post
from  app.users.forms import (RegistrationForm, LoginForm, EditProfileForm,
                                   RequestResetForm, ResetPasswordForm, EmptyForm)
from app.users.utils import save_picture, send_reset_email
from urllib.parse import urlsplit
import sqlalchemy as sa
from datetime import datetime, timezone

users = Blueprint('users', __name__)


@users.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

 # Login route
@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = LoginForm()
    if form. validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'error')
            return redirect(url_for('users.login'))
        else:
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or urlsplit(next_page).netloc != '':
                next_page = url_for('views.home')
                return redirect(next_page)
            flash('Login successfull')
            return redirect(url_for('views.home'))
    return render_template('login.html', title='login', form=form)

# Register route
@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created, pls login', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='register', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def user_account():
    form = EditProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('user.user_account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        image = url_for('static', filename='images/profile_image/' + current_user.image)
    return render_template('user_account.html', title='Account',
                           image=image, form=form, user=current_user)

@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Saved')
        return redirect(url_for('users.user_account', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='edit profile', form=form)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('view.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to change your password.', 'info')
        return redirect(url_for('user.login'))
    return render_template('change_password.html', title='Change Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('view.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('user.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('user.login'))
    return render_template('reset_token.html', title='Change Password', form=form)



@users.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == user))
        if user is None:
            flash('User not found.', 'danger')
            return redirect(url_for('views.home'))
        if user == current_user:
            flash('you cannot follow yourself')
            return redirect(url_for('users.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('you are following {username}')
        return redirect(url_for('user.user', username=username))
    else:
        return redirect(url_for('views.home'))
    
@users.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username))
        if user is None:
            flash('User {username} not found')
            return redirect(url_for('views.home'))
        if user == current_user:
            flash('you cannot unfollow yourself')
            return redirect(url_for('user.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {username}')
        return redirect(url_for('user.user_account', username=username))
    else:
        return redirect(url_for('views.home'))