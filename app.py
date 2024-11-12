import mysql.connector
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# MySQL database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",                 # Replace with your MySQL username
    password="Akshb17.",              # Replace with your MySQL password
    database="mass_mail_project" # The database name
)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# User class to represent authenticated users
class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

    @staticmethod
    def get_by_username(username):
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            return User(user["id"], user["username"], user["email"])
        return None

    @staticmethod
    def get(user_id):
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            return User(user["id"], user["username"], user["email"])
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')


    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, hashed_password))
        db.commit()
        return jsonify({"message": "Registration successful"}), 201
    except mysql.connector.IntegrityError:
        return jsonify({"message": "Username or email already exists"}), 400
    finally:
        cursor.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.get_by_username(username)
    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True) 