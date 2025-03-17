Purpose

    Intent - This code is intended to read through a grocery bill and generate SQL insert queries. The sql queries can thereafter be used to insert expence records to SQLlite db.

    The SQL data can be used to analyze expenses and create analytics dashboards on it.


        1. Create a DB schema to store the item details from bill into the database

            - Create a code Generative AI code that can generate Insert query from the image of the bills
            - Create a code that can insert query to insert data into the created table schema in 2

        2. Create another table to store the bill metadata such as date of purchase, invoice number, Grand total , etc..

        3. Create a AI code to generate queries that can analyse the expences and create charts based on the data in the tables

        4. As always keep improving the design so that it can be more convinient to use.

Key Changes and Explanations:

    1. generate_sql_query_for_bill_metadata Function (in app.py):

        a. Item Count Extraction:
            - item_count_prompt = "From the previous data, give me only the number of items in the bill": A new prompt is created to ask Gemini to determine the number of items.
            - item_count_text = get_gemini_response(image_bytes, item_count_prompt): This sends the new prompt to Gemini to get the item count.
            - metadata['item_count'] = item_count_text: adds the item count to metadata dictionary.
        b. bytes to string:
            - response_string = bytes_to_string(response.encode()): converts the response to string before extracting metadata from it.
            - Error handling: if the response_string is None, then Could not extract data from image. Try another one is displayed.
        c. Error handling: if metadata is not None check is added before asking for item count. if metadata is None then an error is displayed.

    2. generate_bill_metadata_insert_query_promt Function (in methods.py):

            a. New Column:
            - item_count (INTEGER): the number of items in the bill. is added to the table description.
            b. Updated Example:
            - The example now includes item_count.
    3. extract_grocery_bill_metadata Function (in bill_metadata.py):

            - remains same.

    4. bytes_to_string Function (in utils.py):

            - added bytes_to_string function to the utils.py file.

    5. Imports:

            - from utils import bytes_to_string is added to the app.py file.

    Workflow:

        1. Image Upload: The user uploads a grocery bill image.
        2. Text Extraction: Gemini extracts the text from the image.
        3. Convert to string: The extracted text is converted to string using bytes_to_string.
        4. Metadata Extraction: extract_grocery_bill_metadata parses the text to get bill date, time, number, grand total, and payment mode.
        5. Item Count: Gemini is asked to count the number of items based on the image content.
        6. SQL Prompt: generate_bill_metadata_insert_query_promt creates the SQL query prompt with the metadata and item count.
        7. SQL Generation: Gemini generates the final SQL INSERT query.
        8. Display: the generated sql query is displayed.

    Key Improvements:

        1. Item Count: The code now correctly extracts the item count and includes it in the SQL query.
        2. robust: code is robust enough to handle None values.
        3. bytes to string conversion: code handles bytes to string conversion.
        4. Clearer Prompts: The prompts are well-defined and specific.
        5. Error Handling: The code handles potential errors.
        6. code is modular: the code is now more modularized.
        7. Correct SQL: The generated SQL queries now match the updated table structure.
        8. Well Structured: code is well stuctured with methods, bill_metadata and utils files.


    How to Run:

        1. Install Dependencies:
            pip install streamlit google-generativeai python-dotenv pillow

        2. Set Up API Key:
            Create a .env file in the same directory as your script.

        3. Add your Google Generative AI API key:
            GOOGLE_API_KEY=YOUR_API_KEY_HERE

        5. Save Files: Save the code above as the following:
            app.py (main code)
            methods.py (helper functions)
            bill_metadata.py (metadata extraction logic)
            utils.py (utility functions)

        6. Run:
            streamlit run app.py