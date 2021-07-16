from flask_mail import Message
from app import mail, app   
from flask import render_template
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()
    
def send_password_reset_email(user):
    token = user.get_password_reset_token()
    send_email('Movie Box : Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))
    
def email_verification(user):
    token = user.get_verify_email_token()
    send_email('Movie Box : Verify Your Email ',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               html_body=render_template('email/email_conformation.html', user=user, token=token))