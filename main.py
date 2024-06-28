import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load OpenAI service details
openai.api_key = os.getenv('OPENAI_API_KEY')

# Custom CSS for a more polished UI
st.markdown("""
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: #f5f5f7;
            color: #1d1d1f;
        }
        .stTextInput, .stButton {
            margin-top: 20px;
        }
        .chat-bubble {
            display: inline-block;
            padding: 10px;
            border-radius: 15px;
            margin: 5px;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        }
        .user-message {
            background: #e1f5fe;
            text-align: right;
            color: black;
        }
        .assistant-message {
            background: #007aff;
            text-align: left;
            color: white;
        }
        .user-message-container {
            text-align: right;
        }
        .assistant-message-container {
            text-align: left;
        }
        .chat-container {
            display: flex;
            flex-direction: column-reverse;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 HealthBot")
st.markdown("*Ask, Learn, Thrive. Healthbot is here for you*")
st.markdown("Welcome to HealthBot. Please enter your symptoms or questions below:")

# Initialize the session state to keep track of the conversation and user name
if 'conversation' not in st.session_state:
    st.session_state.conversation = [
        {"role": "system", "content": "You are a helpful healthcare assistant."}
    ]
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# Function to display the chat history with customizable CSS styles
def display_chat_history():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for message in reversed(st.session_state.conversation[1:]):
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-message-container">
                <div class="chat-bubble user-message">
                    <strong>{st.session_state.user_name} 🤔:</strong><br>{message['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        elif message["role"] == "assistant":
            st.markdown(f"""
            <div class="assistant-message-container">
                <div class="chat-bubble assistant-message">
                    <strong>HealthBot 🩺:</strong><br>{message['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# If the user's name is not set, ask for it
if not st.session_state.user_name:
    st.session_state.user_name = st.text_input("Please enter your name:", key="name_input")

    # If the user has entered a name and clicks "Submit"
    if st.button("Submit Name"):
        # Add a greeting message from the assistant
        st.session_state.conversation.append({"role": "assistant", "content": f"Hello {st.session_state.user_name}!"})
        st.experimental_rerun()

# If the user's name is set, proceed with the conversation
if st.session_state.user_name:
    # Display the greeting message
    if len(st.session_state.conversation) == 2:
        display_chat_history()
    
    # Get user input and button
    user_input = st.text_input("Enter your symptoms or questions:", key="input_text")

    # If user has entered something and clicks the "Send" button
    if st.button("Send"):
        if user_input:
            # Append user input to the conversation
            st.session_state.conversation.append({"role": "user", "content": user_input})
            
            # Call the OpenAI API to get the assistant's response
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.conversation
            )
            
            # Get the assistant's reply
            assistant_reply = response['choices'][0]['message']['content'].strip()
            
            # Append assistant's reply to the conversation
            st.session_state.conversation.append({"role": "assistant", "content": assistant_reply})
            
            # Clear the input box by rerunning the app
            st.experimental_rerun()

    # Display the updated chat history below the input box
    display_chat_history()
