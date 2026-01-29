# K-Drama Tracker

Rebecca's personal K-drama watch history tracker with sorting, filtering, and automatic poster fetching from TMDb.

**Public website:** https://rinva19.github.io/kdrama-tracker/

---

## Quick Update Guide

### Adding New Dramas

When you add new dramas to Airtable:

1. **Add drama info to Airtable** (Title, Rating, Year, Actors, etc.)
2. **Fetch posters from TMDb:**
```bash
   python fetch_posters_tmdb.py
```
   - Automatically finds dramas without posters
   - Searches TMDb and adds poster URLs to Airtable
   - Skips dramas that already have posters (safe to run anytime)

3. **Update the website:**
```bash
   update-dramas
```
   - Pulls latest data from Airtable
   - Regenerates the website
   - Pushes to GitHub
   - Website updates in ~2 minutes

---

## Features

- **Drama posters** automatically fetched from TMDb
- **Dynamic counter** showing number of dramas displayed
- **Sorting options:**
  - Title (A-Z or Z-A)
  - Rating (High-Low or Low-High)
  - Year Released (Newest or Oldest)
  - Date Finished (Recent or Oldest)
- **Filter options:**
  - All Dramas
  - 5 Stars
  - 4 Stars
  - 3 Stars
  - 1 & 2 Stars
  - Kdrama Group (dramas watched with viewing group, sorted by watch order)
- **Actor/Actress names** from your curated Airtable lists
- **TMDb attribution** (required for using their poster images)

---

## Files Overview

### Main Scripts
- `transform_data.py` - Fetches drama data from Airtable and converts actor IDs to names
- `fetch_posters_tmdb.py` - Fetches poster URLs from TMDb API
- `update.sh` - Automation script that runs transform_data.py and pushes to GitHub

### Website Files
- `index.html` - Main website structure
- `styles.css` - Styling and layout
- `script.js` - Sorting, filtering, and display logic
- `dramas.json` - Generated data file that powers the website

### Configuration
- `airtable_credentials.py` - API keys for Airtable and TMDb (never push to GitHub!)
  - Contains: `API_KEY` (Airtable) and `TMDB_API_KEY`
  - Base ID and Table names are hardcoded in scripts

---

## Airtable Structure

### Required Fields in "Korean Dramas" table:
- Title
- Rating (1-5)
- Year Released
- Country of Origin
- Genre (multi-select)
- Actors (linked records to Actors table)
- Actresses (linked records to Actresses table)
- Poster URL (populated by fetch_posters_tmdb.py)
- Date Finished
- Kdrama Mamas (number field - watch order for group dramas)
- Channel
- Viewing Status

### Actor/Actress Tables:
- Name field with format: "First-name Last-name" (e.g., "Park Seo Joon")

---

## Troubleshooting

### update-dramas doesn't work
Navigate to the Scripts folder and run manually:
```bash
cd ~/Documents/Household/Scripts
./update.sh
```

### Posters aren't fetching
Check that your TMDb API key is valid in `airtable_credentials.py`

### Actor names not showing
Run transform_data.py to regenerate dramas.json with updated actor lookups:
```bash
python transform_data.py
```

### Website not updating after push
GitHub Pages can take 2-5 minutes to deploy. Clear browser cache with `Cmd + Shift + R`

---

## Setup Notes

- Alias `update-dramas` is configured in shell profile to run update.sh from any directory
- TMDb API allows 1000 requests/day (more than enough for this use case)
- Poster URLs are stored in Airtable, so website doesn't require live TMDb access
- All scripts use Python 3 and require: `pyairtable`, `requests`, `beautifulsoup4`

---

## Future Enhancement Ideas

- Add plot summaries from TMDb
- Add actor headshot photos
- Click actor names for more info
- Search functionality
- More filter combinations
