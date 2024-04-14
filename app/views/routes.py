from flask import render_template, request, Blueprint, url_for
from app.models import Post
from flask_login import login_required
import sqlalchemy as sa
from app.models import db
import app

views = Blueprint('views', __name__)


@views.route("/")
@views.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@views.route('/explore')
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