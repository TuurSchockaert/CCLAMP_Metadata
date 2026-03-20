import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import os
import re
import time
import random

# Load the list of URLs and identifiers
df = pd.read_csv('author_identifier_list.txt', sep='\t')  # Adjust separator if needed

# Create a folder to save the JSON files
output_folder = "scraped_json"
os.makedirs(output_folder, exist_ok=True)

# List to collect failed scrapes
failed_scrapes = []


def sanitize_filename(name):
    """Clean the filename: remove illegal characters, replace spaces, and lowercase."""
    name = name.strip()
    name = re.sub(r'[\\/*?:"<>|]', "", name)  # Remove illegal characters
    name = name.replace(" ", "_")  # Replace spaces with underscores
    name = name.lower()
    return name


for idx, row in df.iterrows():
    author = row.get('Author')
    identifier = row.get('identifier')
    url = row.get('Link')

    if pd.isna(identifier) or pd.isna(url):
        continue  # Skip if either Identifier or Link is missing

    try:
        print(f"Scraping {idx + 1}/{len(df)}: {identifier} ({author}) - {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find('script', type='application/ld+json')

        if script_tag:
            json_data = script_tag.string.strip()
            parsed_json = json.loads(json_data)

            # Sanitize the identifier name for safe file naming
            safe_identifier = sanitize_filename(identifier)

            filename = os.path.join(output_folder, f"{safe_identifier}.json")
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(parsed_json, f, indent=2, ensure_ascii=False)
        else:
            print(f"No <script type='application/ld+json'> found for {url}")
            failed_scrapes.append(
                {'Author': author, 'identifier': identifier, 'Link': url, 'Reason': 'No JSON-LD found'})

    except Exception as e:
        print(f"Error scraping {url} for {author} ({identifier}): {e}")
        failed_scrapes.append({'Author': author, 'identifier': identifier, 'Link': url, 'Reason': str(e)})

    # Add a polite random sleep between 2 and 5 seconds
    wait_time = random.uniform(2, 5)
    print(f"Waiting {wait_time:.2f} seconds before next request...")
    time.sleep(wait_time)

# Save failed attempts to a CSV
if failed_scrapes:
    fail_log = pd.DataFrame(failed_scrapes)
    fail_log.to_csv('failed_scrapes.csv', index=False)
    print(f"Saved {len(failed_scrapes)} failed scrapes to failed_scrapes.csv")

print("Done scraping all URLs.")
