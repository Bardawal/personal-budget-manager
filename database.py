from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Create a SQLAlchemy instance
db = SQLAlchemy()

def setup_database(app):
    # Fetch database configuration from environment
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")

    # Define the connection string
    connection_url = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}"

    # Set configuration for the Flask app
    app.config["SQLALCHEMY_DATABASE_URI"] = connection_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Bind SQLAlchemy to the app
    db.init_app(app)
