import os
import streamlit as st
from PIL import Image
from google import genai
from google.genai.types import Part # Correctly import Part from google.genai.types
from dotenv import load_dotenv

# 1. Load environment variables from .env file
# This allows you to keep your API key secure and not hardcoded in the script.
load_dotenv()

# 2. Retrieve the Google API Key from environment variables
# Ensure you have GOOGLE_API_KEY set in your .env file or system environment.
GOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# 3. Initialize the Google Generative AI client
# This is the correct and current way to establish a connection to the Gemini API.
client = genai.Client(api_key=GOGLE_API_KEY)

# 4. Define a function to interact with the Gemini model
# This function sends the prompt (system instructions + image + user question)
# to the Gemini 2.0 Flash model and returns its text response.
def get_gemini_response(system_prompt, image_object, user_input):
    """
    Sends a multimodal prompt to the Gemini 2.0 Flash model.

    Args:
        system_prompt (str): The initial instructions or role for the AI.
        image_object (PIL.Image.Image): The image to be analyzed by the model.
        user_input (str): The specific question or query about the image.

    Returns:
        str: The text response generated by the Gemini model.
    """
    response = client.models.generate_content(

        model="gemini-1.5-flash", # Specifying the model: Gemini 2.0 Flash is suitable for multimodal tasks.
        contents=[
            # The 'contents' list defines the parts of the prompt.
            # For multimodal inputs, each part must be explicitly typed.
            # Text parts are wrapped in genai.types.Part objects.
            Part(text=system_prompt), # First part: System instructions given as text.
            image_object,             # Second part: The PIL Image object. The library handles its conversion internally.
            Part(text=user_input)     # Third part: The user's specific question as text.
        ]
    )
    return response.text # Extracting and returning only the text content from the model's response.

# --- Streamlit Application User Interface (UI) ---

# 5. Set up the Streamlit page configuration
# This sets the title that appears in the browser tab.
st.set_page_config(page_title="Multilanguage Invoice Extractor")

# 6. Display the main header of the application
st.header("Multilanguage Invoice Extractor")

# 7. Create a text input field for the user's question
# The 'key' argument is important for Streamlit to manage widget state, especially if you have multiple inputs.
input_text = st.text_input("Input: ", key="input")

# 8. Create a file uploader widget for the invoice image
# Specifies accepted file types (JPG, JPEG, PNG) for image uploads.
uploaded_file = st.file_uploader("Upload your Invoice image: ", type=["jpg", "jpeg", "png"])

# Initialize 'image' variable to None. It will hold the PIL Image object if a file is uploaded.
image = None

# 9. Display the uploaded image if a file is provided
if uploaded_file is not None:
    # Open the uploaded file using Pillow (PIL) to get an Image object.
    image = Image.open(uploaded_file)
    # Display the image in the Streamlit application.
    st.image(image, caption="Uploaded image")

# 10. Create a button to trigger the invoice analysis
# When this button is clicked, Streamlit re-runs the entire script.
submit = st.button("Tell me about this invoice")

# 11. Define the system prompt string
# This prompt guides the Gemini model on its role and task.
system_prompt = """
You are an expert in understanding invoices. We will upload an image of invoice and you will have to answer any question based on that
"""

# 12. Logic to execute when the submit button is clicked
if submit:
    # 13. Check if both a file was uploaded and successfully converted to a PIL Image object
    if uploaded_file is not None and image is not None:
        try:
            # 14. Call the get_gemini_response function with the system prompt, image, and user input.
            response = get_gemini_response(system_prompt, image, input_text)
            
            # 15. Display the response from the Gemini model
            st.subheader("The response is ")
            st.write(response)
        except Exception as e:
            # 16. Catch and display any errors that occur during the API call
            st.error(f"An error occurred while getting response from Gemini: {e}")
            # Also print the full error to the console for more detailed debugging (e.g., in your terminal).
            print(f"Full error during Gemini call: {e}")
    else:
        # 17. Display a warning if the user clicks submit without uploading an image
        st.warning("Please upload an invoice image first.")
