import streamlit as st
import re

def check_password_strength(password):
    score = 0
    suggestions = []

    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("➤ Password should be at least 8 characters long.")

    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("➤ Include both UPPERCASE and lowercase letters.")

    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        suggestions.append("➤ Add at least one number (0-9).")

    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        suggestions.append("➤ Include at least one special character (!@#$%^&*).")

    # Bonus point if password is 12+ characters long
    if len(password) >= 12:
        score += 1

    st.subheader("🔐 Password Analysis Complete")
    st.write(f"**Score:** {score}/5")

    if score <= 2:
        st.error("❌ Strength: Weak")
        st.info("💡 Suggestions to improve your password:")
        for suggestion in suggestions:
            st.write(suggestion)
    elif score == 3 or score == 4:
        st.warning("⚠️ Strength: Moderate")
        st.info("💡 Consider improving your password:")
        for suggestion in suggestions:
            st.write(suggestion)
    else:
        st.success("✅ Strength: Strong Password!")
        st.balloons()

# Streamlit App
st.title("🔑 Password Strength Meter")
user_password = st.text_input("Enter your password", type="password")

if user_password:
    check_password_strength(user_password)
