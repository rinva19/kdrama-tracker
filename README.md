# K-Drama Tracker

Rebecca's personal K-drama watch history with sorting, filtering, search, and actor information.

**Live site:** https://rinva19.github.io/kdrama-tracker/

---

## Quick Start: Updating After Airtable Changes

When you add or edit dramas in Airtable, here's your workflow:

### 1. Add New Dramas to Airtable
Fill in your Korean Dramas table with:
- Title (required)
- Rating, Year Released, Actors, Actresses, Genre, etc.
- Leave Poster URL and Plot Summary blank initially

### 2. Fetch Missing Data
Run this to get posters and plot summaries for new dramas:
```bash
python fetch_posters_tmdb.py
```
This automatically:
- Finds dramas without posters or summaries
- Searches TMDb and adds them to Airtable
- Skips dramas that already have data (safe to run anytime)

### 3. Update Website
```bash
update-dramas
```
This single command:
- Pulls latest data from Airtable
- Regenerates `dramas.json`
- Commits and pushes to GitHub
- Website updates in ~2 minutes

**That's it!** Three steps total.

---

## Optional: Adding Actor Profile Images

If you want actor headshots in the actor modal:

```bash
python fetch_actor_images.py
```

This:
- Finds actors/actresses without profile images
- Searches TMDb for headshots
- Adds them to your Actors/Actresses tables
- Skips actors who already have images

Then run `update-dramas` to push changes.

---

## Features

### Display & Navigation
- Drama posters and plot summaries from TMDb
- Search box with autocomplete (searches titles, actors, genres)
- Dynamic counter showing filtered results
- Expandable cards - click any drama to see plot summary
- Gold gradient badges for group-watched dramas

### Sorting Options
- Title (A-Z or Z-A)
- Rating (High-Low or Low-High)  
- Year Released (Newest or Oldest)
- Date Finished (Recent or Oldest)

### Filtering Options
- All Dramas
- By star rating (5, 4, 3, 2, or 1 stars)
- Kdrama Group (group-watched dramas in watch order)

### Actor Features
- Click any actor/actress name to see:
  - Their profile photo (if available)
  - Total dramas watched
  - Average rating across their dramas
  - Complete list of their dramas you've seen

---

## File Structure

### Scripts You Run
- **`fetch_posters_tmdb.py`** - Gets poster URLs and plot summaries from TMDb
- **`fetch_actor_images.py`** - Gets actor/actress profile images from TMDb
- **`update.sh`** - Your automation script (aliased as `update-dramas`)
- **`transform_data.py`** - Pulls from Airtable and builds dramas.json

### Website Files
- **`index.html`** - Main page structure
- **`styles.css`** - All styling
- **`script.js`** - Search, sort, filter, and actor modal logic
- **`dramas.json`** - Generated data file (don't edit manually!)

### Configuration
- **`airtable_credentials.py`** - API keys (NEVER push to GitHub!)
  - Contains: `API_KEY` (Airtable) and `TMDB_API_KEY`
  - Base ID and table names are in the scripts themselves

---

## Airtable Structure

### Korean Dramas Table
Required fields:
- **Title** - Drama name
- **Rating** - 1-5 stars
- **Year Released** - Year as number
- **Genre** - Multi-select
- **Actors** - Linked records to Actors table
- **Actresses** - Linked records to Actresses table
- **Country of Origin** - Text
- **Date Finished** - Date field
- **Viewing Status** - Single select
- **Channel** - Multi-select
- **Kdrama Group** - Number (watch order for group dramas)
- **Poster URL** - Text (auto-filled by fetch_posters_tmdb.py)
- **Plot Summary** - Long text (auto-filled by fetch_posters_tmdb.py)

### Actors/Actresses Tables
- **Name** - Format: "First-name Last-name" (e.g., "Park Seo-Joon")
- **Profile Image URL** - Text (auto-filled by fetch_actor_images.py)

---

## Troubleshooting

### `update-dramas` command not found
The alias may not be set up. Navigate to your scripts folder and run directly:
```bash
cd ~/Documents/Household/Scripts
./update.sh
```

### Posters/summaries aren't fetching
1. Check that `TMDB_API_KEY` is valid in `airtable_credentials.py`
2. TMDb allows 1000 requests/day - you shouldn't hit this limit
3. Some dramas may not be in TMDb's database

### Actor images not appearing in modal
1. Run `fetch_actor_images.py` to get profile images
2. Run `update-dramas` to rebuild dramas.json with the new images
3. Clear browser cache (`Cmd + Shift + R`)

### Website not updating after push
GitHub Pages deployment takes 2-5 minutes. Check:
1. GitHub Actions tab to see if deployment is running
2. Clear browser cache if it's been longer than 5 minutes

### Actor names not showing up
Run `transform_data.py` to rebuild dramas.json with current actor lookups:
```bash
python transform_data.py
```

---

## Technical Details

- **Alias:** `update-dramas` runs `~/Documents/Household/Scripts/update.sh`
- **TMDb API:** Free tier allows 1000 requests/day
- **Data storage:** Poster URLs and summaries stored in Airtable (no live API calls needed on website)
- **Python requirements:** `pyairtable`, `requests`, `beautifulsoup4`
- **Actor data:** Profile images and names pulled from linked Actors/Actresses tables

---

## Future Ideas

- ✅ ~~Plot summaries~~ (DONE!)
- ✅ ~~Actor headshots~~ (DONE!)
- ✅ ~~Click actor names for info~~ (DONE!)
- ✅ ~~Search functionality~~ (DONE!)
- Streaming service availability
- Recommend similar dramas based on ratings
- Export watch history to CSV
