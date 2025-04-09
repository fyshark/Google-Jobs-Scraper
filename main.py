from serpapi import GoogleSearch
import pandas as pd
import datetime
import json
import time
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("SERPAPI_KEY")

ROLE = "Softwareentwickler"
CITY = "Berlin, Germany"
FILTER_KEYWORDS = ["Softwareentwickler", "Software Engineer", "Entwickler", "Developer"]

def parse_posted_at(text):
    if not text:
        return None

    text = text.lower().strip()
    now = datetime.datetime.now()

    # "just posted", "eben", "gerade", "few seconds ago"
    if any(x in text for x in ["just", "gerade", "eben", "few seconds", "wenigen sekunden"]):
        return now

    # Remove "ago" or "vor"
    text = text.replace("ago", "").replace("vor", "").strip()
    parts = text.split()

    if len(parts) < 2:
        return None

    try:
        value = int(parts[0])
    except ValueError:
        return None

    unit = parts[1]

    # English
    if "minute" in unit:
        return now - datetime.timedelta(minutes=value)
    elif "hour" in unit:
        return now - datetime.timedelta(hours=value)
    elif "day" in unit:
        return now - datetime.timedelta(days=value)
    elif "week" in unit:
        return now - datetime.timedelta(weeks=value)
    elif "month" in unit:
        return now - datetime.timedelta(days=value * 30)

    # German
    elif "minute" in unit:
        return now - datetime.timedelta(minutes=value)
    elif "stunde" in unit:
        return now - datetime.timedelta(hours=value)
    elif "tag" in unit:
        return now - datetime.timedelta(days=value)
    elif "woche" in unit:
        return now - datetime.timedelta(weeks=value)
    elif "monat" in unit:
        return now - datetime.timedelta(days=value * 30)

    return None

print(f"🔍 Searching for '{ROLE}' in {CITY}...")

params = {
    "engine": "google_jobs",
    "q": ROLE,
    "location": CITY,
    "hl": "de",
    "api_key": API_KEY
}

search = GoogleSearch(params)
results = search.get_dict()


jobs = results.get("jobs_results", [])

filtered_jobs = []
params = {
    "engine": "google_jobs",
    "q": ROLE,
    "location": CITY,
    "hl": "de",
    "api_key": API_KEY
}

page_count = 0
MAX_PAGES = 5

while page_count < MAX_PAGES:
    print(f"\n🔍 The {page_count + 1} page job post scraping...")
    search = GoogleSearch(params)
    results = search.get_dict()

    if "error" in results:
        print("❗ Error message:", results["error"])
        break

    jobs = results.get("jobs_results", [])
    print(f"➡️ Got {len(jobs)} job posts.")

    for job in jobs:
        title = job.get("title", "")
        if any(keyword.lower() in title.lower() for keyword in FILTER_KEYWORDS):
            filtered_jobs.append({
                "title": title,
                "company": job.get("company_name"),
                "location": job.get("location"),
                "publish_time": parse_posted_at(job.get("detected_extensions", {}).get("posted_at")),
                "link": job.get("apply_options", [{}])[0].get("link", job.get("share_link", ""))
            })

    # check if it has next page or not
    next_token = results.get("serpapi_pagination", {}).get("next_page_token")
    if not next_token:
        print("🚫 No more pages.")
        break

    # update the next page parameter
    params["next_page_token"] = next_token
    page_count += 1

    time.sleep(1.5)


df = pd.DataFrame(filtered_jobs)

if df.empty:
    print("⚠️ No matching jobs found.")
else:
    df = df.sort_values(by="publish_time", ascending=False, na_position="last")
    df = df.head(30)  # only keep top 20
    df.to_csv("berlin_jobs_top30.csv", index=False, encoding="utf-8-sig")
    print(f"✅ Saved top {len(df)} jobs to berlin_jobs_top30.csv")

with open("berlin_jobs_raw_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("✅ Saved the json search result to the file berlin_jobs_raw_results.json")