# kdrama-tracker
K-drama group watch list

# K-Drama Tracker

Public website: https://rinva19.github.io/kdrama-tracker/

## How to Update the Website

When you add new dramas to Airtable:

1. Open Terminal (anywhere on your Mac)
2. Type: `update-dramas`
3. Press Enter
4. Wait ~2 minutes for the website to refresh

That's it!

## Files
- `airtable_credentials.py` - Your secret API token (never push to GitHub!)
- `transform_data.py` - Fetches dramas from Airtable
- `dramas.json` - The data that powers the website
- `index.html`, `styles.css`, `script.js` - The website files
- `update.sh` - Automation script

## Troubleshooting
If `update-dramas` doesn't work, navigate to this folder and run:
```
./update.sh
```
