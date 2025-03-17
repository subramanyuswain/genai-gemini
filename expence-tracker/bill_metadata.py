"""
PROMPT USED TO GENERATE BELOW CODE:

read an image of a grocery bill , extract data such as bill date, time, bill number, 
number of items, grand total, payment mode and create SQL insert queries to insert all 
the extracted data into a table
"""

import google.generativeai as genai
import os
import io
from PIL import Image
import base64
from dotenv import load_dotenv
from methods import *
from utils import bytes_to_string
import re
from datetime import datetime

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
def extract_grocery_bill_metadata(bill_text):
    """
    Extracts metadata like date, time, grand total, bill/transaction ID, and payment mode from a grocery bill text.

    Args:
        bill_text (str): The text content of the grocery bill.

    Returns:
        dict: A dictionary containing the extracted metadata, or None if extraction fails.
    """

    metadata = {}

    # Extract Date (looking for various date formats)
    date_patterns = [
        r'Date:\s*(\d{2}[/-]\d{2}[/-]\d{4})',  # DD/MM/YYYY or DD-MM-YYYY
        r'(\d{4}[/-]\d{2}[/-]\d{2})',  # YYYY/MM/DD or YYYY-MM-DD
        r'(\w{3}\s+\d{1,2},\s+\d{4})',  # Month Day, Year (e.g., Jan 15, 2024)
        r'(\d{1,2}\s+\w{3}\s+\d{4})', # Day Month Year(e.g., 15 Jan 2024)
        r'(\d{2}[/-]\d{2}[/-]\d{2})' # DD/MM/YY or DD-MM-YY
    ]

    for pattern in date_patterns:
        date_match = re.search(pattern, bill_text, re.IGNORECASE)
        if date_match:
            date_str = date_match.group(1)
            try:
                # Attempt to parse the date using different formats
                for fmt in ('%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d', '%Y-%m-%d', '%b %d, %Y', '%d %b %Y','%d/%m/%y', '%d-%m-%y'):
                    try:
                        metadata['date'] = datetime.strptime(date_str, fmt).strftime('%Y-%m-%d') #standardize date format
                        break
                    except ValueError:
                        pass
                else:
                    print(f"Warning: Could not parse date: {date_str}")
                    metadata['date'] = None # or handle the error in another way
                break #found a date, move on
            except ValueError:
                print(f"Warning: Could not parse date: {date_str}")
                metadata['date'] = None
            break

    # Extract Time (looking for various time formats)
    time_patterns = [
        r'Time:\s*(\d{1,2}:\d{2}\s*[AP]M)',  # HH:MM AM/PM
        r'(\d{1,2}:\d{2}\s*[AP]M)',
        r'Time:\s*(\d{1,2}:\d{2})',  # HH:MM (24-hour format)
        r'(\d{1,2}:\d{2})', # HH:MM(24-hour format)
    ]
    for pattern in time_patterns:
        time_match = re.search(pattern, bill_text, re.IGNORECASE)
        if time_match:
            time_str = time_match.group(1)
            try:
                #Attempt to parse time with different formats
                for fmt in ('%I:%M %p', '%H:%M'):
                    try:
                        metadata['time'] = datetime.strptime(time_str,fmt).strftime('%H:%M:%S')
                        break
                    except ValueError:
                        pass
                else:
                    print(f"Warning: Could not parse time: {time_str}")
                    metadata['time'] = None
                break
            except ValueError:
                print(f"Warning: Could not parse time: {time_str}")
                metadata['time'] = None
                break

    # Extract Grand Total (looking for various total formats)
    total_patterns = [
        r'Grand Total:\s*([\$₹]?\s*[\d,]+\.\d{2})',
        r'Total:\s*([\$₹]?\s*[\d,]+\.\d{2})',
        r'Amount Due:\s*([\$₹]?\s*[\d,]+\.\d{2})',
        r'([\$₹]?\s*[\d,]+\.\d{2})\s*$', # if total is on last line
        r'Total Amount:\s*([\$₹]?\s*[\d,]+\.\d{2})'
    ]

    for pattern in total_patterns:
        total_match = re.search(pattern, bill_text, re.IGNORECASE)
        if total_match:
            total_str = total_match.group(1).replace(',', '').replace('$', '').replace('₹','').strip()
            try:
                metadata['grand_total'] = float(total_str)
            except ValueError:
                print(f"Warning: Could not parse total: {total_str}")
                metadata['grand_total'] = None
            break

    # Extract Bill/Transaction ID (looking for various ID formats)
    id_patterns = [
        r'Transaction ID:\s*([\w\d-]+)',
        r'Txn ID:\s*([\w\d-]+)',
        r'Invoice #:\s*([\w\d-]+)',
        r'Order #:\s*([\w\d-]+)',
        r'Receipt #:\s*([\w\d-]+)',
        r'Ref #:\s*([\w\d-]+)',
        r'([\w\d-]+)\s*Transaction',
        r'Bill #:\s*([\w\d-]+)'
    ]

    for pattern in id_patterns:
        id_match = re.search(pattern, bill_text, re.IGNORECASE)
        if id_match:
            metadata['transaction_id'] = id_match.group(1)
            break
    
    # Extract Payment Mode (looking for various payment mode keywords)
    payment_mode_keywords = [
        r'Cash',
        r'Card',
        r'UPI',
        r'Credit',
        r'Debit',
        r'Online',
        r'Wallet',
        r'Net Banking',
        r'GPay',
        r'PhonePe',
        r'Paytm'
    ]
    payment_mode_pattern = r'(?i)' + '|'.join(payment_mode_keywords) # (?i) for case insensitive
    payment_match = re.search(payment_mode_pattern, bill_text)
    if payment_match:
        metadata['payment_mode'] = payment_match.group(0).lower()
    else:
        metadata['payment_mode'] = "NA"

    return metadata

def generate_sql_query_for_bill_metadata(image, st):
    """
    Extracts metadata from bill image and generates SQL query
    Args:
        image: image of bill
    Returns:
        sql query string
    """
    image_bytes = image_to_bytes(image)
    prompt = "Extract text from the image"
    try:
        response = get_gemini_response(image_bytes, prompt)
        response_string = bytes_to_string(response.encode())
        if response_string is not None:
             metadata = extract_grocery_bill_metadata(response_string)
        else:
            st.error("Could not extract data from image. Try another one")
            return "Could not extract data from image"
        if metadata is not None:
            item_count_prompt = "From the previous data, give me only the number of items in the bill"
            item_count_text = get_gemini_response(image_bytes, item_count_prompt)
            metadata['item_count'] = item_count_text

            metadata_prompt = generate_bill_metadata_insert_query_promt(metadata)
            sql_query = get_gemini_response(image_bytes,metadata_prompt)
            return sql_query
        else:
            st.error("Could not extract data from image. Try another one")
            return "Could not extract data from image"
    except Exception as e:
        return f"Error generating SQL query: {e}"
    
def execute_bill_metadata(image, st):
        sql_query = generate_sql_query_for_bill_metadata(image, st)
        return sql_query



# def main():
#     """
#     Main function to run the streamlit app.
#     """
#     st.title("Grocery Bill to SQL Converter")

#     uploaded_file = st.file_uploader("Upload a grocery bill image", type=["jpg", "jpeg", "png"])

#     if uploaded_file is not None:
#         image = Image.open(uploaded_file)
#         st.image(image, caption="Uploaded Grocery Bill", use_container_width=True)
        
#         if st.button("Generate SQL Query for Bill Metadata"):
#             sql_query = generate_sql_query_for_bill_metadata(image)
#             st.text_area("Generated SQL Query for Bill Metadata", value=sql_query, height=200)
#             if sql_query=="Could not create query" or sql_query == "Could not extract data from image":
#                  st.error("Could not extract data from image. Try another one")

# if __name__ == "__main__":
#     main()

