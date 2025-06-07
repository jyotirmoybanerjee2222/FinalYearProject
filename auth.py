# auth.py
import re
import pyrebase

firebaseConfig = {
    "apiKey": ,
    "authDomain": "contexify-16827.firebaseapp.com",
    "projectId": "contexify-16827",
    "storageBucket": "contexify-16827.firebasestorage.app",
    "messagingSenderId": "991703954388",
    "appId": "1:991703954388:web:c7f9ae8e0bd231fac1dc41",
    "measurementId": "G-PWVJ86R5N8",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

def signup(username, email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        return True, "User created successfully."
    except Exception as e:
        return False, extract_firebase_error(e)

def login(identifier, password):
    try:
        user = auth.sign_in_with_email_and_password(identifier, password)
        return True, identifier
    except Exception as e:
        return False, extract_firebase_error(e)

def extract_firebase_error(exception):
    try:
        error_json = exception.args[1]
        error_detail = eval(error_json)['error']['message']
        return error_detail.replace('_', ' ').capitalize()
    except:
        return "An unknown error occurred."
