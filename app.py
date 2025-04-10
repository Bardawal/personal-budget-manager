from flask import Flask
from flask_cors import CORS
from app.database import db
from .main import routes
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create Flask application
app = Flask(__name__)
CORS(app)

# Configure database connection
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database with app
db.init_app(app)

# Register application routes
app.register_blueprint(routes)

# Start the app and create DB tables if not existing
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
