### IMPORTS
from datetime import datetime
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
# association table for multi-product cart
order_product = db.Table(
    'order_product',
    db.Column(
            'order_id', 
            db.Integer, 
            db.ForeignKey('order.id'),
            primary_key=True
            ),
    db.Column(
            'product_id', 
            db.Integer, 
            db.ForeignKey('product.id'),
            primary_key=True
            )
    )
    
# customers
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
                        db.String(50), 
                        nullable=False
                    )

    orders = db.relationship('Order', backref='customer')

# orders
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(
                        db.Datetime, 
                        nullable=False, 
                        default=datetime.utcnow
                    )
    customer_id = db.Column(
                        db.Integer, 
                        db.ForeignKey('customer.id'), 
                        nullable=False
                    )
    
    products = db.Relationship('Product', secondary=order_product)

# products
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    prince = db.Column(db.Float)




### ROUTES