import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import PyPDF2 as pdf

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

## Gemini pro response
def get_gemini_response(input, pdf_content, prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_text(uploaded_file):
    pdf_reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

input_prompt = """
Act like a very skilled and experienced ATS(Application Tracking System) with deep 
understanding of tech field, software development, data science, data engineering,
DevOps, Data Analyst. Your task is to review the provided resume against the Job Description.
You must consider the job market is very competitive and you should provide best assistence 
for improving there resume. Assisgn the percentage Matching based on jd and the missing
 keywords with high accuracy.

"""

## Streamlit app code
st.set_page_config(page_title="ATS Resume expert", page_icon="🔮")
st.text("ATS Tracking system")
jd=st.text_area("Paste the job description here")
uploaded_file = st.file_uploader("Upload a PDF Resume", type=["pdf"], help="Upload the resume in PDF format")

submit = st.button("Submit")

if submit: 
    if uploaded_file is not None:
        pdf_text = input_pdf_text(uploaded_file)
        response = get_gemini_response(pdf_text, jd, input_prompt)
        st.subheader(response)
    else:
        st.error("Please upload a PDF file")