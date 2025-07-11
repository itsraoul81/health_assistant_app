import streamlit as st
import google.generativeai as genai

for m in genai.list_models():
    print(m.name)

# Set your Gemini API key
genai.configure(api_key="AIzaSyAqDo75w3RYOqbhGtherUk4BXy-hSgncb8")

# Initialize model
model = genai.GenerativeModel("models/gemini-2.5-flash")



# Streamlit UI
st.set_page_config(page_title="Health Assistant", layout="centered")
st.title("🩺 Gemini Health Assistant")
st.markdown("Ask a health-related question:")

user_input = st.text_input("Your Question")

if user_input:
    st.write("Generating response...")
    response = model.generate_content(user_input)
    st.success(response.text)

