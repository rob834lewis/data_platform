# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------------------------------------------------
Written by      : Rob Lewis

Date            : 20OCT2025

Purpose         : Coffee Ordering App

Dependencies    :

Program name    : coffee_app

Modifications
-------------
20OCT2025   RLEWIS  Initial Version
----------------------------------------------------------------------------------------------------------------------
"""

from flask import Flask, render_template, request, redirect, url_for, session, g, jsonify
import os
import uuid # for generating user id
import logging
import sqlite3
import datetime
import time
from functools import wraps

# ---------------
# --- Logging ---
# ---------------

log_file = '/srv/data-coven/src/logs/coffee_app.log' # file for storing log

logging.basicConfig(
    level    = logging.INFO                               ,
    format   = '%(asctime)s - %(levelname)s - %(message)s',
    filename = log_file                                   ,
    filemode = 'a'
)

# console handler to enable logging to appear in the output window
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(console_handler)

logging.info(f"Application stating up...")

# --------------------------
# --- Application Config ---
# --------------------------

app = Flask(__name__,template_folder='/srv/data-coven/src/apps/coffee_order/templates')

# this key is used to sign the session cookie. Would need to be changed in a production environment
app.secret_key = 'a_very_secret_key_for_coffee_app' 

# -----------------------
# --- Database Config ---
# -----------------------

DATABASE = 'coffee_orders.db' # The local file where all data will be stored

def get_db_connection():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # This allows accessing columns by name
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db_connection()
        # Create the orders table if it doesn't exist
        db.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                coffee_name TEXT NOT NULL,
                coffee_price REAL NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        db.commit()

# Initialize the database on startup
init_db()
logging.info("SQLite database initialized and checked.")


# ---------------
# --- Classes ---
# ---------------

# coffee menu
class Coffee:

    def __init__(self, id, name, price, description):
        self.id          = id
        self.name        = name
        self.price       = price
        self.description = description

# customer order
class Order:
    def __init__(self, user_id, coffee_name, coffee_price):
        self.user_id = user_id
        self.coffee_name = coffee_name
        self.coffee_price = coffee_price
        self.created_at = datetime.datetime.now().isoformat()

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'coffee_name': self.coffee_name,
            'coffee_price': self.coffee_price,
            'created_at': self.created_at
        }


# ---
# --- Sample Coffee Menu
# ---

# available coffees
coffees = [
    Coffee(1, "Espresso"   , 2.50, "A strong, concentrated coffee beverage."                  ),
    Coffee(2, "Flat White" , 3.75, "Espresso with steamed milk and a thin layer of microfoam."),
    Coffee(3, "Americano"  , 3.20, "Espresso shots diluted with hot water."                   ),
    Coffee(4, "Cappuccino" , 3.90, "Equal parts espresso, steamed milk, and foamed milk."     ),
    Coffee(5, "Latte"      , 3.90, "Espresso with hot steamed milk, milder than Flat White."     )
]

# find coffee function
def find_coffee_by_id(coffee_id):
    try:
        coffee_id = int(coffee_id)
        return next((c for c in coffees if c.id == coffee_id), None)
    except ValueError:
        return None

# ---
# --- Helper Functions
# ---

def get_current_user_id():
    # Uses the session data set during login
    return session.get('user_id')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if get_current_user_id() is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# ---
# --- Routes and Logic
# ---


@app.route('/')
def index():
    user_id = get_current_user_id()
    return render_template('index.html', coffees=coffees, user_id=user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user_name = request.form.get('username')
        if user_name and user_name.strip():
            session['user_id'] = user_name.strip()
            logging.info(f"User logged in: {user_name.strip()}")
            # Redirect to the dashboard or the page they were trying to access
            next_page = request.args.get('next') or url_for('dashboard')
            return redirect(next_page)
        else:
            error = "Please enter a valid name."
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    user_id = get_current_user_id()
    if user_id:
        session.pop('user_id', None)
        logging.info(f"User logged out: {user_id}")
    return redirect(url_for('index'))


@app.route('/order', methods=['POST'])
@login_required
def place_order():
    user_id = get_current_user_id()
    coffee_id = request.form.get('coffee_id')
    
    coffee = find_coffee_by_id(coffee_id)

    if not coffee:
        logging.error(f"Order failed: Coffee ID {coffee_id} not found.")
        return "Error: Coffee not found.", 404

    # Create the new Order object
    new_order = Order(user_id, coffee.name, coffee.price)
    order_data = new_order.to_dict()

    # --- SQLite Database Save ---
    try:
        db = get_db_connection()
        db.execute(
            'INSERT INTO orders (user_id, coffee_name, coffee_price, created_at) VALUES (?, ?, ?, ?)',
            (order_data['user_id'], order_data['coffee_name'], order_data['coffee_price'], order_data['created_at'])
        )
        db.commit()
        logging.info(f"Order placed successfully for {user_id}: {coffee.name} (Saved to SQLite)")
        # Get the ID of the last inserted row
        order_row = db.execute('SELECT last_insert_rowid()').fetchone()
        order_id = order_row[0]
        
        return redirect(url_for('order_success', order_id=order_id))

    except sqlite3.Error as e:
        logging.error(f"Database error during order placement for {user_id}: {e}")
        return render_template('error.html', message="Database connection error. Order failed.")


@app.route('/order_success/<int:order_id>')
@login_required
def order_success(order_id):
    user_id = get_current_user_id()
    
    try:
        db = get_db_connection()
        order_row = db.execute(
            'SELECT * FROM orders WHERE id = ? AND user_id = ?',
            (order_id, user_id)
        ).fetchone()

        if order_row:
            order = {
                'id': order_row['id'],
                'user_id': order_row['user_id'],
                'coffee_name': order_row['coffee_name'],
                'coffee_price': order_row['coffee_price'],
                'created_at': order_row['created_at']
            }
            return render_template('success.html', order=order)
        else:
            logging.warning(f"Order ID {order_id} not found for user {user_id}")
            return "Order not found or access denied.", 404

    except sqlite3.Error as e:
        logging.error(f"Database error during order lookup: {e}")
        return render_template('error.html', message="Could not retrieve order details.")


@app.route('/dashboard')
@login_required
def dashboard():
    user_id = get_current_user_id()
    orders = []

    try:
        db = get_db_connection()
        rows = db.execute(
            'SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC',
            (user_id,)
        ).fetchall()
        
        # Convert sqlite3.Row objects to standard dictionaries for template
        orders = [{
            'id': row['id'], 
            'coffee_name': row['coffee_name'], 
            'coffee_price': row['coffee_price'], 
            'created_at': row['created_at']
        } for row in rows]
        
    except sqlite3.Error as e:
        logging.error(f"Database error during dashboard retrieval for {user_id}: {e}")
        # orders list remains empty, and the template handles it

    return render_template('dashboard.html', user_id=user_id, orders=orders)


@app.route('/recent_orders')
#@login_required
def recent_orders():
    try:
        db = get_db_connection()
        rows = db.execute(
            'SELECT * FROM orders ORDER BY id DESC LIMIT 20'
        ).fetchall()

        orders = [{
            'id': row['id'],
            'user_id': row['user_id'],
            'coffee_name': row['coffee_name'],
            'coffee_price': row['coffee_price'],
            'created_at': row['created_at']
        } for row in rows]

        return {'orders': orders}

    except sqlite3.Error as e:
        logging.error(f"Database error during recent orders fetch: {e}")
        return {'orders': []}, 500



@app.route('/live_dashboard')
#@login_required
def live_dashboard():
    return render_template('live_dashboard.html')


# ---
# Run the app
# ---

if __name__ == '__main__':
    # When you run this file directly, it starts the web server

    # debug=True allows the server to automatically reload when you make changes
    app.run(host="0.0.0.0", port=5000, debug=True)