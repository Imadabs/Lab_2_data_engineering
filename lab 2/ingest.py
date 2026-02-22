"""
Lab 2 - Data Ingestion Script
Scrapes Google Play Store apps and reviews and saves them as JSONL files.
"""
import json
import time
import sys
from google_play_scraper import app, reviews, search, Sort

OUTPUT_DIR = r"c:\Users\bellm\Desktop\lab 2\playstore_pipeline\data\raw"

# Define a selection of popular app IDs to scrape
APP_IDS = [
    "com.whatsapp",
    "com.instagram.android",
    "com.facebook.katana",
    "com.spotify.music",
    "com.netflix.mediaclient",
    "com.google.android.youtube",
    "com.twitter.android",
    "com.snapchat.android",
    "com.tiktok.android",
    "com.amazon.mShop.android.shopping",
    "com.google.android.gm",
    "com.microsoft.teams",
    "com.zoom.videomeetings",
    "com.duolingo",
    "com.ubercab",
    "com.airbnb.android",
    "com.paypal.android.p2pmobile",
    "com.linkedin.android",
    "com.reddit.frontpage",
    "com.discord",
]

def scrape_apps(app_ids):
    """Scrape app metadata."""
    apps_data = []
    total_apps = len(app_ids)
    for i, app_id in enumerate(app_ids, 1):
        try:
            result = app(app_id, lang='en', country='us')
            apps_data.append(result)
            print(f"[{i}/{total_apps}] [OK] Scraped app: {app_id}")
            time.sleep(0.5)
        except Exception as e:
            print(f"[{i}/{total_apps}] [SKIP] {app_id}: {e}")
    return apps_data

def scrape_reviews(app_ids, count_per_app=5000):
    """Scrape reviews for each app."""
    all_reviews = []
    from datetime import datetime, timedelta
    cutoff_date = datetime.now() - timedelta(days=100)
    total_apps = len(app_ids)

    for i, app_id in enumerate(app_ids, 1):
        print(f"[{i}/{total_apps}] Scraping reviews for {app_id}...")
        try:
            valid_reviews_count = 0
            continuation_token = None
            
            # Fetch in batches to show progress
            while valid_reviews_count < count_per_app:
                batch_size = min(200, count_per_app - valid_reviews_count)
                
                result, continuation_token = reviews(
                    app_id,
                    lang='en',
                    country='us',
                    sort=Sort.NEWEST,
                    count=batch_size,
                    continuation_token=continuation_token
                )
                
                if not result:
                    break
                
                reached_cutoff = False
                for r in result:
                    review_date = r.get('at') 
                    if review_date:
                        if review_date >= cutoff_date:
                            r['appId'] = app_id
                            all_reviews.append(r)
                            valid_reviews_count += 1
                        else:
                            # Reached a review older than 100 days, we can stop for this app
                            reached_cutoff = True
                            
                # Print progress on the same line
                print(f"   -> Fetched {valid_reviews_count} recent reviews so far...", end='\\r')
                sys.stdout.flush()
                
                if reached_cutoff or not continuation_token:
                    break
                    
            print(f"\\n   [OK] Finished {app_id}: {valid_reviews_count} reviews (last 100 days)")
            time.sleep(0.5)
        except Exception as e:
            print(f"\\n   [SKIP] {app_id}: {e}")
    return all_reviews

def write_jsonl(data, filepath):
    """Write list of dicts to JSONL file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        for record in data:
            f.write(json.dumps(record, default=str) + '\n')
    print(f"[SAVED] {len(data)} records -> {filepath}")

if __name__ == "__main__":
    import os
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("=== Scraping Apps ===")
    apps_data = scrape_apps(APP_IDS)
    write_jsonl(apps_data, os.path.join(OUTPUT_DIR, "apps.jsonl"))

    print("\n=== Scraping Reviews ===")
    # Set to a very large number to get "all" reachable reviews
    reviews_data = scrape_reviews(APP_IDS, count_per_app=5000)
    write_jsonl(reviews_data, os.path.join(OUTPUT_DIR, "reviews.jsonl"))

    print(f"\nDone! {len(apps_data)} apps, {len(reviews_data)} reviews.")
