def get_create_insert_query_promt():
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