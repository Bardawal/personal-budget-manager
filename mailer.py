from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Mail instance
mailer = Mail()

def setup_mail(app):
    # Configure mail settings
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

    # Bind mailer to Flask app
    mailer.init_app(app)

def dispatch_email(recipient, subject_line, content):
    # Create and send email message
    message = Message(
        subject=subject_line,
        sender=os.getenv("MAIL_USERNAME"),
        recipients=[recipient]
    )
    message.body = content
    mailer.send(message)
