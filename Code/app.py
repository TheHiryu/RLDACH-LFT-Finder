

import os
from flask import Flask, render_template, request, redirect, jsonify
import asyncio
from discord import Webhook # Falls noch für andere Funktionen benötigt
import aiohttp
import random
import json

app = Flask(__name__)

# DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE" # Behalten, falls benötigt
# received_message = None # Behalten, falls benötigt

# --- Beispiel-Spielerliste (bleibt für /api/player_suggestions) ---
player_names_list_from_backend = ["DrunKingan", "rYu'89er", "sEr!aL", "DonF1re", "wiz", "x13-no-chat", "Ruvio", "nfb", "Wahlsor", "SwkT", "Yeti", "GustaV", "Noiizy", "KFCtheG", "SoundLucky", "R3voG4ming", "wry", "Link", "HERRBEYSEN", "Gnagflow06", "BoatyMcBoatface", "kkeno", "Lucifer", "no", "Tanome", "xvacmx", "Zenih", "NoToxic4u", "littleOogwayy", "Maufius95", "kkatyonak", "Ic3m4n", "pyhru", "Sonus", "Razzy", "MDK", "ShowCast", "seb", "KawaiiNico()", "LzrShak", "wilsbergg", "S", "jurl", "MiG91110", "LostJ3ster", "Ex0tical", "Flamezz", "Sqezz", "jjZZi", "Rockmysox", "riino", "Veit", "s!cK)", "Arceus", "womzyy", "yutu-", "Fabi", "ArdaGler", "M", "Gaetano", "dd", "Vano", "Saubr", "Wrixk", "RnZ", "Zeptic", "Toad", "BRUH", "solorll", "Skartes", "affenbande", "celly", "Oni", "KranKeSchranKe!", "Schlafi", "Anear", "Kontra", "runni", "Saut", "ongodpxnlchrrrr", "Peta", "m4a1dh", "Unc", "Goldennugg3t", "Dwoopy", "MaZ", "Juicy", "DarkHawkMHRNr10", "Happy", "VensoMcQueen", "z", "BobTschigarillo", "Oschi", "Jxuuls(PermaBanned)", "Z", "P4inUwU", "Hiryu", "Unlucky", "Coby", "Teo", "Ginjo", "vel", "KVN", "Phillegal", "beGenius", "collin", "dwizzytwizzycwipzy", "Cedric", "Harlem", "Ravish", "RELYXseysores", "Robba", "TaQuiX", "Nucklan", "Vito", "MrSunshine", "Darksmon", "XW", "dp7th", "NyxxOCE", "Hansen", "black5ky", "ATLAS", "YYRob", "INVTS7", "Flonobo", "K", "muyrico", "Griffin", "Eibur", "Hartmann", "Samy", "c", "Pxxloo", "HaZe", "St0rmi", "dot", "GLF", "Bobrittobandito", "Fiftzzeh", "shanks", "JackDjTom", "kyu", "CryptoRL", "Wizurd", "MrGrony", "Mino", "Lxuiis", "Denloe", "Omit313(chatoff)", "sirvile", "Revannx", "Catalysm", "Lyyvx", "stelu", "dmnc(NewtoSquare-Deadzone)", "Change", "Schiggy)", "MrPatchino", "Sanjee", "Yoloboy-", "Mino", "MH", "Sheepz#Washed", "Matrixx", "Anna-Lena3", "zebu", "Abstract", "anti", "Jss", "Zoroo", "yoka", "Zeddo", "Nox", "nick", "requ", "Awx", "nkls", "(-)", "Aquaknarre", "TheodoreJasperDetweiler", "Dave", "SpinatEsser", "BastianR", "JustaShadow", "rombuskap", "kryptoN", "Ventus", "Leytrix", "Moriitz", "Bzkill", "Mozz", "Yukisekki", "dk", "CMass", "dNa", "TrickShot-", "Reazyy", "Nico", "TKBOY", "Migne", "tobiray", "Putrik", "Clyro", "Marcel", "ady", "JXDN", "fortnitegamer", "Phix", "Shinoa", "Sucuki", "PadS", "orochi--", "BOB", "LK", "Kuko", "scream33", "cel", "DonKing95", "Stupzy", "GBATheGrinder", "ttvLeeOuh", "Tronix", "iwouldnever", "xelty", "jey", "Mitrooo", "judie", "Skifty-", "Fabi", "Swenzy", "MD", "Time2Lazer", "Nico", "ExjuiceMe", "frozen", "MiKa", "Rizex", "Bryan", "Repi66", "Cheeky", "Kampi", "Staraptoah", "HENTHE", "getSnek'd", "Mizu", "bob", "Sama3", "Gemmel7", "marv", "GabeOwners", "Nils", "tls", "crasery", "lumyna", "nex", "FE!N", "Mayzah", "Tomey", "apex", "PJ", "Finex", "Anteez", "Buster", "Desire", "Myrtle", "Tobi", "Deniz", "OGGZeroTwo", "becareful!", "Youngstar", "Tx0", "eij", "Elacior", "Superzwerg", "Rain", "Kalemon", "Jesus", "Rappiii", "lo", "PeppaPinch", "TimKoschi", "FATE", "Lievito", "Fussel28", "hasenkeule(-)", "Lance", "maaybie", "Maliken", "Maze", "Reazzy", "albo", "Cantus", "sarity", "Barou", "A1re4x", "Percy17", "timur4kzxc", "stivi", "lexi", "opertix", "aqua", "Gerry", "slashy", "BurnyPee", "SquishyMunching", "Flywalker", "c0by", "ankle", "sascha", "RealMalbu", "saiiko99", "Vempa", "Sn0wPanda", "Stmpy", "MkNsfsfsfsfsf", "solid", "Risk0", "SunZ", "THK", "zyde", "KabseR", "Dom", "lemi", "NLRgruhnd", "tryath", "Maikoz", "Imgn", "paulSZN", "lennerd", "Rias3", "Sharkyy", "5kimi", "MashafromO'Block", "Jannik", "blue", "Skyrunner170", "Seeeebi", "Coco", "TeeHeeUwUUwO", "MSR", "Plat", "u", "Schmocky23", "Golo", "schnappi", "Trinity", "rpsn", "RGE", "PureHate", "PhysixRL", "TarGeT", "L1K3R", "jck", "DustyDunker", "Rampage", "VolleRoffl", "Alexmeister", "Luii", "Sky3", "nygama", "time", "xBarracuda", "Gitto", "Vince", "Leschi", "Snowyyy", "Snoopy", "Ersatzspieler", "Lvtona", "ttvhelmoods", "Rian", "Fabso", "energizer", "xImmerDruff69", "FirePhoeniXx", "BanditSkyfall", "MikeB0i", "Tommy", "Carlos)", "Vinex", "Valid", "Loading", "BombardinoCrocodilo", "Shrimpwithahorn", "mafiahuhn", "Croby", "txmmy", "M-9TempesT", "Bahamas", "JulzZ", "Anju", "Kygo", "Maeve", "Bxrchii", "luap", "Eylow", "mrx", "kayuun", "NI", "ItsLeMax", "Kovi", "davee", "Jorden", "Trumps", "Bagua", "Jazii", "Daeky", "Rybu", "zane", "Trannel", "C-ptn(", "Charlez", "Dele", "philip", "gray", "t7mi", "Kyuu", "lepaniel", "tehe", "Timbo", "JackTheSec", "CheeseLover", "Kunotori", "antboy", "Jesus", "Genis", "jirka", "Hyrole", "dp", "FLYING", "E", "allthedogsarechasing", "SpiderDxD", "Gabriel", "mgi", "Fears", "Tetraflix", "Jzy", "Zavo", "octrax", "Rey", "gryhnd", "Tigreee", "SailorMiku3", "eurorunix", "Sarak", "jannesabi", "Kobrick", "Enter", "Kerze", "gettingrobbed", "Ripox", "raqzy", "TheBMKP", "vZ", "Brain", "spreatex", "Bobbl", "Nyco", "rintintin", "Brennholz3000", "zImpeL", "nibbolaus", "Brasnika", "quiply", "Rigl", "Crmson", "Thiess", "!sk", "Beez", "heinzzketchup", "Frozy", "OIIAI", "hax", "viu", "waftlaft-", "Alyiuu", "Gilibi", "Flo!", "nukezz!", "JayBeaR", "YARY", "NinjaminionZ", "ribsteak", "xandar", "Temp", "Vension", "992", "qatixx", "Kaizen", "seb", "phil", "ForGet", "Jere", "Waddy", "XVII", "WaveZ", "Bryze", "meez", "Phoenix", "iTxE7", "luggas", "Headshotski", "ifuhsaif", "AsusPrimeB450M", "T!KTOKHLGHLIVE", "Rndy", "Bamberek", "anga", "Nikoo", "Mounteverrizz", "Fujii", "ZedeX", "Drecksgame", "advanceobserve", "SleeeeepyFlow", "balou", "Freex!", "1", "Lairon)", "Caniwnl!", "v0qe3", "mreritz", "Exinho", "b3nnyyy", "aspen", "H4nn3s", "Q", "Pindroy", "Rayy", "Flex", "Waldi", "Craca", "Eryyc", "Trizzletan", "muzan", "SlayerBerlin", "DrNuts", "Kurdischsensei", "polar", "sqtnx", "ObiWag-Wan", "tvylics", "nick", "Clutshy", "Noah", "Monkeyman", "Letzoff", "zMkr", "Ingo", "Albrun", "Shino", "nex", "Henne", "avoid", "rysh", "Any", "Maggo", "bruh", "sakufadicheru", "Relox", "huz(smurf)", "Fynn", "T7lm", "PASCAL", "-", "noah", "Dok", "zRaynii", "rivez", "JustDean", "maegiic", "goldiesaidtrap", "Prod0x", "DyseUp", "jonjas", "Jamie", "poow", "bst", "Kryptos", "STEAR", "JustNoel", "Kingkazay", "reasn", "heppydoge", "LimitRL", "A1MBL1ND", "SARPBCKillajay-16", "Shawarma", "tobidobrzerobi", "Dark-Hero9864", "Jaynut", "LeftKick", "marv", "GunLeanmanGunLean", "Frawin", "Norttew", "Shiku", "ttvSlaySRL", "ImPmzZ", "llamar", "iplaylikeyou", "seb", "KESHI", "img", "Facer", "tate3", "staa", "Aarivex", "RDA!", "lou", "TravelSky", "Stingray", "anxiety", "everjan66", "Timinski", "ikee279", "Marcvader", "menqu", "naap848", "Rio", "Imagine", "yukain", "FishyK2", "Kiremi", "Br0dah", "Abc", "free", "Dark", "(-L-)", "faab", "dp", "chrs", "storm", "BROKENTHUMBGRR", "Tavix", "TriggerHappy", "Luraxbtw", "clxmens", "n4ykzz", "Cloudy", "azumi", "SoFon!", "tr1", "aspect", "Final", "hmky", "Aloey", "tucotucitosalamanca", "KYN", "quyoo", "Virus", "Wingz", "456", "Ruby-Chan", "Juzo", "verixz", "Isay", "LionZz", "Jasmin", "deshr", "topfit", "ttvStrikerFlow", "Wavy()", "kyza404", "Husky", "tim", "Scotty", "MrSquiddy", "X", "hiimsizl", "OmaNascher69", "Delta", "Kiqo", "Husk", "track", "Scopes", "Nexus", "tyler", "iMischunja", "predii", "Buckster", "Plexus", "Nytro", "kilixn", "rax", "x2", "JBerg", "L", "Toabdjzl", "mavonyx", "VanDerSar", "Fumtastic", "Nioo", "lele", "Ryu", "eric", "cookie", "NiuKomma", "Luca", "Syko", "Menvos", "DraXie", "Snupi", "Sranangtongo", "seltt", "plastikmuell", "DARKZONE", "ju", "TwitchxqRs7", "Rease", "TRA", "uxt", "Gyree", "Gedeon", "Fabe", "Lq", "Horizon", "knox", "MonKey66", "antzn", "sheiswifeymaterial", "Victarion", "Luca", "Emely", "justchillin420", "Jxshii", "shila", "hhenrck", "Gimme", "prownzyyy", "gohaN", "tabiospb", ")", "Sean", "dave", "Tyra", "yummy", "Pikatra", "KonsiKa", "LilRudi", "Vempa", "Yoeky", "dayyshift", "Cryptiic", "ihy", "vcx", "Femboycracker83", "Poly", "Sua", "zennin", "Luhkey", "PlayMestre", "Jonnaayri", "Sensei", "XMK", "Fared", "Monjuk", "Lj", "morebitcoinmoreproblems", "Veyn", "zym", "toomd", "r", "Fuwamoco", "Phliip", "Obigoon", "mesh", "Vylipp", "Timonster", "ph3x", "Eus", "Flexxy", "Jayku", "Heshy", "tizi(chatoff)", "Luiis", "0", "Phyn", "mauricem0", "Rosenrot", "KAR0TTENP0WERFan#1", "PlayboiRyze", "77", "Ley(RandomizedCarsonly)", "ninho!!", "Jinx", "Avicii", "Pfandi", "YuiX", "Brainiac", "Duon", "NicX", "AqouZ", "Syrzzs", "Arashi", "Lyrics", "Sparky", "mikerino!", "kimbo", "lazy)", "Mimicry96", "Eswirdehrenlos", "Waze", "Pumsy", "F", "TheHamburgerwithCheese", "foujeck3", "Whalexity", "Wat3r", "Justin", "Marv", "sCito9", "Josef", "vibindogee", "neo", "-Kaz-", "zhypix", "Oldman!", "xela", "Quexxy", "Pls05", "ntra", "ReRe", "bretski", "hopeless", "Menzuu", "Beyazz", "kcaj", "adgoez", "Rezears", "Keks", "jinx", "kaan", "Revxnge", "Cranddy", "Dark-Sider88", "Lyserg", "Kvn", "Akiba", "nlz", "Saint", "BXRKRL", "Saiint", "Emalyx", "lyrix", "flow", "zane", "Sil", "ARk3YAN", "DerManager", "a7ex", "Jos", "taycan", "m", "Monski", "Soda", "Yumekoo", "Splashy", "Aqueh", "SPQR", "Feetlover34", "Conschu", "Jraws", "Asura", "Rakete", "NKS", "Uraziel", "Ghost", "VirgilVanDih", "haten'", "Itsayax", "Boris", "BannedOnMain", "Vatiri", "Clmns", "exe", "kayz", "ritzke", "Miyho", "B", "Bacon!", "luca", "Chabub", "Jordi", "DOOMY", "rifo", "Dmy", "MoreChoiceLowerFaresGreatCare", "stuhli", "Kaiser", "kvre", "385ms", "spiegeleggs", "Movi", "BenniDLN", "frvt", "J", "Breqxi", "justify", "M", "teezay", "At07", "m1", "eexpir", "mxm", "Jonas", "Silas", "Flitzpiepe", "Timbales", "spelvatatsu", "moneytalks", "Twister", "CJ", "Juvi", "SenpaiBlank20yo", "2xxx", "R0nnix", "Westgeist", "Derlex", "synix", "Dissolved3003", "E", "EcK", "yeet", "echteemilia", "Natsu", "Len", "ApperantlyD", "Akeno", "alex", "Chelsea", "DiZzy", "Thiess", "Kami", "Abdulla", "madison", "Resority", "murice", "Dreyy", "Vipex", "Jesk", "schumiwnl", "Noa", "twnzr", "Oki", "manos", "ZeroTwo", "Tempo", "b", "Blaive", "Squizzel", "Mooisel", "Kalli", "Adraxah", "LeonIzzBack", "hunterzz", "N7mD", "washedaf", "Mash", "tenshi!", "ILoveAlinasHazeleyes", "Please", "qeo54"]
    # ... Fügen Sie hier Ihre ca. 1000 Spielernamen ein

if len(player_names_list_from_backend) < 50:
    for i in range(len(player_names_list_from_backend), 1000):
        player_names_list_from_backend.append(f"SpielerName_{i:03d}_{random.choice(['Alpha', 'Beta', 'Gamma', 'Delta'])}")

# --- Mock-Daten für alte Routen (können entfernt werden, wenn die Routen wegfallen) ---
mock_divisions_list = ["1", "2", "3.1", "3.2", "4A", "CHALLENGER SERIES"]
mock_teams_by_division = {
    "1": [
        {'id': 1, 'name': 'Team Galactic Force', 'wins': 5, 'losses': 1, 'win_loss_rate': 0.833, 'round_difference': 10},
        {'id': 2, 'name': 'Team Nebula Raiders', 'wins': 4, 'losses': 2, 'win_loss_rate': 0.667, 'round_difference': 7},
    ],
    "CHALLENGER SERIES": [
        {'id': 20, 'name': 'Rising Rockets', 'wins': 7, 'losses': 0, 'win_loss_rate': 1.0, 'round_difference': 15},
    ]
}
mock_all_teams_structured = {
    "top_divisions": {
        "1": [(1, "Team Galactic Force"), (2, "Team Nebula Raiders")],
    },
    "sub_divisions": {
        "3": { "3.1": [(4, "Team Orbital Mechanics")] }
    }
}
mock_team_details_map = {
    "1": {
        "info": (1, "Team Galactic Force"),
        "participants": [(101, "Player 'Zenith'", "Player")],
        "games": [("g1", "Team Galactic Force", "Team Nebula Raiders", 3, 1)],
        "division_teams": [(2, "Team Nebula Raiders")]
    }
}
# --- Ende Mock-Daten für alte Routen ---


# --- Hauptrouten ---
@app.route('/')
def route_home(): # Endpunktname für url_for in base.html/_header.html/_footer.html
    return render_template('index.html')

# --- Neue Routen basierend auf der aktualisierten Navigation ---
@app.route('/spielermatching')
def route_spielermatching():
    # Hier kommt die Logik für die Spielermatching-Seite
    # Erstellen Sie eine Datei templates/spielermatching.html
    return render_template('spielermatching.html', page_id="spielermatching_page", site_id="main_site")

@app.route('/spielerklassifikation')
def route_spielerklassifikation():
    # Hier kommt die Logik für die Spielerklassifikation-Seite
    # Sie hatten diese Route in der vorherigen index.html als 'spielerstatistiken'
    # Ich nehme an, das Template heißt nun spielerklassifikation.html
    # Erstellen Sie eine Datei templates/spielerklassifikation.html
    return render_template('spielerklassifikation.html', page_id="spielerklassifikation_page", site_id="main_site")

@app.route('/quotenmacher')
def route_quotenmacher():
    # Hier kommt die Logik für die Quotenmacher-Seite
    # Erstellen Sie eine Datei templates/quotenmacher.html
    return render_template('quotenmacher.html', page_id="quotenmacher_page", site_id="main_site")


@app.route('/spielerstatistiken')
def route_spielerstatistiken():
    return render_template('spielerstatistiken.html', page_id="spielerstatistiken_page", site_id="main_site")


@app.route('/stats') # Die Route für Statistiken, die im Header rechts verlinkt ist
def route_stats():
    # Ihre bestehende statistiken_seite Funktion wurde umbenannt und hier integriert
    # Erstellen Sie eine Datei templates/stats.html (oder benennen Sie spielerstatistiken.html um)
    return render_template('stats.html', page_id="stats_page", site_id="main_site")


# --- API-Route für Spielervorschläge (bleibt erhalten für Autocomplete) ---
@app.route('/api/player_suggestions')
def player_suggestions():
    query = request.args.get('q', '').strip().upper()
    if not query:
        return jsonify([])
    suggestions = [
        name for name in player_names_list_from_backend 
        if query in name.upper()
    ][:10]
    return jsonify(suggestions)



# --- Alte Routen (können auskommentiert oder entfernt werden, da nicht mehr im Hauptmenü) ---
# @app.route('/divisions')
# def divisions_route():
#     print("Displaying mock divisions list")
#     return render_template('divisions.html', divisions=mock_divisions_list, page_id="divisions_page", site_id="main_site")

# @app.route('/divisions/<division_name>')
# def division_detail(division_name):
#     teams_for_render = mock_teams_by_division.get(division_name, [])
#     print(f"Displaying mock team details for division: {division_name}")
#     return render_template(
#         'division_detail.html',
#         division=division_name,
#         teams=teams_for_render,
#         page_id=f"division_{division_name}_page", site_id="main_site"
#     )

# @app.route('/teams')
# def teams_route():
#     print("Displaying mock teams overview")
#     return render_template('teams.html',
#                            top_divisions=mock_all_teams_structured["top_divisions"],
#                            sub_divisions=mock_all_teams_structured["sub_divisions"],
#                            page_id="teams_page", site_id="main_site")


# @app.route('/teams/<team_id_str>', methods=['GET', 'POST', 'DELETE'])
# def team_detail_route(team_id_str):
#     # Diese Route ist komplex und würde eine tiefere Überarbeitung ohne DB benötigen
#     # oder man verweist auf eine separate Detailseite, die mit den neuen Anforderungen gestaltet wird.
#     # Fürs Erste mit Mock-Daten belassen, falls die URL noch direkt aufgerufen wird.
#     mock_details = mock_team_details_map.get(team_id_str)
#     if not mock_details:
#         generic_team_info = (int(team_id_str) if team_id_str.isdigit() else team_id_str, f"Team {team_id_str} (Details nicht gefunden)")
#         return render_template('team_detail.html',
#                                team=generic_team_info,
#                                participants=[], games=[], num_players=0, num_coaches=0, division_teams=[],
#                                page_id=f"team_{team_id_str}_page", site_id="main_site")
#     # ... (Rest der GET/POST/DELETE Logik mit mock_details wie zuvor) ...
#     team_info_for_template = mock_details.get("info", (team_id_str, f"Team {team_id_str}"))
#     current_participants = mock_details.get("participants", [])
#     num_players = sum(1 for p in current_participants if len(p) > 2 and p[2] == 'Player')
#     num_coaches = sum(1 for p in current_participants if len(p) > 2 and p[2] == 'Coach')
#     return render_template('team_detail.html',
#                            team=team_info_for_template,
#                            participants=current_participants,
#                            games=mock_details.get("games", []),
#                            num_players=num_players,
#                            num_coaches=num_coaches,
#                            division_teams=mock_details.get("division_teams", []),
#                            page_id=f"team_{team_id_str}_page", site_id="main_site")


# @app.route('/rulebook')
# def rulebook():
#     return render_template('rulebook.html', page_id="rulebook_page", site_id="main_site")


# @app.route('/signup', methods=['GET', 'POST']) # Entfernt, da kein Login/Signup mehr
# def signup():
#     # ... alte signup Logik ...
#     pass

# @app.route('/receive-message', methods=["POST"]) # Entfernt, falls nur für signup relevant
# def receive_message_route():
#     # ... alte receive_message Logik ...
#     pass

# async def send_discord_notification(name_param): # Behalten, falls anderweitig genutzt
#     # ... alte send_discord_notification Logik ...
#     pass


if __name__ == '__main__':
    print(f"Flask App startet auf Port 5000 (erreichbar über Docker-Mapping auf externen Port, z.B. 5003)")
    app.run(host="0.0.0.0", port=5000, debug=True)