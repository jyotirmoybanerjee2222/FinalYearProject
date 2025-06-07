import streamlit as st
import fitz
from summarizer import summarize_text
from auth import login, signup,is_valid_email

def login_page():
    st.title("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        success, user = login(email, password)
        if success:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.success(f"Welcome {email}!")
        else:
            st.error(user)  # This contains error message


def signup_page():
    st.title("📝 Sign Up")

    username = st.text_input("Username")
    email = st.text_input("Email Address")
    password = st.text_input("Choose Password", type="password")

    if st.button("Sign Up"):
        if not username or not email or not password:
            st.error("All fields are required.")
        elif not is_valid_email(email):
            st.error("Invalid email format. Please enter a valid email.")
        else:
            success, message = signup(username, email, password)
            if success:
                st.success(message)
            else:
                st.error(message)




def app_page():
    st.title("Contexify - PDF Summarizer and ChatBot")
    pdf = st.file_uploader("Upload your PDF", type="pdf")

    if pdf and st.button("Summarize"):
        from fitz import open as open_pdf  # only when used
        doc = open_pdf(stream=pdf.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()

        summary = summarize_text(text)
        st.subheader("Summary:")
        st.write(summary)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.success("Logged out successfully.")

def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    menu = st.sidebar.selectbox("Menu", ["Login", "Sign Up"] if not st.session_state.logged_in else ["Home", "Logout"])

    if not st.session_state.logged_in:
        if menu == "Login":
            login_page()
        elif menu == "Sign Up":
            signup_page()
    else:
        app_page()

if __name__ == "__main__":
    main()