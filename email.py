from flask import Flask,render_template, g, current_app
from flask_mail import Mail, Message
from celery import Celery, Task

mail = Mail()

def send_email(recipient, subject, body):
    with current_app.app_context():
        message = Message(subject=subject, recipients=[recipient])
        message.html = render_template('email_template.html', subject=subject, body=body)
        mail.send(message)
