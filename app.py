import streamlit as st
import sqlite3
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

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
    for message in messages[::-1]:
        st.write(f"{message[0]}: {message[1]} at {message[2]}")

def clear_database():
    """Clear the messages table in the database."""
    c.execute("DELETE FROM messages")
    conn.commit()
    st.success("Chatroom cleared.")

# Initialize last clear time
if 'last_clear_time' not in st.session_state:
    st.session_state['last_clear_time'] = datetime.now()

# Streamlit UI
st.title('Public Chatroom')

# User input for sending messages
default_username = "Guest"
username = st.text_input('Enter your username:', value=default_username)

# Display chatroom content
display_chatroom()

message = st.text_input('Type your message here:')
if st.button('Send Message'):
    add_message(username, message)

# Check if it's time to clear the database
if datetime.now() - st.session_state['last_clear_time'] > timedelta(minutes=10):
    clear_database()
    st.session_state['last_clear_time'] = datetime.now()

# Auto-refresh every 3 seconds
st_autorefresh(interval=3000, key="chatroom_auto_refresh")
