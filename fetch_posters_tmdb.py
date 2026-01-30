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
    """Search TMDb for drama and get poster URL and plot summary"""
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
        
        if response.status_code != 200:
            print(f"  ❌ TMDb API error for: {drama_title}")
            return None, None
        
        data = response.json()
        results = data.get('results', [])
        
        if not results:
            print(f"  ⚠️  No results found for: {drama_title}")
            return None, None
        
        # Get first result's poster and summary
        first_result = results[0]
        poster_path = first_result.get('poster_path')
        overview = first_result.get('overview', '')
        
        poster_url = f"{TMDB_IMAGE_BASE}{poster_path}" if poster_path else None
        
        if poster_url:
            print(f"  ✅ Found data: {drama_title} ({first_result.get('name', 'Unknown')})")
        else:
            print(f"  ⚠️  No poster available for: {drama_title}")
            
        return poster_url, overview
            
    except Exception as e:
        print(f"  ❌ Error for {drama_title}: {str(e)}")
        return None, None

def update_airtable_data(record_id, poster_url, plot_summary):
    """Update Airtable record with poster URL and plot summary"""
    try:
        url = f"{AIRTABLE_URL}/{record_id}"
        
        # Build fields to update (only include what we have)
        fields = {}
        if poster_url:
            fields["Poster URL"] = poster_url
        if plot_summary:
            fields["Plot Summary"] = plot_summary
            
        if not fields:
            return False
            
        data = {"fields": fields}
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
        
        # Skip if already has BOTH poster URL and plot summary
        existing_poster = fields.get('Poster URL')
        existing_summary = fields.get('Plot Summary')
        if existing_poster and existing_summary:
            print(f"[{i}/{len(test_records)}] Skipping: {title} (already has data)")
            success_count += 1
            continue
        
        print(f"[{i}/{len(test_records)}] Processing: {title}")
        
        # Search TMDb for poster and summary
        poster_url, plot_summary = search_tmdb_drama(title, year)
        
        if poster_url or plot_summary:
            # Update Airtable with both
            if update_airtable_data(record_id, poster_url, plot_summary):
                success_count += 1
            else:
                fail_count += 1
        else:
            fail_count += 1
        
        # Be polite to TMDb API
        time.sleep(0.3)
        
    print(f"\n✅ Complete! Success: {success_count}, Failed: {fail_count}")

if __name__ == "__main__":
    main()