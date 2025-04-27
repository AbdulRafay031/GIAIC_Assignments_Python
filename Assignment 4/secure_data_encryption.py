import streamlit as st
import hashlib
import json
import os
from cryptography.fernet import Fernet


# === File Setup ===
KEY_FILE = "secret.key"
DATA_FILE = "data.json"

# === Generate or Load Encryption Key ===
if os.path.exists(KEY_FILE):
    with open(KEY_FILE, "rb") as f:
        KEY = f.read()
else:
    KEY = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(KEY)

cipher = Fernet(KEY)

# === Load Stored Data ===
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        stored_data = json.load(f)
else:
    stored_data = {}

# === Session State Defaults ===
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0
if "redirect_to_login" not in st.session_state:
    st.session_state.redirect_to_login = False

# === Hashing Function ===
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# === Encrypt and Decrypt Functions ===
def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()

def decrypt_data(encrypted_text, passkey):
    hashed_passkey = hash_passkey(passkey)
    for key, value in stored_data.items():
        if value["encrypted_text"] == encrypted_text and value["passkey"] == hashed_passkey:
            st.session_state.failed_attempts = 0
            return cipher.decrypt(encrypted_text.encode()).decode()
    st.session_state.failed_attempts += 1
    return None

# === Save Data to File ===
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(stored_data, f, indent=4)

# === UI ===
st.title("🔒 Secure Data Encryption System")

menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.selectbox("Navigation", menu)

# === Handle Forced Redirect to Login ===
if st.session_state.redirect_to_login and choice != "Login":
    st.warning("🔒 Redirecting to login due to too many failed attempts...")
    st.session_state.redirect_to_login = False
    st.experimental_rerun()

# === Home Page ===
if choice == "Home":
    st.subheader("🏠 Welcome")
    st.write("Use this app to **securely store and retrieve data** using a passkey.")

# === Store Data Page ===
elif choice == "Store Data":
    st.subheader("📂 Store Data Securely")
    user_data = st.text_area("Enter Data:")
    passkey = st.text_input("Enter Passkey:", type="password")

    if st.button("Encrypt & Save"):
        if user_data and passkey:
            hashed_passkey = hash_passkey(passkey)
            encrypted_text = encrypt_data(user_data)
            stored_data[encrypted_text] = {
                "encrypted_text": encrypted_text,
                "passkey": hashed_passkey
            }
            save_data()
            st.success("✅ Data stored securely!")
            st.code(encrypted_text, language='text')
        else:
            st.error("⚠️ Both fields are required!")

# === Retrieve Data Page ===
elif choice == "Retrieve Data":
    st.subheader("🔍 Retrieve Your Data")
    encrypted_text = st.text_area("Enter Encrypted Data:")
    passkey = st.text_input("Enter Passkey:", type="password")

    if st.session_state.failed_attempts >= 3:
        st.session_state.redirect_to_login = True
        st.experimental_rerun()

    if st.button("Decrypt"):
        if encrypted_text and passkey:
            result = decrypt_data(encrypted_text, passkey)
            if result:
                st.success("✅ Decrypted Data:")
                st.code(result, language='text')
            else:
                attempts_left = 3 - st.session_state.failed_attempts
                st.error(f"❌ Incorrect passkey! Attempts remaining: {attempts_left}")
        else:
            st.error("⚠️ Both fields are required!")

# === Login Page ===
elif choice == "Login":
    st.subheader("🔑 Reauthorization Required")
    login_pass = st.text_input("Enter Master Password:", type="password")

    if st.button("Login"):
        if login_pass == "admin123":  # Replace with your own logic for real apps
            st.session_state.failed_attempts = 0
            st.session_state.redirect_to_login = False
            st.success("✅ Reauthorized successfully! Redirecting to Retrieve Data...")
            st.experimental_rerun()
        else:
            st.error("❌ Incorrect password!")
