#!/bin/bash

echo "🎬 Updating K-drama list..."

# Step 1: Fetch latest data from Airtable
echo "📥 Fetching dramas from Airtable..."
python transform_data.py

# Step 2: Push to GitHub
echo "📤 Pushing to GitHub..."
git add dramas.json
git commit -m "Update dramas - $(date '+%Y-%m-%d')"
git push

echo "✅ Done! Website will update in ~2 minutes at https://rinva19.github.io/kdrama-tracker/"