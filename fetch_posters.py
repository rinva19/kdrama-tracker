import requests
from bs4 import BeautifulSoup
import time
from airtable_credentials import API_KEY

# Airtable setup - put your values here
BASE_ID = "appst48a7a8w57s0O"
TABLE_NAME = "Korean%20Dramas"  # URL-encoded space
AIRTABLE_URL = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def search_asianwiki_poster(drama_title):
    """Search AsianWiki for drama and extract poster URL"""
    try:
        # Format search URL
        search_title = drama_title.replace(" ", "_")
        asianwiki_url = f"https://asianwiki.com/{search_title}"
        print(f"  Trying URL: {asianwiki_url}")
        
        # Fetch the page (with browser headers to avoid blocking)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(asianwiki_url, headers=headers)
        print(f"  Response code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"  ❌ Page not found for: {drama_title}")
            print(f"  First 200 chars of response: {response.text[:200]}")
            return None
            
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the poster image in thumbinner div
        thumbinner = soup.find('div', {'class': 'thumbinner'})
        if thumbinner:
            img = thumbinner.find('img', {'class': 'thumbimage'})
            if img and img.get('src'):
                poster_url = "https://asianwiki.com" + img['src']
                print(f"  ✅ Found poster: {drama_title}")
                return poster_url
        
        print(f"  ⚠️  No poster found for: {drama_title}")
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
        response = requests.patch(url, json=data, headers=headers)
        return response.status_code == 200
    except Exception as e:
        print(f"  ❌ Failed to update Airtable: {str(e)}")
        return False

def main():
    print("🎬 Starting poster fetcher (TEST MODE - 5 dramas)...\n")
    
    # Fetch all dramas from Airtable
    # Fetch all dramas from Airtable
    response = requests.get(AIRTABLE_URL, headers=headers)
    print(f"API Response Status: {response.status_code}")
    print(f"API Response: {response.text[:500]}")  # First 500 chars
    records = response.json().get('records', [])
    
    # TEST: Only process first 5 dramas
    test_records = records[:5]
    
    print(f"Testing with {len(test_records)} dramas\n")
    
    success_count = 0
    fail_count = 0
    
    for i, record in enumerate(test_records, 1):
        record_id = record['id']
        fields = record['fields']
        title = fields.get('Title', 'Unknown')
        
        print(f"[{i}/{len(test_records)}] Processing: {title}")
        
        # Search for poster
        poster_url = search_asianwiki_poster(title)
        
        if poster_url:
            # Update Airtable
            if update_airtable_poster(record_id, poster_url):
                success_count += 1
            else:
                fail_count += 1
        else:
            fail_count += 1
        
        # Be polite to AsianWiki servers
        time.sleep(1)
        
    print(f"\n✅ Test complete! Success: {success_count}, Failed: {fail_count}")
    print("If results look good, remove the [:5] slice to run all dramas!")

if __name__ == "__main__":
    main()