import streamlit as st
import random
import json
import datetime
import os

# Load challenges
with open("Assignment 5/data/challenges.json", "r") as file:
    challenges = json.load(file)

# Load quotes
with open("Assignment 5/data/quotes.json", "r") as file:
    quotes = json.load(file)

st.title("🌱 Growth Mindset Challenge")

if st.button("Give me today's challenge!"):
    st.subheader("🧠 Today's Challenge:")
    st.write(random.choice(challenges))

if st.button("Inspire Me!"):
    st.subheader("💬 Quote of the Day:")
    st.write(random.choice(quotes))

st.subheader("✍️ Reflect in Your Journal")
entry = st.text_area("Write about your thoughts:", height=200)

if st.button("Save Entry"):
    os.makedirs("Assignment 5/journal", exist_ok=True)
    with open("Assignment 5/journal/entries.txt", "a") as f:
        f.write(f"{datetime.date.today()}:\n{entry}\n---\n")
    st.success("Saved!")
