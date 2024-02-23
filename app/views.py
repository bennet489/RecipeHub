from app import app, db
from flask import render_template
from flask_login import login_required, current_user
import sqlalchemy as sa
from app.models import User, Post
from app.forms import EmptyForm
from flask import request, url_for

@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    if current_user.is_authenticated:
        posts = db.paginate(current_user.following_posts(), page=page,
                            per_page=app.config['POSTS_PER_PAGE'], error_out=False)
        next_url = url_for('home', page=posts.next_num) \
            if posts.has_next else None
        prev_url = url_for('home', page=posts.prev_num) \
            if posts.has_prev else None
        return render_template('home.html', title='Home',
                               posts=posts.items, next_url=next_url,
                               prev_url=prev_url)
    else:
        # Handle case where user is not authenticated
        # For example, you can simply render the home page without following posts
        query = sa.select(Post).order_by(Post.timestamp.desc())
        posts = db.paginate(query, page=page,
                            per_page=app.config['POSTS_PER_PAGE'], error_out=False)
        next_url = url_for('home', page=posts.next_num) \
            if posts.has_next else None
        prev_url = url_for('home', page=posts.prev_num) \
            if posts.has_prev else None
        return render_template('home.html', title='Home',
                               posts=posts.items, next_url=next_url,
                               prev_url=prev_url)

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    form = EmptyForm()
    return render_template('account.html', user=user)

@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Post).order_by(Post.timestamp.desc())
    posts = db.paginate(query, page=page,
                        per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template("home.html", title='Explore', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)