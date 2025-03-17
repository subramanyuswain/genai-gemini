def generate_item_insert_query_promt():
    """
    Generates an SQL INSERT query from a grocery bill image.

    Args:
        image: A PIL Image object representing the grocery bill.

    Returns:
        A string containing the SQL INSERT query or an error message.
    """

    prompt = """
    You are an expert in reading grocery bills and extracting relevant information. 
    Your task is to extract items, quantity, price and taxes from the provided grocery bill image.
    Generate a SQL INSERT query to add the extracted data into a table named 'grocery_items'.
    
    The table 'grocery_items' has the following columns:
    - item_name (TEXT): The name of the grocery item.
    - quantity (REAL): The quantity of the item.
    - unit (TEXT): The measureing unit of the item, it would be number of items if Integer and kgs if decimal NA if not available in the bill.
    - rate (REAL): The per unit price of the item mention NA if not available in the bill.
    - price (REAL): The price of the item.
    - taxes (REAL): The taxes applied to the item.

    Make sure to only output the sql query without any additional text. If you dont understand the image, say "Could not extract data from image".

    Example:
    INSERT INTO grocery_items (item_name, quantity, unit, rate, price, taxes) VALUES ('Apple', 2, 'NUMBER', 300.00, 600.00, 1.05);
    INSERT INTO grocery_items (item_name, quantity, price, taxes) VALUES ('Milk', 1, 'NUMBER', 2.00, 3.99, 0.05);
    INSERT INTO grocery_items (item_name, quantity, price, taxes) VALUES ('Rice', 2.5, 'KG', 10.00, 25, 0.05);
    INSERT INTO grocery_items (item_name, quantity, price, taxes) VALUES ('Sweet Corn', 5, 'NUMBER', 5.00, 25, 0.05);
    """

    return prompt

def generate_bill_metadata_insert_query_promt(metadata, table_name="grocery_bills"):
    """
    Generates an SQL INSERT query using the Gemini API.

    Args:
        metadata (dict): The extracted metadata.
        table_name (str): The name of the table to insert into.

    Returns:
        str: The SQL INSERT query, or an error message if there's a problem.
    """

    if not metadata:
        return "Error: No metadata provided."

    
    prompt = f"""
    You are an expert SQL query writer.
    Generate a SQL INSERT query to add data into a table named '{table_name}'.
    The following metadata needs to be inserted:
    {metadata}

    The table '{table_name}' has the following columns:
    - date (DATE): The date of the bill.
    - time (TIME): The time of the bill.
    - grand_total (REAL): The total amount of the bill.
    - transaction_id (TEXT): The unique identifier for the bill.
    - payment_mode (TEXT): The payment method used.
    - item_count (INTEGER): the number of items in the bill.

    Ensure the data types in the query match the column types.
    Make sure to only output the sql query without any additional text. If you dont understand the data, say "Could not create query".

    Example:
    INSERT INTO grocery_bills (date, time, grand_total, transaction_id, payment_mode,item_count) VALUES ('2023-10-27', '10:30:00', 56.78, 'TXN12345', 'card', 5);
    """
    return prompt
