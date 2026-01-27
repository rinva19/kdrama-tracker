from airtable_credentials import API_KEY

# Database info
BASE_ID = "appst48a7a8w57s0O"
TABLE_NAME = "Korean Dramas"

# Connect and fetch
from pyairtable import Api
api = Api(API_KEY)
table = api.table(BASE_ID, TABLE_NAME)
records = table.all()

# Show what we got
print(f"Found {len(records)} dramas!")
print("\nFirst drama:")
print(records[0]['fields'])