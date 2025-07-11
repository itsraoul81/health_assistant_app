import google.generativeai as genai
import os
# from dotenv import load_dotenv # Keep this if you use .env, otherwise remove

# --- Configuration ---
# Load environment variables if you are using a .env file
# load_dotenv()

# IMPORTANT: If you hardcoded your API key in app.py, you need to hardcode it here too.
# Otherwise, ensure GEMINI_API_KEY is set in your .env file or environment variables.
# Example if hardcoding:
GEMINI_API_KEY = "AIzaSyAqDo75w3RYOqbhGtherUk4BXy-hSgncb8" # Replace with your actual Gemini API Key

# Configure the Google Gemini API
try:
    if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_API_KEY_HERE":
        raise ValueError("Gemini API Key is not set. Please replace 'YOUR_API_KEY_HERE' with your actual key.")
    genai.configure(api_key=GEMINI_API_KEY)
except ValueError as e:
    st.error(f"Configuration Error: {e}")
    st.stop() # Stop the Streamlit app if the API key is missing or invalid.
except Exception as e:
    st.error(f"An unexpected error occurred during API configuration: {e}")
    st.stop()

print("Fetching available Gemini models...")
try:
    # List all available models
    for m in genai.list_models():
        # Filter for models that support 'generateContent' method, as that's what you need
        if 'generateContent' in m.supported_generation_methods:
            print(f"Name: {m.name}")
            print(f"  Description: {m.description}")
            print(f"  Supported Methods: {m.supported_generation_methods}")
            print("-" * 30)
except Exception as e:
    print(f"An error occurred while listing models: {e}")
    print("Please check your internet connection and API key.")

print("\n--- End of Model List ---")
print("Look for models like 'gemini-1.5-pro', 'gemini-1.5-flash', or 'gemini-2.0-flash'.")
print("You'll use one of these names to replace 'gemini-pro' in your app.py file.")
