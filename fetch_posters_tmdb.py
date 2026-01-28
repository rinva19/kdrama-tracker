import requests
import time
from airtable_credentials import API_KEY, TMDB_API_KEY

# Airtable setup
BASE_ID = "appst48a7a8w57s0O"
TABLE_NAME = "Korean%20Dramas"
AIRTABLE_URL = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
airtable_headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# TMDb setup
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

def search_tmdb_drama(drama_title, year=None):
    """Search TMDb for drama and get poster URL"""
    try:
        # Search for TV show
        search_url = f"{TMDB_BASE_URL}/search/tv"
        params = {
            "api_key": TMDB_API_KEY,
            "query": drama_title,
            "language": "en-US"
        }
        
        if year:
            params["first_air_date_year"] = year
        
        response = requests.get(search_url, params=params)
        print(f"  API Response Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"  ❌ TMDb API error for: {drama_title}")
            print(f"  Response: {response.text[:200]}")
        
        data = response.json()
        results = data.get('results', [])
        
        if not results:
            print(f"  ⚠️  No results found for: {drama_title}")
            return None
        
        # Get first result's poster
        first_result = results[0]
        poster_path = first_result.get('poster_path')
        
        if poster_path:
            poster_url = f"{TMDB_IMAGE_BASE}{poster_path}"
            print(f"  ✅ Found poster: {drama_title} ({first_result.get('name', 'Unknown')})")
            return poster_url
        else:
            print(f"  ⚠️  No poster available for: {drama_title}")
            return None
            
    except Exception as e:
        print(f"  ❌ Error for {drama_title}: {str(e)}")
        return None

def update_airtable_poster(record_id, poster_url):
    """Update Airtable record with poster URL"""
    try:
        url = f"{AIRTABLE_URL}/{record_id}"
        data = {
            "fields": {
                "Poster URL": poster_url
            }
        }
        response = requests.patch(url, json=data, headers=airtable_headers)
        return response.status_code == 200
    except Exception as e:
        print(f"  ❌ Failed to update Airtable: {str(e)}")
        return False

def main():
    print("🎬 Starting TMDb poster fetcher (TEST MODE - 5 dramas)...\n")
    
    # Fetch ALL dramas from Airtable (handle pagination)
    all_records = []
    offset = None
    
    while True:
        params = {"offset": offset} if offset else {}
        response = requests.get(AIRTABLE_URL, headers=airtable_headers, params=params)
        data = response.json()
        all_records.extend(data.get('records', []))
        offset = data.get('offset')
        if not offset:
            break
    
    records = all_records
    
    # Process ALL dramas
    test_records = records  # Remove [:5] to process all
    
    print(f"Testing with {len(test_records)} dramas\n")
    
    success_count = 0
    fail_count = 0
    
    for i, record in enumerate(test_records, 1):
        record_id = record['id']
        fields = record['fields']
        title = fields.get('Title', 'Unknown')
        year = fields.get('Year Released')
        
        # Skip if already has poster URL
        existing_poster = fields.get('Poster URL')
        if existing_poster:
            print(f"[{i}/{len(test_records)}] Skipping: {title} (already has poster)")
            success_count += 1
            continue
        
        print(f"[{i}/{len(test_records)}] Processing: {title}")
        
        # Search TMDb for poster
        poster_url = search_tmdb_drama(title, year)
        
        if poster_url:
            # Update Airtable
            if update_airtable_poster(record_id, poster_url):
                success_count += 1
            else:
                fail_count += 1
        else:
            fail_count += 1
        
        # Be polite to TMDb API
        time.sleep(0.3)
        
    print(f"\n✅ Test complete! Success: {success_count}, Failed: {fail_count}")
    print("If results look good, change [:5] to process all dramas!")

if __name__ == "__main__":
    main()