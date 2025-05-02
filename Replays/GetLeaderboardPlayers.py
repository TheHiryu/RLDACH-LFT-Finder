import requests
from bs4 import BeautifulSoup
import time
import cloudscraper

BASE_URL = "https://rocketleague.tracker.network"
LEADERBOARD_URL_TEMPLATE = BASE_URL + "/rocket-league/leaderboards/playlist/steam/default?page={page}&playlist=11&country=de"

def get_profile_ids(page):
    
    url = LEADERBOARD_URL_TEMPLATE.format(page=page)    
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    scraper = cloudscraper.create_scraper()
    response = scraper.get(url, headers=HEADERS)

    if not response.ok:
        print(f"Fehler beim Abrufen der Seite {response.status_code}")
        return []

    website = BeautifulSoup(response.text, 'html.parser')
    profile_ids = []

    for a_tag in website.find_all("a", href=True):
        href = a_tag["href"]
        if href.startswith("/rocket-league/profile/steam/"):
            steam_id = href.split("/")[-1]
            profile_ids.append(steam_id)
    
    return profile_ids

def scrape_all_pages():
    all_profiles = []
    for page in range(1, 11):
        print(f"Verabreite Seite {page}...")
        steam_ids = get_profile_ids(page)
        all_profiles.extend(steam_ids)
        time.sleep(1)

    return all_profiles

if __name__ == "__main__":
    steam_ids = scrape_all_pages()

    with open("Top_1000_Players.txt", "w", encoding="utf-8") as f:
        for steam_id in steam_ids:
            f.write(steam_id + "\n")

    print(f"Gespeichert: {len(steam_ids)} Links in 'Top_1000_Players.txt'")