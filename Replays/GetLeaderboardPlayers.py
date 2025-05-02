import requests
from bs4 import BeautifulSoup
import time
import cloudscraper

BASE_URL = "https://rocketleague.tracker.network"
LEADERBOARD_URL_TEMPLATE = BASE_URL + "/rocket-league/leaderboards/playlist/steam/default?page={page}&playlist=11&country=de"

def get_profiles(page):
    
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
    profiles = []

    for a_tag in website.find_all("a", href=True):
        href = a_tag.get("href", "")

        if href.startswith("/rocket-league/profile/steam/"):
            steam_id = href.split("/")[-1]
            username = a_tag.text.strip()
            profiles.append((steam_id, username))
    
    return profiles

def scrape_all_pages():
    all_profiles = []
    for page in range(1, 11):
        print(f"Verabreite Seite {page}...")
        some_profiles = get_profiles(page)
        all_profiles.extend(some_profiles)
        time.sleep(1)

    return all_profiles

if __name__ == "__main__":
    all_profiles = scrape_all_pages()

    with open("Top_Players.txt", "w", encoding="utf-8") as f:
        for steam_id, username in all_profiles:
            f.write(f"{steam_id}, {username}\n")

    print(f"Gespeichert: {len(all_profiles)} Links in 'Top_Players.txt'")