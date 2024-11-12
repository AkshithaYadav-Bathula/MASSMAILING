import streamlit as st
import requests

# Set up the Flask API URL
FLASK_API_URL = "http://127.0.0.1:5000"

# Streamlit app for login and registration
st.title("User Authentication System")

# Tabs for Login and Registration
tab1, tab2 = st.tabs(["Login", "Register"])

# Register tab
with tab2:
    st.header("Register")
    register_username = st.text_input("Username", key="register_username")
    register_email = st.text_input("Email", key="register_email")
    register_password = st.text_input("Password", type="password", key="register_password")

    if st.button("Register"):
        # Send registration data to Flask API
        register_data = {
            "username": register_username,
            "email": register_email,
            "password": register_password
        }
        response = requests.post(f"{FLASK_API_URL}/register", json=register_data)
        
        if response.status_code == 201:
            st.success("Registration successful. You can now log in.")
        else:
            st.error(response.json().get("message"))

# Login tab
with tab1:
    st.header("Login")
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        # Send login data to Flask API
        login_data = {
            "username": login_username,
            "password": login_password
        }
        response = requests.post(f"{FLASK_API_URL}/login", json=login_data)
        
        if response.status_code == 200:
            st.success("Login successful!")
        else:
            st.error(response.json().get("message"))

    if st.button("Logout"):
        # Send logout request to Flask API
        response = requests.post(f"{FLASK_API_URL}/logout")
        
        if response.status_code == 200:
            st.success("Logged out successfully.")
        else:
            st.error("Error logging out.") 