from app import app, db
from flask import render_template
from flask_login import login_required
import sqlalchemy as sa
from app.models import User

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/user/<full_name>')
@login_required
def user(full_name):
    user = db.first_or_404(sa.select(User).where(User.full_name == full_name))
    return render_template('user.html', user=user)