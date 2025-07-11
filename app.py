import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv # Make sure this line is present

# --- Configuration ---

# NEW: Load environment variables from a .env file.
# This function searches for a .env file in the current directory and loads
# any key-value pairs found there into the script's environment variables.
load_dotenv() # Make sure this line is present and NOT commented out

# Retrieve the Gemini API key from the environment variables.
# This is the secure way to access your API key.
# The `os.getenv()` method retrieves the value of the environment variable
# named "GEMINI_API_KEY".
try:
    gemini_api_key = os.getenv("GEMINI_API_KEY") # This line should be present
    if not gemini_api_key:
        # Raise an error if the environment variable is not found,
        # guiding the user to set it correctly.
        raise ValueError("GEMINI_API_KEY environment variable not set. Please ensure it's in your .env file.")
    genai.configure(api_key=gemini_api_key)
except ValueError as e:
    st.error(f"Configuration Error: {e}. Please ensure your GEMINI_API_KEY is correctly set in the .env file.")
    st.stop() # Stop the Streamlit app if the API key is missing or invalid.
except Exception as e:
    st.error(f"An unexpected error occurred during API configuration: {e}")
    st.stop()
# ... (rest of your app.py code) ...

# Initialize the Generative Model.
model = genai.GenerativeModel('models/gemini-2.5-pro')

# --- Streamlit User Interface (UI) ---

# Set basic page configuration for the Streamlit app.
st.set_page_config(
    page_title="AI Health Assistant",
    layout="centered", # 'centered' or 'wide'
    initial_sidebar_state="auto" # 'auto', 'expanded', or 'collapsed'
)

# Display the main title and an introductory markdown.
st.title("🩺 AI Health Assistant")
st.markdown("""
Welcome to your AI-powered Health Assistant!
Type your basic clinical health-related questions below, and I'll provide informative responses.

**Important Disclaimer:**
This assistant provides general information for educational purposes only and is **not a substitute for professional medical advice, diagnosis, or treatment.** Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. Never disregard professional medical advice or delay in seeking it because of something you have read on this application.
""")

# Create a text area for the user to input their question.
# The `placeholder` provides a hint, and `height` controls the size of the input box.
user_question = st.text_area(
    "Ask your health question here:",
    placeholder="e.g., What are the common symptoms of the flu?",
    height=120
)

# Create a button to submit the user's question.
# The code inside this 'if' block will execute when the button is clicked.
if st.button("Get Answer", key="submit_button"):
    # Check if the user has entered any text.
    if user_question:
        # Display a spinner while the LLM is processing the request.
        with st.spinner("Thinking... Please wait for the AI to generate a response."):
            try:
                # Generate content using the Gemini model.
                # The prompt is carefully crafted to guide the model's behavior and focus.
                # It includes a system instruction to ensure the AI acts as a helpful,
                # informative health assistant and explicitly states limitations.
                response = model.generate_content(
                    f"""
                    You are a helpful and informative AI health assistant.
                    Your goal is to provide concise, accurate, and general information on health-related questions.
                    **Crucially, you must always state that you are not a medical professional and cannot provide diagnoses or personalized medical advice.**
                    Encourage the user to consult a qualified healthcare professional for any specific health concerns.

                    Here is the user's question:
                    "{user_question}"
                    """,
                    # Configuration for content generation.
                    # 'temperature' controls the randomness of the output.
                    # A lower temperature (e.g., 0.2-0.5) makes the output more deterministic and factual,
                    # which is generally preferred for health information.
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.4
                    )
                )

                # Display the generated response from the LLM.
                st.subheader("Assistant's Response:")
                st.info(response.text)

            except Exception as e:
                # Catch any errors during the API call or response generation.
                st.error(f"An error occurred while generating the response: {e}")
                st.warning("Please try rephrasing your question or try again later.")
    else:
        # Warn the user if they try to submit an empty question.
        st.warning("Please enter a question in the text area above to get an answer.")

# Add a simple footer for branding or additional information.
st.markdown("---")
st.markdown("Powered by Google Gemini & Streamlit")

