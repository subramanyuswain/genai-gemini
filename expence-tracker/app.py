import streamlit as st
import google.generativeai as genai
import os
import io
from PIL import Image
import base64
from dotenv import load_dotenv
from methods import *
from bill_metadata import execute_bill_metadata

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(image_data, prompt):
    """
    Gets a response from the Gemini Pro Vision model based on the image and prompt.

    Args:
        image_data: The image data (bytes).
        prompt: The prompt for the model.

    Returns:
        The text response from the model.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
     
    # Prepare the image part for Gemini
    image_part = { # changed into dict
            "mime_type": "image/jpeg",
            "data": base64.b64encode(image_data).decode()
    }

    response = model.generate_content([prompt, image_part])
    return response.text

def image_to_bytes(image):
    """
    Convert image into bytes.
    Args:
        image: PIL image.
    Returns:
        bytes
    """
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr

def generate_sql_query(image):
    
    image_bytes = image_to_bytes(image)

    prompt = generate_item_insert_query_promt()
    

    try:
        response = get_gemini_response(image_bytes, prompt)
        return response
    except Exception as e:
        return f"Error generating SQL query: {e}"

def main():
    st.title("Grocery Bill to SQL Converter")

    uploaded_file = st.file_uploader("Upload a grocery bill image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Grocery Bill", use_container_width=True)

        if st.button("Generate SQL Query"):
            sql_query = generate_sql_query(image)
            sql_query += "\n" + execute_bill_metadata(image, st)
            st.text_area("Generated SQL Query", value=sql_query, height=200)
            if sql_query=="Could not extract data from image":
                st.error("Could not extract data from image. Try another one")

if __name__ == "__main__":
    main()
