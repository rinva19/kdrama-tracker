import requests
import time
from airtable_credentials import API_KEY, TMDB_API_KEY

# Airtable setup
BASE_ID = "appst48a7a8w57s0O"
ACTORS_TABLE = "Actors"
ACTRESSES_TABLE = "Actresses"
AIRTABLE_URL_BASE = f"https://api.airtable.com/v0/{BASE_ID}"
airtable_headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# TMDb setup
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w185"

def search_tmdb_person(person_name):
    """Search TMDb for person and get profile image URL"""
    try:
        # Search for person
        search_url = f"{TMDB_BASE_URL}/search/person"
        params = {
            "api_key": TMDB_API_KEY,
            "query": person_name,
            "language": "en-US"
        }

        response = requests.get(search_url, params=params)

        if response.status_code != 200:
            print(f"  ❌ TMDb API error for: {person_name}")
            return None

        data = response.json()
        results = data.get('results', [])

        if not results:
            print(f"  ⚠️  No results found for: {person_name}")
            return None

        # Get first result's profile image
        first_result = results[0]
        profile_path = first_result.get('profile_path')

        if not profile_path:
            print(f"  ⚠️  No profile image for: {person_name}")
            return None

        profile_url = f"{TMDB_IMAGE_BASE}{profile_path}"
        print(f"  ✅ Found image: {person_name} ({first_result.get('name', 'Unknown')})")
        return profile_url

    except Exception as e:
        print(f"  ❌ Error for {person_name}: {str(e)}")
        return None

def update_airtable_record(table_name, record_id, profile_url):
    """Update Airtable record with profile image URL"""
    try:
        url = f"{AIRTABLE_URL_BASE}/{table_name}/{record_id}"
        data = {
            "fields": {
                "Profile Image URL": profile_url
            }
        }
        response = requests.patch(url, json=data, headers=airtable_headers)
        return response.status_code == 200
    except Exception as e:
        print(f"  ❌ Failed to update Airtable: {str(e)}")
        return False

def fetch_table_records(table_name):
    """Fetch all records from an Airtable table"""
    all_records = []
    offset = None

    while True:
        params = {"offset": offset} if offset else {}
        response = requests.get(f"{AIRTABLE_URL_BASE}/{table_name}",
                              headers=airtable_headers, params=params)
        data = response.json()
        all_records.extend(data.get('records', []))
        offset = data.get('offset')
        if not offset:
            break

    return all_records

def process_table(table_name, table_display_name):
    """Process all records in a table"""
    print(f"\n{'='*60}")
    print(f"Processing {table_display_name}")
    print(f"{'='*60}\n")

    records = fetch_table_records(table_name)
    print(f"Found {len(records)} {table_display_name.lower()}\n")

    success_count = 0
    skip_count = 0
    fail_count = 0

    for i, record in enumerate(records, 1):
        record_id = record['id']
        fields = record['fields']
        name = fields.get('Name', 'Unknown')

        # Skip if already has profile image
        existing_image = fields.get('Profile Image URL')
        if existing_image:
            print(f"[{i}/{len(records)}] Skipping: {name} (already has image)")
            skip_count += 1
            continue

        print(f"[{i}/{len(records)}] Processing: {name}")

        # Search TMDb for profile image
        profile_url = search_tmdb_person(name)

        if profile_url:
            # Update Airtable
            if update_airtable_record(table_name, record_id, profile_url):
                success_count += 1
            else:
                fail_count += 1
        else:
            fail_count += 1

        # Be polite to TMDb API
        time.sleep(0.3)

    print(f"\n{table_display_name} Summary:")
    print(f"  ✅ Updated: {success_count}")
    print(f"  ⏭️  Skipped: {skip_count}")
    print(f"  ❌ Failed: {fail_count}")

def main():
    print("🎭 Starting TMDb Actor/Actress Image Fetcher...\n")

    # Process actors
    process_table(ACTORS_TABLE, "Actors")

    # Process actresses
    process_table(ACTRESSES_TABLE, "Actresses")

    print(f"\n{'='*60}")
    print("✅ All done!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
