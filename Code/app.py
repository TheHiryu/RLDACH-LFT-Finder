from flask import Flask, render_template, request, redirect, jsonify, flash
# from discord import Webhook
import random
#import json
import psycopg2
import os
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import pairwise_distances
import joblib


app = Flask(__name__)
app.secret_key = os.urandom(42)


# --- Beispiel-Spielerliste (bleibt für /api/player_suggestions) ---
player_names_list_from_backend = ["dayyshift","Rizex","Rezears","shila","scream33.","twnzr","ttv Striker Flow","!sk.","img.","Menzuu.","jinx.","Nyco","Tavix","spelvatatsu","Brainiac","qatixx","Gnagflow06","Jazii","MD",".","schnappi","RELYX seysores.","Kaiser â°","LeonIzzBack","I Love Alinas Hazel eyes","nlz","Fabso","Tigreee","Miyho.","Dreyy^^","Zeddo","Catalysm","Mash","WaveZ","Kyuu.","Phliip","Vano","Please","Q","Youngstar","Arda GÃ¼ler","Cheeky","Pindroy","Twister.","ritzke","requ","N7mD[?]","Sparky.","Poly","Beyazz","S.","energizer","Cloudy.","Luca","Flamezz","à­¨MSRà­§",".","Noah","Barou","Akeno","Alyiuu","qeo54","Golo","Snowyyy",".","Jraws â","DiZzy","Yeti","cookie","Jannik","Chabub","Bryan","RealMalbu","Lxuiis","Rias <3","Dmy","Eibur","madison","Heshy","Jonas.","kkatyonak","kaan","-Kaz-","Prod0x","Bombardino Crocodilo","Luiis","Hartmann","seltt","Husky.","Hiryu","zym.","Keks","Snoopy","tvylics","ankle","Revxnge.","hax","Fabi","SquishyMunching","Bacon!","Kawaii Nico (â§â½â¦)","timur4k zxc","Arashi","Anju.","kyza404","Fears","RnZ","Yumekoo","Tommy","ARk3YAN","riino","Mino","Phix","H4nn3s","Aquaknarre.",".","Moriitz.","Pumsy","Bxrchii","E.","Conschu","Bob Tschigarillo","Wat3r","prownzyyy.","Flo!","Desire","Âµ","77","BannedOnMain","lazy :)","Ersatzspieler","Beez","Waze","everjan66","m1 ð¹","Nico","manos ã",".","R0nnix.","bst.","L.","JulzZ.","NinjaminionZ","nex.","Risk0","zebu","tate <3","TrickShot^-^","Âµ","Aloey","CJÂµ","Es wird ehrenlos","Playboi Ryze","Nils","NKS","Dele","nibbolaus.","dNa","luca","nukezz!","THK.","Monski","sirvile","Nico","synix","Rease","ForGet","raqzy","wry","slashy","76561198077072980, ongod pxnlchrrrr","antboy","heinzzketchup","davee","Maggo","JustNoel","Sua","Mayzah â","Pls05","Sailor Miku <3","TravelSky","Rain",":âº","clxmens.","Sleeeeepy Flow â","Percy17","zane","Final","~Plexus","Valid","mÃ¸reritz","Mizu","Alexmeister","Kiremi","SARPBC Killajay-16","Tempo","Flex","Lj","gryhnd",".","Superzwerg","XW","tim","B","Carlos :)","Kaizen","eexpir","FATE","KVN","ImPmzZ",".","The Hamburger with Cheese","Clmnsâ","jirka","PadS","Lyrics","Derlex","TarGeT*","azumi","KESHI.","all the dogs are chasing","luggas","wiz","Wingz",",","Gemmel.7","Rio","ifuhsaif",".","Marcel.","JXDN","lexi.","Shrimp with a horn","LK.","Stupzy","Sn0wPanda","BROKEN THUMB GRR","Omit313 (chat off)","affenbande","rax","Niu_Komma","Quexxy.","Charlez","Anteez","Deniz","runni.","MkNsfsfsfsfsf","Tobi","SaubÃ¤r","Norttew","stuhli","Femboycracker83","phil","Reazzy","kimbo.","yoka.","Jzy",".","Blaive","mikerino!","advance. observe.","Lievito","Lyyvx.","Bamberek","m",".MiKa","hunterzz","Monjuk","b.","Crypto.RL","â  KYN","BurnyPee","â octraxâ","Gedeon","LionZz","Victarion","rombuskap","aqua","hi im sizl","Ripox.","x**2","xandar",".","MikeB0i","balou.","JackTheSecâ¢","naap848","Ravish","Ingo","Plat","chrs","Saiint","Rigl","Finex","yeet","Jesus","INVTS7.","Vince","iTxE7","OmaNascher69","pyhru","Zeniâ h","Maikoz","Fabi","ReRe.","m4a1dh","avoid.","Feetlover34","GunLeanmanGunLean","dp7th","Maze.","dÃ¶p",".Â´,","quyoo","_PlayMestre_","i would never","dot","YuiX",".jonjas","kvre","Timonster","L1K3R","Juzo.","more bitcoin more problems","Eylow","aspect","justchillin.420","Len","Maeve â","lemi","ntra","Frozy.","Rappiii","Kuko","385ms","Lq.","âï¸ C-ptn :(","Scotty. â","Sky<3","i play like you","F","dk","xva cmx","â  PJ â","BRUH","teezay","yummy","schumiwnl~","cel","Anna-Lena :3","Skyrunner_170","meezã","antzn","Zavo","Flexxy.","Ic3m4n","taycan","v0qe.<3","Hyrole","_Sarak_","Nioo","predii.","Facer","Jayku","Just Dean","seb","Physix_RL","Awx","A1re4x","Tronix","Waddy","c0by :âº","Emely","Veit","Fussel28","sarity","deshr","marv","Jorden","mgi","Reazyy","JBerg","Can. iwnl! ã","black5ky","Obigoon","At07","Ruby-Chan","Syrzzs",".Mitroooâ¢","Splashy","Shinoa","wilsbergg","Change","jjZZi .","Abc","murice","Cantus","Wavy(?)","JÃ¤ss.","Hansen","Tx0","eijÃ­","womzyy","Tomey","Frawin","sEr!aL ã","track","lou","kyu.","X","Aqueh","beGenius","Menvos","Kunotori","D A R K Z O N E","Repi66","celly",":)","Kryptos","Avicii","Gaetano","tls","Matrixx","jck.","b3nnyyy","Migne.","â rysh","EcK","RÃ¶Ã¶DA!","Ley (Randomized Cars only)","aspen","Ghost.",".","Imgn","Gyree.","Sama<3",".","ApperantlyD.","Asura","Fabe â","Mimicry96","Fishy K2","mauricem0","Sil","Schmocky23","eurorunix","Fumtastic","orochi -.-","Unc","zennin","goldie said trap","ribsteak","Toabdjzl","BastianR","Coco","Thiess.","free","Tanome","Vinex.","Luii","Rian","AqouZ","Cranddy","TKBOY","Dissolved3003","Robba","KFC the G","kryptoN","Syko","LzrShak","FE!N","Fared","Wahlsor","Dusty Dunker","KÃ¦vn",".MDK","t7mi","rivez.","Flonobo","Akiba","Mon_Key66","anga","Albrun","Dok","Unlucky","GustaV","jurl","Clutshy","Daeky","Slayer_Berlin","Croby","Yoeky","verixz","MH.â","Oni","Buster.","jurl","Clutshy","Rampage","Razzy","Dark.","Asus Prime B450M","M.","philip","frvt.","Isay","Rybu","ZedeX","noah.","Pxxloo","FLYING","blue","kilixn","Nexus","Stingray","Squizzel","zane","Veyn.","Uraziel","lepaniel","Kalemon","nkls ã","s!cK ;)","[E]","too_md","paulSZN","Brasnika","Revannx","Abdulla","NoToxic4u","knox","Jaynut","Fynn","Josef","Leschi","Lance","Jxshii","Thiess ._.","Exinho","Venso McQueen","Br0dah","Time2Lazer","ððð","r","Kalli.","c","PASCAL","HaZe.â","1","Craca","Elacior","Its.ayax","Breqxi","sascha",".gray","yutu.-","R3voG4ming","Trumps","PureHate","Z.","Jinx","Kiqo","Tyraâ¢","solid.","opertix.","rifo","mesh","ttv/LeeOuh","bretski","Arceus","KAR0TTENP0WERFan 1","Sqezz","Zoroo","Silas","vcx","Timinski",".","Darksmon","Emalyx","[OGG] â¤ ZeroTwo â¤","z.","Jasmin","Noa","storm","Loading....","zhypix","ikee279","vibindogee","neo.","Shino","Mino.","Mooisel :}","Kami","Jesk.","little Oogwayy^^","Bzkill","MaZ","sqtnx","Sranangtongo","viu.","vZ","// xelty","anxiety","nex",".","Oki","echte emilia","Timbales","T!KTOK HLGH [LIVE]","Lyserg.","KonsiKa","Henneâ¢","Trannel","rpsn","Flitzpiepe","uá´ÊÉ¹Éê½","a7ex","eric.","reasn","Goldennugg3t","Ginjo","P4in UwUâ¢","Nytro","Peta","YYRob","kayuun","Ryu.","Brennholz3000","Mr.Sunshine","Eus","ItsLeMax","â hopelessâ","Bagua","ExjuiceMe",".","Juvi","SoÄ« Fon!","Duon","Teo","SoundLucky","~hhenrck","Â´Â´","Vempa","FirePhoeniXx","no","jey","Clyro","Trizzletan","haten","kcaj","tobiray","xBarracuda","luap","Lairon :)","Wrixk","tizi. (chat off)","solorll_","Westgeist","judie","Whalexity","Rayy","Fujii","< Senpai Blank 20 yo>","Genis","Lvtona","Temp","dp","alex","Horizon","Staraptoah","Mozz","DonF1re","Kerze","Bobritto bandito","Seeeebi","OIIAI","shanks","Tetraflix","Rosenrot","Vension","St0rmi","ttv.SlaySRL","poow","xela.","DrunKingan","hasenkeule","nick","Abstract","Natsu","Vipex","ttv/helmoods","tabiospb","Lurax_btw","Peppa Pinch","zImpeL","HENTHE","Snupi","hmky.","[GBA] | _TheGrinder_","Ventus","Swenzy","fortnitegamer","DOOMY","Twitch: xqRs7","Phoenix","STEAR","Shiku","SunZ.","tenshi!","Anear","Lucifer","ph3x","washed af","TaQuiXâ","Dark-Sider_88","Bobbl","Maliken","TimKoschi","SPQR","ady","Gabe Owners","ju","dave[?]","Husk.","Toad","Jxuuls (Perma Banned)","Marcvader","lo","MoreChoice.LowerFares.GreatCare.","The_BMKP","Sonus","seb.","Virus","Mounteverrizz","waftlaft^-^","Kurdischsensei","Schiggy :)",".C.Mass","zRaynii","Buckster","MrGrony","Jesus","Fiftzzeh","Sensei","Nikoo ã","mavonyx","Cedric","saiiko99","Nucklan","maegiic","TriggerHappy","kkeno","Sucuki.","time.","Bryze","Soda","menqu","Putrik","staa","llamar","sakufadicheru","Van Der Sar","?",".","ShowCast","mrx.","âªBahamas","992","[NLR] gruhnd","foujeck <3","Vylipp","Any","Sharkyy","Sanjee","Justin","collin","Old man!","Skifty ^-^","MiG91110","TeeHee UwU UwO","Adraxah","adgoez","mxm.","x13-no-chat","lumyna","Ruvio","Denloe","Boris","Brain","Kovi.","Crmson","marv","ninho!!","á¶» ð ð°","Jamie.","StÃ¼mpy","456","she is wifey material","5kimi","Jos","Kobrick","Saut","CheeseLover","spiegeleggs","Movi","Theodore Jasper Detweiler","Virgil Van Dih","VolleRoffl","polar","Pfandi","LimitRL","Juicy","uxt.","Trinity","A1M.BL1ND",".","Drecksgame","Luca","lyrix","J.","Cryptiic","BOBâ¢","Happy :]","Nox","xImmerDruff69","Shawarma","tuco tucito salamanca","T7lm","Dom. ^^","à¹",".","txmmy","Relox","Ex0tical","Rey","Kontra","Fuwamoco","mafiahuhn.","Obi Wag-Wan","Eryyc","lennerd","Letzoff","DarkHawk [MHR_Nr10]","DyseUp","Oschi","Scopes","MrPatchino","Dave","Wizurd","flow","iMischunja","stelu","quiply","Gerry","crasery.","Lil Rudi","Zero Two","Rakete","M.","Jonna ayri","R Ã G E","topfit","Skartes","Griffin","faab","JackDjTom","Rndy.","*-*","TRA","Vempa","Gimme","Waldi","nygama","NicX","Coby","Vito","nick.","M-9 TempesT","Dwoopy","~","K","Maufius95","frozen","justify","DraXie","XVII","Yukisekki","lele","Myrtle","Just a Shadow","Rockmysox","Link","Samy","tyler.","DrNuts","GLF","NI","dd","apex.","Phillegal","DerManager","Yoloboy^-^","Marv","Flywalker","KabseR","Schlafi","Vatiri","sCito9","BXRK RL","vel","ATLAS","Luhkey","Noiizy","ResorityÂ¥","heppy doge","maaybie","muy rico","Monkeyman","albo","YARY","SwkT","LostJ3ster","SpiderDxD","jannes abi","ihy.","seb","Sean","Jordi","Phyn","Kingkazay","BenniDLN","Jere.","2xxx",".exe","Boaty McBoatface","Kampi","Saint","KranKe SchranKe!","bob","JayBeaR.","spreatex","gohaN",".","Gilibi ^^","Mr. Squiddy",".","getting robbed","Headshotski","//zyde.","LeftKick_","...","Gitto.","Zeptic","Freex!","kayz","Aarivex","HERRBEYSEN","Delta","money talks","plastikmuell","muzan","dmnc. (New to Square-Deadzone)","rintintin","rYu 89er","get Snek´d","bruh","Don_King95","0","n4ykzz","anti.","zMkr.","stivi","huz (smurf)","nfb","Kygo","Imagine.","Masha from O´Block","SpinatEsser","Enter.","NyxxOCE","Leytrix","Harlem","tryath","dwizzy twizzy cwipzy","Chelsea","tobi dobrze robi","Timbo","Pikatra","Gabriel","yukain","BanditSkyfall ,O_O,","be careful!","tehe","tr1","Dark-Hero9864","XMK."]
if len(player_names_list_from_backend) < 50:
    for i in range(len(player_names_list_from_backend), 1000):
        player_names_list_from_backend.append(f"SpielerName_{i:03d}_{random.choice(['Alpha', 'Beta', 'Gamma', 'Delta'])}")



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

    return render_template('quotenmacher.html', page_id="quotenmacher_page", site_id="main_site")


@app.route('/spielerstatistiken', methods=["GET", "POST"]) # Die Route für Spielerstatistiken, die im Header links verlinkt ist
def route_spielerstatistiken():
    if request.method == 'POST':
        player_name = request.form.get("playerName", default=None)

        df = pd.read_csv('matches.csv')
        feature_cols = [
            'stats_core_goals', 'stats_core_goals_against', 'stats_core_saves',
            'stats_core_assists', 'stats_core_score', 'stats_boost_amount_collected',
            'stats_boost_amount_stolen', 'stats_movement_avg_speed_percentage',
            'stats_positioning_avg_distance_to_ball', 'stats_positioning_percent_defensive_third',
            'stats_positioning_percent_offensive_third', 'stats_positioning_percent_behind_ball',
            'stats_demo_inflicted', 'stats_demo_taken'
        ]

        # Initialisiere cats leer
        cats = None

        mask = df['player_name'].str.lower() == player_name.lower()
        player_id = int(df.loc[mask, 'player_id'].iloc[0])
        if player_id:
            # Preprocessing
            imp = SimpleImputer(strategy='median')
            X_imp = imp.fit_transform(df[feature_cols])
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X_imp)
                # Ähnliche Spieler berechnen
            def find_three_categories(player_id: int, k: int = 5):
                idx_list = df.index[df['player_id'] == player_id].tolist()
                if not idx_list:
                    raise KeyError(f"player_id {player_id} nicht gefunden")
                idx = idx_list[0]

                dists = pairwise_distances([X_scaled[idx]], X_scaled, metric='cosine').flatten()

                df_d = pd.DataFrame({
                    'player_id': df['player_id'].values,
                    'player_name': df['player_name'].values,
                    'distance': dists
                })
                df_d = df_d[df_d['player_id'] != player_id].reset_index(drop=True)
                df_d['similarity'] = 1 - df_d['distance']

                selected_ids = set()
                result = {}

                df_nearest = (
                    df_d.sort_values('distance')
                        .drop_duplicates('player_id')
                        .head(k)
                        .copy()
                )
                result['nearest'] = df_nearest
                selected_ids.update(df_nearest['player_id'])

                df_neutral = (
                    df_d.assign(diff_abs=lambda d: (d['distance'] - 1).abs())
                        .sort_values('diff_abs')
                        .loc[~df_d['player_id'].isin(selected_ids)]
                        .drop_duplicates('player_id')
                        .head(k)
                        .copy()
                )
                result['neutral'] = df_neutral
                selected_ids.update(df_neutral['player_id'])

                df_opposite = (
                    df_d.assign(diff_abs=lambda d: (d['distance'] - 2).abs())
                        .sort_values('diff_abs')
                        .loc[~df_d['player_id'].isin(selected_ids)]
                        .drop_duplicates('player_id')
                        .head(k)
                        .copy()
                )
                result['opposite'] = df_opposite

                return result

            cats = find_three_categories(player_id=player_id, k=5)
            if cats:
                for key in cats:
                    cats[key] = cats[key].to_dict(orient='records')
        return render_template(
            'spielerstatistiken.html',
            page_id="spielerstatistiken_page",
            site_id="main_site",
            cats=cats,
            player_name=player_name)
    else:
        return render_template(
            'spielerstatistiken.html',
            page_id="spielerstatistiken_page",
            site_id="main_site",
            cats=None,
            player_name=None
        )



@app.route('/stats') # Die Route für Statistiken, die im Header rechts verlinkt ist
def route_stats():
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



@app.route('/api/player_stats', methods = ['POST'])
def player_stats():
    data = request.get_json()
    player_name = data.get('name', '').strip()

    if not player_name:
        return jsonify({'error': 'Kein Spielername angegeben'}), 400
    
    try:
        DB_CONFIG = {
            'dbname': 'RLReplays',
            'user': 'postgres',
            'password': 'postgres',
            'host': 'db',
            'port': 5432
        }
        
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("""
                    SELECT player_id 
                    FROM replay_stats
                    WHERE name = %s
                    """, (player_name,))

        result = cur.fetchone()

        player_id = get_player_id(cur, player_name)

        if result is None:
            return jsonify({'error': 'Spielername nicht gefunden'}), 404

        cur.execute("""
            SELECT prob_cluster_0_median, prob_cluster_1_median, prob_cluster_2_median, prob_cluster_3_median 
            FROM player_stats 
            WHERE player_id = %s
        """, (player_id,))

        playstyles = cur.fetchone()
    
        cur.close()
        conn.close()

        if playstyles is None:
            return jsonify({'error': 'Keine Statistiken für diesen Spieler gefunden'}), 404
        
        labels = ['Fast Attacker, 1st man', 'Konterspieler, 2nd man', 'Libero, 3rd man', 'Mixed Style']
        values = list(playstyles)

        return jsonify({'labels': labels, 'values': values})

    except Exception as e:
        print(f"Fehler bei DB-Zugriff: {e}")
        return jsonify({'error': f"Fehler bei DB-Zugriff: {e}"}), 500


def get_player_id(cur, player_name):
        cur.execute("""
                    SELECT player_id 
                    FROM replay_stats
                    WHERE name = %s
                    """, (player_name,))

        result = cur.fetchone()

        return result[0]








FEATURE_COLS = [
    'stats_core_goals', 'stats_core_goals_against', 'stats_core_saves',
    'stats_core_assists', 'stats_core_score', 'stats_boost_amount_collected',
    'stats_boost_amount_stolen', 'stats_movement_avg_speed_percentage',
    'stats_positioning_avg_distance_to_ball', 'stats_positioning_percent_defensive_third',
    'stats_positioning_percent_offensive_third', 'stats_positioning_percent_behind_ball',
    'stats_demo_inflicted', 'stats_demo_taken'
]

def find_three_categories(df: pd.DataFrame, X_scaled, player_id: int, k: int = 5):
    idx = df.index[df['player_id'] == player_id]
    if idx.empty:
        raise KeyError(f"player_id {player_id} nicht gefunden")
    idx = idx[0]

    dists = pairwise_distances([X_scaled[idx]], X_scaled, metric='cosine').flatten()
    df_d = pd.DataFrame({
        'player_id': df['player_id'],
        'name': df['name'],
        'distance': dists
    }).query("player_id != @player_id").reset_index(drop=True)
    df_d['similarity'] = 1 - df_d['distance']

    selected = set()
    cats = {}

    # Nearest
    nearest = df_d.sort_values('distance').drop_duplicates('player_id').head(k).copy()
    cats['nearest'] = nearest
    selected |= set(nearest['player_id'])

    # Neutral (Distanz ~ 1)
    tmp = df_d.assign(diff_abs=lambda d: (d['distance'] - 1).abs())
    neutral = tmp[~tmp['player_id'].isin(selected)].sort_values('diff_abs').head(k).copy()
    cats['neutral'] = neutral
    selected |= set(neutral['player_id'])

    # Opposite (Distanz ~ 2)
    tmp = df_d.assign(diff_abs=lambda d: (d['distance'] - 2).abs())
    opposite = tmp[~tmp['player_id'].isin(selected)].sort_values('diff_abs').head(k).copy()
    cats['opposite'] = opposite

    return {k: v.to_dict(orient='records') for k, v in cats.items()}

@app.route('/tinder', methods=['GET'])
def tinder():
    player_name = request.args.get('playerName', default='').strip()
    cats = None

    if player_name:
        # CSV einlesen
        df = pd.read_csv('matches.csv')

        # Spieler-ID finden
        mask = df['name'].str.lower() == player_name.lower()
        if not mask.any():
            flash(f"Spieler '{player_name}' nicht gefunden.")
        else:
            player_id = int(df.loc[mask, 'player_id'].iloc[0])
            # Preprocessing
            imp = SimpleImputer(strategy='median')
            X_imp = imp.fit_transform(df[FEATURE_COLS])
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X_imp)

            # Kategorien berechnen
            raw_cats = find_three_categories(df, X_scaled, player_id, k=5)
            for category, players in raw_cats.items():
                for entry in players:
                    # Suche den Namen zur ID und speichere ihn
                    name = df.loc[
                        df['player_id'] == entry['player_id'],
                        'name'
                    ].iat[0]
                    entry['name'] = name

            # cats enthält jetzt zu jedem Eintrag auch den player_name
            cats = raw_cats
    return render_template(
        'spielermatching.html',
        player_name=player_name,
        cats=cats
    )





if __name__ == '__main__':
    print(f"Flask App startet auf Port 5000 (erreichbar über Docker-Mapping auf externen Port, z.B. 5003)")
    app.run(host="0.0.0.0", port=5000, debug=True)

