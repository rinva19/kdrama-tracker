# Import credentials
from airtable_credentials import API_KEY
from pyairtable import Api
import json

# Database info
BASE_ID = "appst48a7a8w57s0O"
TABLE_NAME = "Korean Dramas"

# Connect to Airtable
api = Api(API_KEY)
table = api.table(BASE_ID, TABLE_NAME)
records = table.all()

# Transform each drama into clean format
clean_dramas = []
for record in records:
    fields = record['fields']
    
    clean_drama = {
        'title': fields.get('Title', 'Unknown'),
        'rating': fields.get('Rating'),
        'year': fields.get('Year Released'),
        'genres': fields.get('Genre', []),
        'country': fields.get('Country of Origin'),
        'poster': fields.get('Poster', [{}])[0].get('url') if fields.get('Poster') else None,
        'status': fields.get('Viewing Status', ['Unknown'])[0],
        'channel': fields.get('Channel', []),
    }
    
    clean_dramas.append(clean_drama)

# Save to JSON file
with open('dramas.json', 'w') as f:
    json.dump(clean_dramas, f, indent=2)

print(f"Transformed {len(clean_dramas)} dramas!")
print("\nFirst drama in clean format:")
print(json.dumps(clean_dramas[0], indent=2))