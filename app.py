import streamlit as st
import sqlite3
import os
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh
from bs4 import BeautifulSoup
import requests

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
    if not message.strip():  # Check if the message is not empty after stripping whitespace
        st.error("Please enter a message.")
        return  # Exit the function without adding the message

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Format: YYYY-MM-DD HH:MM:SS
    c.execute("INSERT INTO messages (username, text, timestamp) VALUES (?, ?, ?)", (username, message, timestamp))
    conn.commit()
    st.success(f"Message added to the chatroom by {username}: {message}")

def clear_database():
    """Clear the messages table in the database."""
    c.execute("DELETE FROM messages")
    conn.commit()
    st.success(f"Chatroom cleared at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")

def scrape_news():
    url = 'http://thedailystar.net'  # Replace with the actual news site URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all div elements with class 'card-image'
    card_images = soup.find_all('div', class_='card-image')
    
    news_items = []
    for card_image in card_images:
        # Within each card_image, find the <a> tag with an aria-label attribute
        link_tag = card_image.find('a', {'aria-label': True})
        if link_tag:
            title = link_tag['aria-label']  # Use the aria-label as the title
            link = link_tag['href']  # Extract the href attribute for the link
            news_items.append({'title': title, 'link': link})
    
    return news_items

def display_scraped_news():
    news_articles = scrape_news()
    for article in news_articles:
        st.write(f"## {article['title']}")
        st.write(f"[Read more]({article['link']})")
        st.write("====================================")


# Streamlit UI

st.sidebar.title('Settings')
# User input for sending messages
default_username = "Guest"
username = st.sidebar.text_input('Enter your username:', value=default_username)

st.sidebar.title('Navigation')
page = st.sidebar.radio('Go to', ['Public Chat', 'News Update'])


# Auto-refresh every 3 seconds
st_autorefresh(interval=3000, key="chatroom_auto_refresh")

if page == 'Public Chat':
    st.title('Public Chatroom')

    # Display chatroom content
    messages = c.execute("SELECT username, text, timestamp FROM messages ORDER BY id DESC").fetchall()
    for message in messages[::-1]:
        with st.chat_message(message[0]):
            st.write(f"{message[0]}: {message[1]}")
            d, t = message[2].split(' ')
            st.write(f"Date: {d} Time: {t}")

    message = st.chat_input("Type your message here:")
    if message:
        add_message(username, message)

elif page == 'News Update':
    st.title('News Update')
    
    # At the beginning of your script, initialize the session state variable
    if 'scrape_news_active' not in st.session_state:
        st.session_state.scrape_news_active = False

    # Modify the button logic to toggle the state
    st.write("Button for News Updates Below:")
    if st.button('Manage News'):
        st.session_state.scrape_news_active = not st.session_state.scrape_news_active

    # Call display_scraped_news only if the state is True
    if st.session_state.scrape_news_active:
        display_scraped_news()

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
