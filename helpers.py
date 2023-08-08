import functools

from flask import redirect, url_for, render_template, g
from .models import Admin, Hospital
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


def select_hospital(request, id):
    hospital = None
    form = SessionForm(request.POST, obj = hospital)
    form.hl_id.choices = [ (hl.id, hl.name) for hl in Hospital.query.order_by('name') ]


def f_phone_no(number):
    return f"+{str(int(number))}"

def f_gender(gender):
    if gender == "f":
        return "Female"
    if gender == "m":
        return "Male"
    
def f_hospital(hl_id):
    hl = Hospital.query.filter(Hospital.id == hl_id).first()
    return hl.name
    
def f_datetime(dt):
    return '{:%Y-%m-%d %H:%M:%S}'.format(dt)

def f_date(d):
    return '{:%Y-%m-%d}'.format(d)

def f_time(t):
    return '{:%H:%M:%S}'.format(t)

def f_timeNoS(t):
    return '{:%H:%M}'.format(t)