### IMPORTS
from datetime import datetime
from email.policy import default
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


### GLOBAL
# instatiate the Flask app/object
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# instatiate the FlaskSQLAlchemy object
db = SQLAlchemy(app)


### MODELS
# customers
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)

# orders
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.Datetime, nullable=False, default=datetime.utcnow)


### ROUTES