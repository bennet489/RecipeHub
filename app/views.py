from app import app, db
from flask import render_template
from flask_login import login_required, current_user
import sqlalchemy as sa
from app.models import User, Post
from app.forms import EmptyForm

@app.route('/')
@app.route('/home')
def home():
    posts = db.session.scalars(current_user.following_posts()).all()
    return render_template('home.html', title='Home', posts=posts)

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    form = EmptyForm()
    return render_template('account.html', user=user)

@app.route('/explore')
@login_required
def explore():
    query = sa.select(Post).order_by(Post.timestamp.desc())
    posts = db.session.scalars(query).all()
    return render_template('home.html', title='Explore', posts=posts)