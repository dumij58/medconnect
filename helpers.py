import functools

from flask import redirect, url_for, render_template, g
from datetime import datetime, date, timedelta

from .models import db, Admin, Hospital, Doctor, DocSession
from .forms import SessionForm

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


def admin_only(view):
    @login_required
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not Admin.query.filter(Admin.username == g.user.username).first():
            return render_template('error.html', e_code = 403, e_text = "Access Denied")

        return view(**kwargs)

    return wrapped_view


def calc_total_apmts(date, start_t, end_t):
    # Combine doc session date with start and end times 
    # (datetime's time objects can't calculate a timedelta, but datetime and date objects can)
    start_dt = datetime.combine(date, start_t)
    end_dt = datetime.combine(date, end_t)
    
    # Get total appointments for a session (if each appointment is 20 minutes)
    total = int((abs(end_dt - start_dt).total_seconds() // 60) // 20)
    return total


def f_phone_no(number):
    return f"+{str(int(number))}"

def f_gender(gender):
    if gender == "f":
        return "Female"
    if gender == "m":
        return "Male"
    if gender == "o":
        return "Other"

def f_dr(doc):
    return f"Dr. {doc}"

def f_age(dob):
    age = int(abs(date.today() - dob).days) // 365
    return age
    
def f_datetime(dt):
    return '{:%Y-%m-%d %H:%M:%S %p}'.format(dt)

def f_dtNoS(dt):
    return '{:%Y-%m-%d %I:%M %p}'.format(dt)

def f_dtNoS_wDay(dt):
    return '{:%Y-%m-%d - %a %I:%M %p}'.format(dt)

def f_date(d):
    return '{:%Y-%m-%d}'.format(d)

def f_time(t):
    return '{:%I:%M:%S %p}'.format(t)

def f_timeNoS(t):
    return '{:%I:%M %p}'.format(t)

def f_mins(td):
    return '{:%M}'.format(td)