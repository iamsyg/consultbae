import os
from dotenv import load_dotenv
from supabase import create_client, Client

from normalize_data.normalize_data1 import normalize_data1
from normalize_data.normalize_data2 import normalize_data2
from normalize_data.normalize_data3 import normalize_data3

import pandas as pd

# Load environment variables
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# Initialize client
supabase: Client = create_client(url, key)

data1 = pd.read_csv(r"C:\\Personal-space\\projects\\source1_naukri_applicants.csv")
data2 = pd.read_csv(r"C:\\Personal-space\\projects\\source2_gig_workers.csv")
data3 = pd.read_csv(r"C:\\Personal-space\\projects\\source3_cbnexus_contacts.csv")

naukari_normalized = normalize_data1(data1)
cbnexus_normalized = normalize_data2(data2)
gig_workers_normalized = normalize_data3(data3)

print(gig_workers_normalized.head(5))

# # Insert data into a table
# data = {"name": "John Doe", "email": "john@example.com"}
# insert_response = supabase.table("people").insert(data).execute()
# print("Inserted:", insert_response.data)

# # Read data from a table
# select_response = supabase.table("people").select("*").execute()
# print("People:", select_response.data)
