import hashlib
import re
import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyA98BWzuQfC2CdAmv7fWGK0PeHA3v2zLas",
    "authDomain": "contexify-16827.firebaseapp.com",
    "projectId": "contexify-16827",
    "storageBucket": "contexify-16827.firebasestorage.app",
    "messagingSenderId": "991703954388",
    "appId": "1:991703954388:web:c7f9ae8e0bd231fac1dc41",
    "measurementId": "G-PWVJ86R5N8",
    "databaseURL": ""  # Optional unless you use Firebase Realtime DB
}


firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

# In-memory user database
users_db = {}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup(username, email, password):
    # Check for existing username
    if username in users_db:
        return False, "Username already exists."

    # Check for existing email
    if any(user["email"] == email for user in users_db.values()):
        return False, "Email already exists."

    # Add user
    users_db[username] = {
        "email": email,
        "password": hash_password(password)
    }
    return True, "User created successfully."

def login(identifier, password):
    password_hash = hash_password(password)
    for username, user in users_db.items():
        if (identifier == username or identifier == user["email"]) and user["password"] == password_hash:
            return True, username
    return False, None
