import requests
import json
import config
import os
import time

HEADERS = {"Authorization": config.API_KEY}
API_Url = config.API_Url
steam_ids = [
    "76561198087548781",
]


def get_replays(steam_id):
    print(f"Verarbeite Spieler: {steam_id}")
    player_url = API_Url.format(steam_id)

    try:
        response = requests.get(player_url, headers=HEADERS)
        data = response.json()
        os.makedirs(f"./Replays/Replay Data/{steam_id}", exist_ok=True)

        filename = f"./Replays/Replay Data/{steam_id}/replays_{steam_id}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

        print(f"Replay-Daten gespeichert in: {filename}")

    except Exception as e:
        print(f"Anderer Fehler bei Spieler {steam_id}: {e}")


def extract_replay_ids(steam_id):
    replay_ids = []
    
    with open(f"./Replays/Replay Data/{steam_id}/replays_{steam_id}.json", 'r', encoding='utf-8') as replays:
        data = json.load(replays)
        
        for replay in data["list"]:
            replay_id = replay["link"].split("/")[-1]
            replay_ids.append(replay_id)

    with open(f"./Replays/Replay Data/{steam_id}/replay_ids_{steam_id}.json", 'w', encoding='utf-8') as f:
        json.dump(replay_ids, f, indent=4)


def get_replay_data(steam_id):
    print(f"Daten für Spieler: {steam_id}")
    
    with open(f"./Replays/Replay Data/{steam_id}/replay_ids_{steam_id}.json", 'r', encoding='utf-8') as replays:
        replay_ids = json.load(replays)
    
    Cooldown_Counter = 0
    for replay_id in replay_ids:
        replay_url = f"https://ballchasing.com/api/replays/{replay_id}"
        Cooldown_Counter += 1
        if Cooldown_Counter % 8 == 0:
            print("Cooldown von 1 Sekunde...")
            time.sleep(1)

        try:
            response = requests.get(replay_url, headers=HEADERS)
            data = response.json()
            
            filename = f"./Replays/Replay Data/{steam_id}/replay_data_{steam_id}_{Cooldown_Counter}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)

            print(f"Replay-Daten gespeichert in: {filename}")

        except Exception as e:
            print(f"Anderer Fehler bei Spielerdaten {steam_id}: {e}")




for steam_id in steam_ids:
    get_replays(steam_id)
    extract_replay_ids(steam_id)
    get_replay_data(steam_id)
