from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')
bcrypt = Bcrypt(app)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': os.getenv('DB_PORT', '3306')
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_tables():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # First, drop the table if it exists to avoid conflicts
            cursor.execute("DROP TABLE IF EXISTS User")
            
            # Then create the table with proper auto-increment settings
            cursor.execute("""
                CREATE TABLE User (
                    UserID INT NOT NULL AUTO_INCREMENT,
                    name VARCHAR(100) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    phone VARCHAR(20),
                    PRIMARY KEY (UserID)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            connection.commit()
            print("Table 'User' created successfully")
        except Error as e:
            print(f"Error creating table: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form.get('phone', '')
        
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(
                    """
                    INSERT INTO User (name, email, password, phone) 
                    VALUES (%s, %s, %s, %s)
                    """,
                    (name, email, hashed_password, phone)
                )
                connection.commit()
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))
            except Error as e:
                flash(f'Error: {e}', 'danger')
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM User WHERE email = %s", (email,))
                user = cursor.fetchone()
                
                if user and bcrypt.check_password_hash(user['password'], password):
                    session['user_id'] = user['UserID']
                    session['user_name'] = user['name']
                    return redirect('https://netflix-loading-page-1.vercel.app')  # Netflix landing page
                else:
                    flash('Invalid email or password', 'danger')
            except Error as e:
                flash(f'Error: {e}', 'danger')
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
