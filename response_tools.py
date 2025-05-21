import psycopg2
import re
import os
import json
import decimal
from urllib.parse import urlparse
from psycopg2.extras import RealDictCursor
from django.conf import settings

def clean_response(raw_response):
    try:
        # Step 1: Remove Markdown code block formatting
        clean_string = raw_response.strip().replace("```json", "").replace("```", "")

        # Step 2: Replace escaped newline chars
        clean_string = clean_string.replace("\\n", "\n")

        # Step 3: Ensure proper JSON format if input was double-escaped
        # Remove backslashes before quotes (common mistake)
        clean_string = clean_string.replace('\\"', '"')

        print("Cleaned string:", clean_string)

        # Step 4: Parse JSON
        data = json.loads(clean_string)

        output_data = {
            "reply": data["reply"],
            "is_query_generated": bool(data["is_query_generated"]),
            "table_display": bool(data["table_display"])
        }

        if output_data["is_query_generated"]:
            output_data["query"] = data["sql_query"]
        else:
            output_data["query"] = False
            output_data["table_display"] = False

        # Save to static/json/output_data.json
        static_json_dir = os.path.join(settings.BASE_DIR, 'static', 'json')
        os.makedirs(static_json_dir, exist_ok=True)
        file_path = os.path.join(static_json_dir, 'output_data.json')

        with open(file_path, 'w') as json_file:
            json.dump(output_data, json_file, indent=4)

        return output_data

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None



import mysql.connector
import json
from decimal import Decimal  # Import Decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def fetch_from_db(query):
    try:
        # Parse DATABASE_URL
        DATABASE_URL = "postgresql://postgres:123456@localhost/livespace"
        result = urlparse(DATABASE_URL)
        
        conn = psycopg2.connect(
            database=result.path.lstrip('/'),
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port or 5432
        )
        
        print("Connected to PostgreSQL database")
        
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query)
        products = cursor.fetchall()
        
        static_json_dir = os.path.join(settings.BASE_DIR, 'static', 'json')
        os.makedirs(static_json_dir, exist_ok=True)
        file_path = os.path.join(static_json_dir, 'property_data.json')

        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(products, json_file, indent=4, cls=DecimalEncoder)
        
        print("Data saved to property_data.json")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"Error: {e}")
    
    return False



# def clean_response(raw_response):
#     try:
#         clean_string = raw_response.replace("```json\n", "").replace("```", "")
#         clean_string = re.sub(r'(?<=[^\\])"(?=[^":,\}\]\n])', r'\"', clean_string)
#         print("Cleaned string:", clean_string)

#         data = json.loads(clean_string)

#         output_data = {
#             "reply": data["reply"],
#             "is_query_generated": bool(data["is_query_generated"]),
#             "table_display": bool(data["table_display"])
#             # "property_query": bool(data["property_query"])
#         }

#         if output_data["is_query_generated"]:
#             output_data["query"] = data["sql_query"]
#         else:
#             output_data["query"] = False
#             output_data["table_display"] = False

#         static_json_dir = os.path.join(settings.BASE_DIR, 'static', 'json')
#         os.makedirs(static_json_dir, exist_ok=True)
#         file_path = os.path.join(static_json_dir, 'output_data.json')

#         with open(file_path, 'w') as json_file:
#             json.dump(output_data, json_file, indent=4)

#         return output_data
#         print("JSON data has been saved as 'output_data.json'")

#     except json.JSONDecodeError as e:
#         print(f"Error decoding JSON: {e}")

#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")

#     return None


# Custom JSON encoder to convert Decimal to float
# class DecimalEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, Decimal):
#             return float(obj)  # Convert Decimal to float
#         return super().default(obj)

# def fetch_from_db(query):
#     try:
#         # Establish connection
#         conn = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="ABcd@#12",
#             database="property_data"
#         )
        
#         if conn.is_connected():
#             print("Connected to MySQL database")
        
#         cursor = conn.cursor(dictionary=True)
        
#         cursor.execute(query)
#         products = cursor.fetchall()
        
#         static_json_dir = os.path.join(settings.BASE_DIR, 'static', 'json')
#         os.makedirs(static_json_dir, exist_ok=True)
#         file_path = os.path.join(static_json_dir, 'property_data.json')

#         with open(file_path, "w", encoding="utf-8") as json_file:
#             json.dump(products, json_file, indent=4, cls=DecimalEncoder)
        
#         print("Data saved to products.json")
        
#         cursor.close()
#         conn.close()
#         return True
        
#     except mysql.connector.Error as e:
#         print(f"Error: {e}")
    
#     return False
