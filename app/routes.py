from PIL import Image
from datetime import timezone, datetime
from app import app, db
from flask_login import current_user, login_required
from app.forms import EditProfileForm, EmptyForm
from flask import flash, redirect, url_for, request, render_template
import sqlalchemy as sa
from app.models import User, Post
from app.forms import PostForm,  UpdateAccountForm
import os
import secrets

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Saved')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='edit profile', form=form)

    
@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == user))
        if user is None:
            flash('User {username} not found.')
            return redirect(url_for('home'))
        if user == current_user:
            flash('you cannot follow yourself')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('you are following {username}')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('home'))
    
@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username))
        if user is None:
            flash('User {username} not found')
            return redirect(url_for('home'))
        if user == current_user:
            flash('you cannot unfollow yourself')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {username}')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('home'))
    
@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        image_file = form.image.data
        if image_file:
            image_filename = save_picture(image_file)
            post = Post(title=form.title.data, content=form.content.data, image_url=image_filename, author=current_user)
        else:
            post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post created', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images/profile_image', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def user_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('user_account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        image_file = url_for('static', filename='images/profile_image/' + current_user.image_file)
    return render_template('user_account.html', title='Account',
                           image_file=image_file, form=form, user=current_user)