from flask import render_template, current_app
from flask_mail import Mail, Message

mail = Mail()

def send_email(recipient, subject, body):
    with current_app.app_context():
        message = Message(subject=subject, recipients=[recipient])
        message.html = render_template('email_template.html', subject=subject, body=body)
        mail.send(message)
