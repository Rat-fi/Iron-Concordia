import sqlite3
import json

# Path to your JSON file
json_file = 'CUFitness/script/data.json'

# Path to your SQLite database file (default Django DB)
db_file = 'CUFitness/db.sqlite3'

def load_data(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def insert_data_into_db(data, db_path):
    """Insert data into each table specified in the JSON file."""
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Loop through each table in the JSON file
    for table_name, rows in data.items():
        for row in rows:
            # Create a list of columns and values from the dictionary
            columns = ', '.join(row.keys())
            placeholders = ', '.join('?' for _ in row)
            values = list(row.values())
            
            # Build and execute the SQL INSERT statement
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(query, values)
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("Data inserted successfully.")

if __name__ == '__main__':
    # Load the data from the JSON file
    data = load_data(json_file)
    
    # Insert the loaded data into the SQLite database
    insert_data_into_db(data, db_file)
