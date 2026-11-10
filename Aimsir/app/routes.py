#import datetime to timestamp new sightings
from datetime import datetime
#import hmac to compare passwords safely
import hmac
#import the render template, redirect and the url_for functions from the flask
#session remembers who is logged in, request is used to read the ?next= address
from flask import render_template, redirect, url_for, flash, session, request
#import the app and database variables from the app package
from app import app, db
#import the forms from the forms.py file
from app.forms import LoginForm, SightingForm
#import the models to check logins and save sightings in the database
from app.models import User, Sighting


# only allow redirects to pages inside this app (stops redirects to other websites)
def is_safe_next(target):
    return bool(target) and target.startswith('/') and not target.startswith('//') and '\\' not in target


# template filter: show '2025-12-30 15:35' as '30 Dec 2025, 15:35'
@app.template_filter('nice_date')
def nice_date(value):
    try:
        return datetime.strptime(value, '%Y-%m-%d %H:%M').strftime('%d %b %Y, %H:%M').lstrip('0')
    except (TypeError, ValueError):
        return value  # leave anything unexpected as it is

#create the association for the URL
@app.route('/')
#create the association for the index
@app.route('/index')
def index():
    user = {'username': session.get('userid', 'Guest')}
    # newest first, only the 10 latest reports
    # if sightings occured on the same date, the sighting id will be used to sort.
    recentSightings = (
        Sighting.query
        .order_by(Sighting.s_datetime.desc(), Sighting.sighting_id.desc())
        .limit(9)
        .all()
    )
    return render_template('index.html', title='Home', user=user, recentSightings=recentSightings)


@app.route('/about')
def about():
    return render_template('aboutus.html', title='About Us')

#this is the app route for the login page
@app.route('/login', methods=['GET', 'POST'])
#the login page to display in web form
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(userid=form.username.data.strip()).first()
        if user is None or not hmac.compare_digest(user.password, form.password.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('login', next=request.args.get('next')))
        # remember the logged in user for the following requests
        session.clear()
        session['userid'] = user.userid
        session.permanent = form.remember_me.data
        flash('Welcome, ' + user.userid + '!', 'success')
        next_page = request.args.get('next')
        if is_safe_next(next_page):
            return redirect(next_page)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

#this is the app route to log the user out
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been signed out', 'success')
    return redirect(url_for('index'))

#this is to create an association for the sightings
@app.route('/sightings', methods=['GET', 'POST'])
#the page to create weather evetnss
def sightings():
    # a sighting belongs to the logged in user, so the user must sign in first
    userid = session.get('userid')
    if userid is None:
        flash('Please sign in to report a sighting', 'error')
        return redirect(url_for('login', next=url_for('sightings')))
    user = db.session.get(User, userid)
    if user is None:
        session.clear()
        flash('Your account was not found, please sign in again', 'error')
        return redirect(url_for('login'))

    form = SightingForm()
    if form.validate_on_submit():
        last = Sighting.query.order_by(Sighting.sighting_id.desc()).first()
        next_number = int(last.sighting_id[1:]) + 1 if last else 1
        sighting = Sighting(
            sighting_id='S' + str(next_number).zfill(4),
            s_datetime=datetime.now().strftime('%Y-%m-%d %H:%M'),
            s_city=form.city.data,
            s_weather_type=form.weather_type.data,
            summary=form.summary.data,
            userid=user.userid
        )
        db.session.add(sighting)
        db.session.commit()
        flash('Sighting reported', 'success')
        return redirect(url_for('index'))
    return render_template('sightings.html', title='Report Weather Sighting', form=form)
