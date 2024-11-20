# Import libraries
from dotenv import load_dotenv
import os
import google.generativeai as genai
import streamlit as st

# Load the API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Pro Model and get response
def get_response(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt])
    return response.text

# Initialize the Streamlit app
st.set_page_config(page_title="Tripsa: AI Trip Planner and Advisor", page_icon="🌍", layout="centered")
st.header("🌍 Tripsa: Your Conversational AI Trip Planner!")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_stage" not in st.session_state:
    st.session_state.conversation_stage = "greeting"
if "trip_details" not in st.session_state:
    st.session_state.trip_details = {
        "destination": None,
        "number_of_people": None,
        "duration": None,
        "type_of_trip": None,
        "type_of_stay": None,
    }

# Conversation stages logic
def handle_conversation(user_message):
    stage = st.session_state.conversation_stage
    trip_details = st.session_state.trip_details

    if stage == "greeting":
        st.session_state.conversation_stage = "ask_destination"
        return "Hello! I'm Tripsa, your AI travel planner. Let's plan your perfect trip! Where would you like to go?"

    elif stage == "ask_destination":
        trip_details["destination"] = user_message
        st.session_state.conversation_stage = "ask_number_of_people"
        return f"Great choice! How many people are going on this trip?"

    elif stage == "ask_number_of_people":
        trip_details["number_of_people"] = user_message
        st.session_state.conversation_stage = "ask_duration"
        return "Got it. How many days will your trip last?"

    elif stage == "ask_duration":
        trip_details["duration"] = user_message
        st.session_state.conversation_stage = "ask_type_of_trip"
        return "Perfect! What type of trip are you planning? (e.g., Family, Friends, Solo, Honeymoon, Adventure)"

    elif stage == "ask_type_of_trip":
        trip_details["type_of_trip"] = user_message
        st.session_state.conversation_stage = "ask_type_of_stay"
        return "Sounds fun! What type of stay do you prefer? (e.g., Hotel, Hostel, Airbnb, Resort)"

    elif stage == "ask_type_of_stay":
        trip_details["type_of_stay"] = user_message
        st.session_state.conversation_stage = "generate_summary"
        return "Thanks for the details! Let me prepare a personalized itinerary for you."

    elif stage == "generate_summary":
        st.session_state.conversation_stage = "done"
        summary_prompt = f"""
        You are an expert travel planner. Based on the following details, generate a detailed trip itinerary:
        - Destination: {trip_details['destination']}
        - Number of People: {trip_details['number_of_people']}
        - Duration: {trip_details['duration']} days
        - Type of Trip: {trip_details['type_of_trip']}
        - Type of Stay: {trip_details['type_of_stay']}
        Include must-visit spots, hidden gems, and best months to visit. Return the response in markdown format.
        """
        return get_response(summary_prompt)

    else:
        return "Is there anything else you'd like to plan or ask about?"

# Main chat interface
st.markdown("### Chat with your AI Planner")

# Display existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for new user messages
if user_input := st.chat_input("Type your message here..."):
    # Append user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get bot response based on conversation stage
    bot_response = handle_conversation(user_input)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)