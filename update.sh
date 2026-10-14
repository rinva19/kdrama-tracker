#!/bin/bash

# Always run from the folder this script lives in
cd "$(dirname "$0")" || { echo "❌ Couldn't find the Scripts folder."; exit 1; }

echo "🎬 Updating K-drama list..."

# Step 1: Fetch latest data from Airtable
echo "📥 Fetching dramas from Airtable..."
if ! python transform_data.py; then
  echo "❌ Couldn't get data from Airtable. Nothing was pushed."
  exit 1
fi

# Step 2: Save the new data
git add dramas.json || { echo "❌ Git isn't working. Nothing was pushed."; exit 1; }

if git diff --cached --quiet; then
  echo "ℹ️  No changes to push. The website is already up to date."
  exit 0
fi

if ! git commit -m "Update dramas - $(date '+%Y-%m-%d')"; then
  echo "❌ Couldn't save the changes. Nothing was pushed."
  exit 1
fi

# Step 3: Send to GitHub
echo "📤 Pushing to GitHub..."
if ! git push; then
  echo "❌ Push to GitHub failed. The website did NOT update."
  echo "   Try: git pull origin main, then run update-dramas again."
  exit 1
fi

echo "✅ Done! Website will update in ~2 minutes at https://rinva19.github.io/kdrama-tracker/"
