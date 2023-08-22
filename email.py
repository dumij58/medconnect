from flask import render_template, g, current_app
from flask_mail import Mail, Message
from threading import Event, Thread

mail = Mail()
thread_event = Event()

async def send_email(recipient, subject, body):
    message = Message(subject=subject, recipients=[recipient])
    message.html = render_template('email_template.html', subject=subject, body=body)
    mail.send(message)
    return "Email sent!"


"""
def render_email_template(subject, body):
    return render_template('email_template.html', subject=subject, body=body)

async def send_email(recipient, subject, body):
    message = Message(subject=subject, recipients=[recipient])
    message.html = render_email_template(subject, body)

    try:
        thread_event.set()
    except Exception as error:
        return f"Starting thread failed - {error}"
    
    email_thread = Thread(target=mail.send(message))
    email_thread.start()

    try:
        thread_event.clear()
    except Exception as error:
        return f"Stopping thread failed - {error}"
"""