# ST-PublicChat

## Overview
ST-PublicChat is a Streamlit-based application designed to provide a platform for universal users to engage in public chat discussions. It allows users to interact in a chatroom environment, facilitating communication and interaction among participants. The application is built using Python and leverages the Streamlit framework for its interactive web interface, making it accessible and easy to use.

## Features
- **Real-time Chatting**: Users can send messages in real-time, which are immediately visible to all participants in the chatroom.
- **User Identification**: Users can enter a username to identify themselves in the chatroom.
- **Message Timestamps**: Each message is timestamped, providing context on when it was sent.
- **Automatic Database Clearing**: The chatroom messages are automatically cleared every 10 minutes to keep the conversation fresh and manageable.
- **Auto-refresh**: The chatroom auto-refreshes every 3 seconds to ensure users see the latest messages without manual reloading.

## Getting Started
To get started with ST-PublicChat, follow these steps:

### Prerequisites
- Ensure you have Python installed on your system.
- Install Streamlit if you haven't already, by running `pip install streamlit` in your terminal.

### Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ST-PublicChat.git
   ```
   Replace `yourusername` with the actual username where the repository is hosted.

2. Navigate to the project directory:
   ```
   cd ST-PublicChat
   ```

3. Install any required packages listed in `requirements.txt`:
   ```
   pip install -r requirements.txt
   ```

### Running the Application
To run the application, execute the following command in your terminal:
```
streamlit run app.py
```
This will start the Streamlit server and open the chatroom in your default web browser.

## Usage
Upon launching, you'll be greeted with the chatroom interface. Here's how to use it:

- **Username**: Enter your desired username in the provided text input field.
- **Sending Messages**: Type your message in the 'Type your message here' input box and click 'Send Message' to post it to the chatroom.
- **Viewing Messages**: The chatroom displays messages along with usernames and timestamps. Messages are shown in descending order, with the most recent messages appearing first.

## Database
The application uses SQLite for storing messages. The database (`chat.db`) automatically created and managed by the application. The database is cleared every 10 minutes to keep the chatroom fresh.

## Contributing
Contributions are welcome! Feel free to fork the repository, make your changes, and submit a pull request.

## Contact
For any questions or suggestions, feel free to open an issue or contact the maintainers.

## Acknowledgments
- Streamlit for making web app development simple and intuitive.
- SQLite for providing a lightweight database solution.

## Disclaimer
This project is for educational purposes and is not intended for production use without further development and security considerations.