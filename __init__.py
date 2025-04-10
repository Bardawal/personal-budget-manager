from flask import Flask
from .database import init_db, db
from .mailer import init_mail
from .main import routes

def build_app():
    # Initialize the Flask app
    application = Flask(__name__)

    # Set up database and mail configurations
    init_db(application)
    init_mail(application)

    # Create database tables within the app context
    with application.app_context():
        db.create_all()

    # Attach route handlers
    application.register_blueprint(routes)

    return application
