### IMPORTS
from datetime import date, datetime
from operator import imod
from tracemalloc import start
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
import random
from datetime import timedelta

### GLOBAL
# instatiate the Flask app/object
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# instatiate the FlaskSQLAlchemy object
db = SQLAlchemy(app)

fake = Faker()

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
                        db.DateTime, 
                        nullable=False, 
                        default=datetime.utcnow
                    )
    customer_id = db.Column(
                        db.Integer, 
                        db.ForeignKey('customer.id'), 
                        nullable=False
                    )
    
    products = db.relationship('Product', secondary=order_product)

# products
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Float)


### HELPER
### create dummy data
def add_customers():
    for i in range(100):
        fake_name = fake.name().lower()
        first_name_initial = fake_name.split()[0][0]
        last_name = fake_name.split()[1]
        
        customer = Customer(
            username = first_name_initial + last_name
        )
        db.session.add(customer)
    db.session.commit()


def add_products():
    for i in range(100):
        product_name = fake.color_name()
        product_price = price = round(random.uniform(0.99, 9.99), 2)
        product = Product(
            name = product_name,
            price = product_price
        )
        db.session.add(product)
    db.session.commit()
    

def add_orders():
    customers = Customer.query.all()
    products = Product.query.all()

    for i in range(100):
        random_customer = random.choice(customers)
        
        random_int = random.randint(1, 5)
        random_producs = random.sample(products, random_int)
        
        random_date = fake.date_this_year()

        order = Order(
            order_date = random_date,
            customer_id = random_customer.id,
            products = random_producs
        )
        db.session.add(order)
    db.session.commit()
    

##### Helpers driver
# add_customers()
# add_products()
# add_orders()

### ROUTES
def get_order_by_id(customer_id=1):
    customer_orders = Order.query.filter_by(
                                    customer_id=customer_id
                                ).all()

    for order in customer_orders:
        print(f"\n{order.customer.username}'s order: {order.order_date}")
        for n, product in enumerate(order.products, start=1):
            print(f"#{n} item ordered: {product.name} -- {product.price}")


def get_sorted_orders(customer_id=1):
    customer_orders = Order.query.filter_by(
                                    customer_id=customer_id
                                ).order_by(
                                    Order.order_date.asc()
                                ).all()
    
    for order in customer_orders:
        print(order.order_date)


def revenue_for_n_days(n=30):
    print(f"Revenue for last {n} days:")
    current_datetime = datetime.now()
    a_month_ago = current_datetime - timedelta(n)
    usd = db.session.query(
                            db.func.sum(Product.price)
                        ).join(
                            order_product
                        ).join(
                            Order
                        ).filter(
                            Order.order_date > a_month_ago
                        ).scalar()
    print("${:,}".format(round(usd, 2)))


def best_customers(threshold=100):
    best = db.session.query(
                            Customer
                        ).join(
                            Order
                        ).join(
                            order_product
                        ).join(
                            Product
                        ).group_by(
                            Customer
                        ).having(
                            db.func.sum(Product.price) > threshold
                        ).all()
    
    print(f"{len(best)} customers that have spent ${threshold}.00 or more:")

    for n, customer in enumerate(best, start=1):
        print(n, customer.username)


# best_customers()
best_customers(25)
# best_customers(50)