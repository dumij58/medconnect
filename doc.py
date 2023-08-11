from flask import (
    Blueprint, flash, g, redirect, render_template, request, session as flask_session, url_for
)
from markupsafe import escape
from werkzeug.security import generate_password_hash
from datetime import datetime, date

from .helpers import login_required, f_time, f_date
from .models import db, Patient, Doctor, DoctorPreVal, Admin, Log, Hospital, DocSession, Appointment
from .forms import SessionForm

bp = Blueprint('doc', __name__, url_prefix='/doc')


@bp.route('/dash', methods=('GET', 'POST'))
@login_required
def dash():
    apmts = db.session.execute(db.select(Appointment, Patient, Hospital).join(Doctor, Appointment.doc_id == Doctor.id).join(Patient, Appointment.pt_id == Patient.id).join(Hospital, Appointment.hl_id == Hospital.id).where(Doctor.id == g.user.id).where(Appointment.datetime >= datetime.now()).order_by(Appointment.datetime)).all()
    session = db.session.execute(db.select(DocSession, Doctor, Hospital).join(Doctor).join(Hospital).where(DocSession.doc_id == g.user.id).where(DocSession.date >= date.today()).order_by(DocSession.date).order_by(DocSession.start_t)).all()
    return render_template('doc/dash.html', session = session, apmts = apmts)

@bp.route('/sessions', methods=('GET', 'POST'))
@login_required
def sessions():
    form = SessionForm()
    form.hl_id.choices = [ (hl.id, hl.name) for hl in Hospital.query.order_by('name') ]
    showForm = False

    # Ensure data is validated on submit
    if request.method == 'POST':

        if form.validate():
            
            # Add records to database
            new_session = DocSession(
                hl_id = form.hl_id.data,
                doc_id = g.user.id,
                date = form.date.data,
                start_t = form.start_t.data,
                end_t = form.end_t.data
            )
            db.session.add(new_session)

            # Append a remark to log
            append = Log(
                created = datetime.now(),
                user = g.user.username,
                remarks = f"Session (On {f_date(form.date.data)} from {f_time(form.start_t.data)} to {f_time(form.end_t.data)}) added to Doctor ({g.user.username})"
            )
            db.session.add(append)

            # Commit all changes to database
            db.session.commit()
            
            # Flash a message and redirect to login page
            showForm = False
            flash('Session Added!', "success")
    
        else:
            showForm = True

    doc_sessions = db.session.execute(db.select(DocSession, Hospital).join(Hospital).where(DocSession.date >= date.today()).order_by(DocSession.date, DocSession.start_t))
    return render_template('doc/sessions.html', form = form, show = showForm, sessions = doc_sessions)


@bp.route('/sessions/remove/<int:s_id>')
@login_required
def session_remove(s_id):
    doc_session = DocSession.query.filter(DocSession.id == escape(s_id)).first()

    # Append a remark to log
    append = Log(
            created = datetime.now(),
            user = g.user.username,
            remarks = f"Session (On {f_date(doc_session.date)} from {f_time(doc_session.start_t)} to {f_time(doc_session.end_t)}) removed from Doctor ({g.user.username})"
        )
    db.session.add(append)
    
    # Delete the hospital data
    db.session.delete(doc_session)

    # Commit changes into the database
    db.session.commit()

    flash(f'Session removed!','info')
    return redirect(url_for('doc.sessions'))


@bp.route('/apmts', methods=('GET', 'POST'))
@login_required
def apmts():
    apmts = db.session.execute(db.select(Appointment, Patient, Hospital).join(Doctor, Appointment.doc_id == Doctor.id).join(Patient, Appointment.pt_id == Patient.id).join(Hospital, Appointment.hl_id == Hospital.id).where(Doctor.id == g.user.id).order_by(Appointment.datetime)).all()
    print(apmts)
    return render_template('doc/appointments.html', apmts = apmts)