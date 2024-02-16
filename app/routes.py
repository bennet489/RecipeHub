from datetime import timezone, datetime
from app import app, db
from flask_login import current_user, login_required
from app.forms import EditProfileForm
from flask import flash, redirect, url_for, request, render_template

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.full_name = form.full_name.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Saved')
        return redirect(url_for('user', full_name=current_user.full_name))
    elif request.method == 'GET':
        form.full_name.data = current_user.full_name
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='edit profile', form=form)

    
