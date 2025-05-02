import requests
import json
import config
import os
import time

HEADERS = {"Authorization": config.API_KEY}
API_Url = config.API_Url

def start():
    cycle = 0
    with open("Top_Players.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            steam_id = line.split(",")[0]
            username = line.split(",")[1].strip()

            cycle += 1

            get_replays(steam_id, username)
            extract_replay_ids(steam_id, username)
            get_replay_data(steam_id, username, cycle)

            # One cycle consists of 50 replays, so after 5000 replays API cooldown for 1 hour triggers
            if(cycle % 100 == 0):
                print("Cooldown for about 40 minutes...")
                time.sleep(2350)


def get_replays(steam_id, username):
    print(f"Processing Player: {username}")
    player_url = API_Url.format(steam_id)

    try:
        response = requests.get(player_url, headers=HEADERS)
        data = response.json()
        os.makedirs(f"./Replays/Replay Data/{steam_id}_{username}", exist_ok=True)

        filename = f"./Replays/Replay Data/{steam_id}_{username}/replays_{steam_id}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

        print(f"Replay data saved in: {filename}")

    except Exception as e:
        print(f"Unexpected error while retrieving player data for {username}: {e}")


def extract_replay_ids(steam_id, username):
    replay_ids = []
    
    with open(f"./Replays/Replay Data/{steam_id}_{username}/replays_{steam_id}.json", 'r', encoding='utf-8') as replays:
        data = json.load(replays)
        
        for replay in data["list"]:
            replay_id = replay["link"].split("/")[-1]
            if(not replay_ids.__contains__(replay_id)):
                replay_ids.append(replay_id)

    with open(f"./Replays/Replay Data/{steam_id}_{username}/replay_ids_{steam_id}.json", 'w', encoding='utf-8') as f:
        json.dump(replay_ids, f, indent=4)


def get_replay_data(steam_id, username, cycle):
    print(f"Data for player: {username}")
    
    with open(f"./Replays/Replay Data/{steam_id}_{username}/replay_ids_{steam_id}.json", 'r', encoding='utf-8') as replays:
        replay_ids = json.load(replays)
    
    Cooldown_Counter = 0
    for replay_id in replay_ids:
        replay_url = f"https://ballchasing.com/api/replays/{replay_id}"
        Cooldown_Counter += 1

        # Every 4 replays a Cooldown of 1 second is triggered
        # After 5000 replays a Cooldown of 40 minutes is triggered (see start())
        if Cooldown_Counter % 4 == 0:
            print("Cooldown for 1 second...")
            time.sleep(1)
        try:
            response = requests.get(replay_url, headers=HEADERS)
            data = response.json()
            
            filename = f"./Replays/Replay Data/{steam_id}_{username}/replay_data_{steam_id}_{Cooldown_Counter}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)

            print(f"Replay data saved in: {filename}")

        except Exception as e:
            print(f"Unexpected error while retrieving replay data for {username}: {e}")
