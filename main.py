#Import all the library
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image
import streamlit as st

#Load the API Key
load_dotenv()
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

#Function to load Google Gemini Vision Model and get response
def get_response_image(image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([image[0], prompt])
    return response.text

#Function to load Google Gemini Pro Model and get response
def get_response(prompt, input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt, input])
    return response.text

    
#Initialize the streamlit app
st.set_page_config(page_title="Tripsa")
st.image('D:\Tripsa\gaj.jpg', width=70)
st.header("Tripsa: Discover and Plan your Culinary Adventures!")


#Creating radio section choices
section_choice = st.radio("Choose Section:", ("Trip Planner", "Restaurant & Hotel Planner"))

###########################################################################################
#If the choice is trip planner
if section_choice == "Trip Planner":

    #Prompt Template
    input_prompt_planner = """
    You are an expert Tour Planner. Your job is to provide recommendations and plan for given location for giner number of days,and given number of people
    and type of trip(Freinds, Family, Solo, Honeymoon, Adventure, etc.).
    even if number of days is not provided.
    Also, suggest hidden secrets, hotels, and beautiful places we shouldn't forget to visit
    Also tell best month to visit given place.
    Retun the response using markdown.
    """

    #Input
    input_plan = st.text_area("Provide location, number of days, Number of People and Type of the trip to obtain itinerary plan!")
    #Button
    submit1 = st.button("Plan my Trip!")
    if submit1:
        response = get_response(input_prompt_planner, input_plan)
        st.subheader("Planner Bot: ")
        st.write(response)
###########################################################################################
#If the choice is Restaurant & Hotel Planner
if section_choice == "Restaurant & Hotel Planner":

    #Prompt Template
    input_prompt_planner = """
    You are an expert Restaurant & Hotel Planner. 
    Your job is to provide Restaurant & Hotel for given place and you have to provide not very expensive and not very cheap,
    - Provide rating of the restaurant/hotel
    - Top 5 restaurants with address and average cost per cuisine
    - Top 5 hotels with address and average cost per night
    Retun the response using markdown.
    """
    #Input
    input_plan = st.text_area("Provide location to find Hotel & Restaurants!")
    #Button
    submit1 = st.button("Find Restaurant & Hotel!")
    if submit1:
        response = get_response(input_prompt_planner, input_plan)
        st.subheader("Acomodation Bot: ")
        st.write(response)