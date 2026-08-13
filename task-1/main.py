import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# Initialize client
supabase: Client = create_client(url, key)

# Insert data into a table
data = {"name": "John Doe", "email": "john@example.com"}
insert_response = supabase.table("people").insert(data).execute()
print("Inserted:", insert_response.data)

# Read data from a table
select_response = supabase.table("people").select("*").execute()
print("People:", select_response.data)
