import psycopg2
import json
import os

DB_CONFIG = {
'dbname': 'RLReplays',
'user': 'postgres',
'password': 'postgres',
'host': 'localhost',
'port': 5432
}

REPLAY_DIR = './Replays/Replay Data/'
TABLE_NAME = 'replay_stats'

def create_table(cur):
    cur.execute(f"""
        DROP TABLE IF EXISTS {TABLE_NAME}
                """)
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        entry_id SERIAL PRIMARY KEY,
        player_name TEXT,
        match_type TEXT,
        team_size INTEGER,
        season INTEGER,
        date TIMESTAMP,

        duration INTEGER,
        overtime BOOLEAN,
        overtime_seconds REAL,
        start_time REAL,
        end_time REAL,

        mvp BOOLEAN,
        shots INTEGER,
        shots_against INTEGER,
        goals INTEGER,
        goals_against INTEGER,
        saves INTEGER,
        assists INTEGER,
        score INTEGER,
        shooting_percentage REAL,

        bpm INTEGER,
        bcpm REAL,
        avg_amount REAL,
        amount_collected INTEGER,
        amount_stolen INTEGER,
        amount_collected_big INTEGER,
        amount_stolen_big INTEGER,
        amount_collected_small INTEGER,
        amount_stolen_small INTEGER,
        count_collected_big INTEGER,
        count_stolen_big INTEGER,
        count_collected_small INTEGER,
        count_stolen_small INTEGER,
        amount_overfill INTEGER,
        amount_overfill_stolen INTEGER,
        amount_used_while_supersonic INTEGER,
        percent_zero_boost REAL,
        percent_full_boost REAL,
        percent_boost_0_25 REAL,
        percent_boost_25_50 REAL,
        percent_boost_50_75 REAL,
        percent_boost_75_100 REAL,

        avg_speed INTEGER,
        avg_speed_percentage REAL,
        total_distance BIGINT,
        percent_supersonic_speed REAL,
        percent_boost_speed REAL,
        percent_slow_speed REAL,
        percent_ground REAL,
        percent_low_air REAL,
        percent_high_air REAL,
        time_powerslide REAL,
        count_powerslide INTEGER,
        avg_powerslide_duration REAL,

        avg_distance_to_ball INTEGER,
        avg_distance_to_ball_possession INTEGER,
        avg_distance_to_ball_no_possession INTEGER,
        avg_distance_to_mates INTEGER,
        percent_defensive_third REAL,
        percent_offensive_third REAL,
        percent_neutral_third REAL,
        percent_defensive_half REAL,
        percent_offensive_half REAL,
        percent_behind_ball REAL,
        percent_infront_ball REAL,
        percent_most_back REAL,
        percent_most_forward REAL,
        percent_closest_to_ball REAL,
        percent_farthest_from_ball REAL,
        goals_against_while_last_defender INTEGER,

        demo_inflicted INTEGER,
        demo_taken INTEGER,

        rank_tier INTEGER,
        rank_division INTEGER
        );
        """)
    
def fill_Table(cur, data):
    match_type = data.get("match_type")
    team_size = data.get("team_size")
    season = data.get("season")
    date = data.get("date")

    duration = data.get("duration")
    overtime = data.get("overtime")
    overtime_seconds = data.get("overtime_seconds")

    for team in ["blue", "orange"]:
        for player in data.get(team, {}).get("players", []):
            player_name = player.get("name") or "None"
            start_time = player.get("start_time") or 0
            end_time = player.get("end_time") or 0

            mvp = player.get("mvp") or "false"
            shots = player.get("stats", {}).get("core", {}).get("shots") or 0
            shots_against = player.get("stats", {}).get("core", {}).get("shots_against") or 0
            goals = player.get("stats", {}).get("core", {}).get("goals") or 0
            goals_against = player.get("stats", {}).get("core", {}).get("goals_against") or 0
            saves = player.get("stats", {}).get("core", {}).get("saves") or 0
            assists = player.get("stats", {}).get("core", {}).get("assists") or 0
            score = player.get("stats", {}).get("core", {}).get("score") or 0
            shooting_percentage = player.get("stats", {}).get("core", {}).get("shooting_percentage") or 0

            bpm = player.get("stats", {}).get("boost", {}).get("bpm") or 0
            bcpm = player.get("stats", {}).get("boost", {}).get("bcpm") or 0
            avg_amount = player.get("stats", {}).get("boost", {}).get("avg_amount") or 0
            amount_collected = player.get("stats", {}).get("boost", {}).get("amount_collected") or 0
            amount_stolen = player.get("stats", {}).get("boost", {}).get("amount_stolen") or 0
            amount_collected_big = player.get("stats", {}).get("boost", {}).get("amount_collected_big") or 0
            amount_stolen_big = player.get("stats", {}).get("boost", {}).get("amount_stolen_big") or 0
            amount_collected_small = player.get("stats", {}).get("boost", {}).get("amount_collected_small") or 0
            amount_stolen_small = player.get("stats", {}).get("boost", {}).get("amount_stolen_small") or 0
            count_collected_big = player.get("stats", {}).get("boost", {}).get("count_collected_big") or 0
            count_stolen_big = player.get("stats", {}).get("boost", {}).get("count_stolen_big") or 0
            count_collected_small = player.get("stats", {}).get("boost", {}).get("count_collected_small") or 0
            count_stolen_small = player.get("stats", {}).get("boost", {}).get("count_stolen_small") or 0
            amount_overfill = player.get("stats", {}).get("boost", {}).get("amount_overfill") or 0
            amount_overfill_stolen = player.get("stats", {}).get("boost", {}).get("amount_overfill_stolen") or 0
            amount_used_while_supersonic = player.get("stats", {}).get("boost", {}).get("amount_used_while_supersonic") or 0
            percent_zero_boost = player.get("stats", {}).get("boost", {}).get("percent_zero_boost") or 0
            percent_full_boost = player.get("stats", {}).get("boost", {}).get("percent_full_boost") or 0
            percent_boost_0_25 = player.get("stats", {}).get("boost", {}).get("percent_boost_0_25") or 0
            percent_boost_25_50 = player.get("stats", {}).get("boost", {}).get("percent_boost_25_50") or 0
            percent_boost_50_75 = player.get("stats", {}).get("boost", {}).get("percent_boost_50_75") or 0
            percent_boost_75_100 = player.get("stats", {}).get("boost", {}).get("percent_boost_75_100") or 0

            avg_speed = player.get("stats", {}).get("movement", {}).get("avg_speed") or 0
            avg_speed_percentage = player.get("stats", {}).get("movement", {}).get("avg_speed_percentage") or 0
            total_distance = player.get("stats", {}).get("movement", {}).get("total_distance") or 0
            percent_supersonic_speed = player.get("stats", {}).get("movement", {}).get("percent_supersonic_speed") or 0
            percent_boost_speed = player.get("stats", {}).get("movement", {}).get("percent_boost_speed") or 0
            percent_slow_speed = player.get("stats", {}).get("movement", {}).get("percent_slow_speed") or 0
            percent_ground = player.get("stats", {}).get("movement", {}).get("percent_ground") or 0
            percent_low_air = player.get("stats", {}).get("movement", {}).get("percent_low_air") or 0
            percent_high_air = player.get("stats", {}).get("movement", {}).get("percent_high_air") or 0
            time_powerslide = player.get("stats", {}).get("movement", {}).get("time_powerslide") or 0
            count_powerslide = player.get("stats", {}).get("movement", {}).get("count_powerslide") or 0
            avg_powerslide_duration = player.get("stats", {}).get("movement", {}).get("avg_powerslide_duration") or 0

            avg_distance_to_ball = player.get("stats", {}).get("positioning", {}).get("avg_distance_to_ball") or 0
            avg_distance_to_ball_possession = player.get("stats", {}).get("positioning", {}).get("avg_distance_to_ball_possession") or 0
            avg_distance_to_ball_no_possession = player.get("stats", {}).get("positioning", {}).get("avg_distance_to_ball_no_possession") or 0
            avg_distance_to_mates = player.get("stats", {}).get("positioning", {}).get("avg_distance_to_mates") or 0
            percent_defensive_third = player.get("stats", {}).get("positioning", {}).get("percent_defensive_third") or 0
            percent_offensive_third = player.get("stats", {}).get("positioning", {}).get("percent_offensive_third") or 0
            percent_neutral_third = player.get("stats", {}).get("positioning", {}).get("percent_neutral_third") or 0
            percent_defensive_half = player.get("stats", {}).get("positioning", {}).get("percent_defensive_half") or 0
            percent_offensive_half = player.get("stats", {}).get("positioning", {}).get("percent_offensive_half") or 0
            percent_behind_ball = player.get("stats", {}).get("positioning", {}).get("percent_behind_ball") or 0
            percent_infront_ball = player.get("stats", {}).get("positioning", {}).get("percent_infront_ball") or 0
            percent_most_back = player.get("stats", {}).get("positioning", {}).get("percent_most_back") or 0
            percent_most_forward = player.get("stats", {}).get("positioning", {}).get("percent_most_forward") or 0
            percent_closest_to_ball = player.get("stats", {}).get("positioning", {}).get("percent_closest_to_ball") or 0
            percent_farthest_from_ball = player.get("stats", {}).get("positioning", {}).get("percent_farthest_from_ball") or 0
            goals_against_while_last_defender = player.get("stats", {}).get("positioning", {}).get("goals_against_while_last_defender") or 0

            demo_inflicted = player.get("stats", {}).get("demo", {}).get("inflicted") or 0
            demo_taken = player.get("stats", {}).get("demo", {}).get("taken") or 0

            rank_tier = player.get("rank", {}).get("tier") or 0
            rank_division = player.get("rank", {}).get("division") or 0

            try:
                cur.execute("""
                    INSERT INTO replay_stats 
                    (player_name, match_type, team_size, season, date, duration, overtime, overtime_seconds, start_time, end_time, mvp, shots, shots_against, goals, goals_against, saves, assists, score, shooting_percentage, bpm, bcpm, avg_amount, amount_collected, amount_stolen, amount_collected_big, amount_stolen_big, amount_collected_small, amount_stolen_small, count_collected_big, count_stolen_big, count_collected_small, count_stolen_small, amount_overfill, amount_overfill_stolen, amount_used_while_supersonic, percent_zero_boost, percent_full_boost, percent_boost_0_25, percent_boost_25_50, percent_boost_50_75, percent_boost_75_100, avg_speed, avg_speed_percentage, total_distance, percent_supersonic_speed, percent_boost_speed, percent_slow_speed, percent_ground, percent_low_air, percent_high_air, time_powerslide, count_powerslide, avg_powerslide_duration, avg_distance_to_ball, avg_distance_to_ball_possession, avg_distance_to_ball_no_possession, avg_distance_to_mates, percent_defensive_third, percent_offensive_third, percent_neutral_third, percent_defensive_half, percent_offensive_half, percent_behind_ball, percent_infront_ball, percent_most_back, percent_most_forward, percent_closest_to_ball, percent_farthest_from_ball, goals_against_while_last_defender, demo_inflicted, demo_taken, rank_tier, rank_division) 
                    VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, 
                    (player_name, match_type, team_size, season, date, duration, overtime, overtime_seconds, start_time, end_time, mvp, shots, shots_against, goals, goals_against, saves, assists, score, shooting_percentage, bpm, bcpm, avg_amount, amount_collected, amount_stolen, amount_collected_big, amount_stolen_big, amount_collected_small, amount_stolen_small, count_collected_big, count_stolen_big, count_collected_small, count_stolen_small, amount_overfill, amount_overfill_stolen, amount_used_while_supersonic, percent_zero_boost, percent_full_boost, percent_boost_0_25, percent_boost_25_50, percent_boost_50_75, percent_boost_75_100, avg_speed, avg_speed_percentage, total_distance, percent_supersonic_speed, percent_boost_speed, percent_slow_speed, percent_ground, percent_low_air, percent_high_air, time_powerslide, count_powerslide, avg_powerslide_duration, avg_distance_to_ball, avg_distance_to_ball_possession, avg_distance_to_ball_no_possession, avg_distance_to_mates, percent_defensive_third, percent_offensive_third, percent_neutral_third, percent_defensive_half, percent_offensive_half, percent_behind_ball, percent_infront_ball, percent_most_back, percent_most_forward, percent_closest_to_ball, percent_farthest_from_ball, goals_against_while_last_defender, demo_inflicted, demo_taken, rank_tier, rank_division
                ))

                print(f"I'm working on it, Player {player_name}")

            except Exception as e:
                print(f"Fehler beim Einfügen in replay_stats für Spieler {player_name}: {e}")
                conn.rollback()
            conn.commit()

def find_jsons(search_dir):
    for root, dirs, files in os.walk(search_dir):
        for file in files:
            if file.startswith('replay_data_'):
                yield os.path.join(root, file)

if __name__ == "__main__":
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    create_table(cur)
    conn.commit()

    for filepath in find_jsons(REPLAY_DIR):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                fill_Table(cur, data)
        except Exception as e:
            print(f"Fehler beim Verarbeiten von {filepath}: {e}")
    
    cur.close()
    conn.close()