import base64
import io
from dotenv import load_dotenv

import streamlit as st
import os
import PIL as Image
import pdf2image
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_gemini_response(input, pdf_content, prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        ## Convert image to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploaded")
    
## Streamlit app code
st.set_page_config(page_title="ATS Resume expert", page_icon="🔮")
st.header("ATS Tracking system")
input_text = st.text_area("Job Description", key="input")
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

submit1 = st.button("Tell me about your resume")

## submit2 = st.button("How can I improvise my skills")

submit3 = st.button("Match Percentile")

input_prompt1 = """
    You are an experienced HR with Tech experience in the field of data science , 
    full stak web development, Big Data engineering, Devops, Data Analyst and your task is to
    review the provided resume against the Job Description for these profiles. Please share 
    your professional evaluation on whether the candidate's profile alligns with their job roles.
     Highlight the strengths and weaknesses of the applicant in relation to the specified job
requirements. """


input_prompt3 = """
    You are a skilled ATS (Application tracking system) scanner with deep understanding of Data science
     , full stak web development, Big Data engineering, Devops, Data Analyst and ATS
      functionality. Your task is to review the provided resume against the Job Description 
      and give the percentage of match if the  resume matches the job description.
      First the output should come as percentage and then the keywords missing and 
      last final thoughts.
      """

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt1)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF resume")

if submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt3)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF resume")