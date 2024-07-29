import streamlit as st
import sqlite3
import os
from datetime import datetime, timedelta
import time

# Connect to SQLite database
def connect_db():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    # Create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS messages
               (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, text TEXT, timestamp TEXT)''')
    conn.commit()
    return conn, c

# Initialize the database connection
conn, c = connect_db()

def add_message(username, message):
    """Add a new message to the chatroom, including the sender's username and a timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Format: YYYY-MM-DD HH:MM:SS
    c.execute("INSERT INTO messages (username, text, timestamp) VALUES (?, ?, ?)", (username, message, timestamp))
    conn.commit()
    st.success(f"Message added to the chatroom by {username}: {message}")

def display_chatroom():
    """Display the chatroom content, showing messages along with usernames and timestamps."""
    c.execute("SELECT username, text, timestamp FROM messages ORDER BY id DESC")
    messages = c.fetchall()
    for message in messages:
        st.write(f"{message[0]}: {message[1]} at {message[2]}")

def clear_database():
    """Clear the messages table in the database."""
    c.execute("DELETE FROM messages")
    conn.commit()
    st.success("Chatroom cleared.")

# Streamlit UI
st.title('Public Chatroom')

# User input for sending messages
username = st.text_input('Enter your username:')
message = st.text_input('Type your message here:')
if st.button('Send Message'):
    add_message(username, message)

# Display chatroom content
display_chatroom()

# Check if it's time to clear the database
last_clear_file = 'last_clear.txt'
if os.path.exists(last_clear_file):
    with open(last_clear_file, 'r') as file:
        last_clear_time = datetime.strptime(file.read(), '%Y-%m-%d %H:%M:%S')
    if datetime.now() - last_clear_time > timedelta(minutes=10):
        clear_database()
        with open(last_clear_file, 'w') as file:
            file.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
else:
    with open(last_clear_file, 'w') as file:
        file.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        clear_database()