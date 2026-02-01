# Import credentials
from airtable_credentials import API_KEY
from pyairtable import Api
import json

# Database info
BASE_ID = "appst48a7a8w57s0O"
TABLE_NAME = "Korean Dramas"
ACTORS_TABLE = "Actors"
ACTRESSES_TABLE = "Actresses"

# Connect to Airtable
api = Api(API_KEY)
drama_table = api.table(BASE_ID, TABLE_NAME)
actors_table = api.table(BASE_ID, ACTORS_TABLE)
actresses_table = api.table(BASE_ID, ACTRESSES_TABLE)

# Fetch all records
drama_records = drama_table.all()
actor_records = actors_table.all()
actress_records = actresses_table.all()

# Create lookup dictionaries for actors/actresses (with profile images)
actor_lookup = {
    record['id']: {
        'name': record['fields'].get('Name', 'Unknown'),
        'profileImage': record['fields'].get('Profile Image URL')
    }
    for record in actor_records
}
actress_lookup = {
    record['id']: {
        'name': record['fields'].get('Name', 'Unknown'),
        'profileImage': record['fields'].get('Profile Image URL')
    }
    for record in actress_records
}

print(f"Loaded {len(actor_lookup)} actors and {len(actress_lookup)} actresses")

# Transform each drama into clean format
clean_dramas = []
for record in drama_records:
    fields = record['fields']
    
    # Get actor names and images from IDs
    actor_ids = fields.get('Actors', [])
    actor_data = [actor_lookup.get(actor_id, {'name': 'Unknown', 'profileImage': None}) for actor_id in actor_ids]
    actor_names = [a['name'] for a in actor_data]
    actor_images = [a['profileImage'] for a in actor_data]

    # Get actress names and images from IDs
    actress_ids = fields.get('Actresses', [])
    actress_data = [actress_lookup.get(actress_id, {'name': 'Unknown', 'profileImage': None}) for actress_id in actress_ids]
    actress_names = [a['name'] for a in actress_data]
    actress_images = [a['profileImage'] for a in actress_data]
    
    clean_drama = {
        'title': fields.get('Title', 'Unknown'),
        'rating': fields.get('Rating'),
        'year': fields.get('Year Released'),
        'genres': fields.get('Genre', []),
        'country': fields.get('Country of Origin'),
        'poster': fields.get('Poster URL'),
        'plotSummary': fields.get('Plot Summary', ''),
        'status': fields.get('Viewing Status', ['Unknown'])[0],
        'channel': fields.get('Channel', []),
        'actors': actor_names,
        'actresses': actress_names,
        'actorImages': actor_images,
        'actressImages': actress_images,
        'dateFinished': fields.get('Date Finished'),
        'kdramaGroup': fields.get('Kdrama Mamas'),
    }
    
    clean_dramas.append(clean_drama)

# Save to JSON file
with open('dramas.json', 'w') as f:
    json.dump(clean_dramas, f, indent=2)

print(f"Transformed {len(clean_dramas)} dramas!")
print("\nFirst drama in clean format:")
print(json.dumps(clean_dramas[0], indent=2))