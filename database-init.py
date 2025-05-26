import pandas as pd
import psycopg2
from psycopg2 import sql
import os

DB_CONFIG = {
    'dbname': 'RLReplays',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': 5432
}

CSV_FILE_REPLAYS = './Replays/matches.csv'
CSV_FILE_PLAYER = './DASC/player_probs.csv'
GRAPH_FOLDER = './plots'
TABLE_NAME_REPLAYS = 'replay_stats'
TABLE_NAME_PLAYER = 'player_stats'
TABLE_NAME_GRAPHS = 'graphs'


def infer_pg_type(dtype):
    """Map pandas dtypes to PostgreSQL types."""
    if pd.api.types.is_integer_dtype(dtype):
        return 'BIGINT'
    elif pd.api.types.is_float_dtype(dtype):
        return 'REAL'
    elif pd.api.types.is_bool_dtype(dtype):
        return 'BOOLEAN'
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return 'TIMESTAMP'
    else:
        return 'TEXT'

def create_table_from_df(conn, df, table_name):
    with conn.cursor() as cur:
        columns = [
            sql.SQL("{} {}").format(
                sql.Identifier(col),
                sql.SQL(infer_pg_type(dtype))
            )
            for col, dtype in df.dtypes.items()
        ]
        cur.execute(sql.SQL("DROP TABLE IF EXISTS {}").format(sql.Identifier(table_name)))
        create_stmt = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({});").format(
            sql.Identifier(table_name),
            sql.SQL(',').join(columns)
        )
        cur.execute(create_stmt)
        cur.close()
        conn.commit()

def insert_data(conn, df, table_name):
    """Insert DataFrame into PostgreSQL table using COPY for speed."""
    with conn.cursor() as cur:
        tmp_csv = 'tmp_data.csv'
        df.to_csv(tmp_csv, index=False, header=False)
        with open(tmp_csv, 'r', encoding='utf-8') as f:
            cur.copy_expert(
                sql.SQL("COPY {} FROM STDIN WITH CSV").format(sql.Identifier(table_name)),
                f
            )
        conn.commit()
        os.remove(tmp_csv)


def create_graph_table(conn, table_name):
    with conn.cursor() as cur:
        cur.execute(sql.SQL("DROP TABLE IF EXISTS {}").format(sql.Identifier(table_name)))
        cur.execute(sql.SQL("""
            CREATE TABLE IF NOT EXISTS {} (
                image_name TEXT,
                image_data BYTEA
            );
        """).format(sql.Identifier(table_name)))
        conn.commit()
    conn.close()

def insert_graphs(conn, table_name, folder_path):
    for filename in os.listdir(folder_path):
        image_path = os.path.join(folder_path, filename)
        with open(image_path, 'rb') as f:
            binary_data = f.read()

        conn = psycopg2.connect(**DB_CONFIG)
        with conn.cursor() as cur:
            cur.execute(f"""
                INSERT INTO {table_name} (image_name, image_data)
                VALUES (%s, %s);
            """, (image_path.split('\\')[-1], binary_data))
            conn.commit()
        conn.close()

def main():
    print("Lade Replay CSV...")
    df_replays = pd.read_csv(CSV_FILE_REPLAYS)
    print(f"CSV geladen mit {len(df_replays)} Zeilen und {len(df_replays.columns)} Spalten.")

    print("Verbinde mit Datenbank...")
    conn = psycopg2.connect(**DB_CONFIG)

    print("Erstelle Replay-Tabelle...")
    create_table_from_df(conn, df_replays, TABLE_NAME_REPLAYS)

    print("Importiere Daten...")
    insert_data(conn, df_replays, TABLE_NAME_REPLAYS)

    print("Import abgeschlossen.")
    
    print("Lade Player CSV...")
    df_player = pd.read_csv(CSV_FILE_PLAYER)
    print(f"CSV geladen mit {len(df_player)} Zeilen und {len(df_player.columns)} Spalten.")

    print("Erstelle Spielertabelle")
    create_table_from_df(conn, df_player, TABLE_NAME_PLAYER)

    print("Importiere Daten...")
    insert_data(conn, df_player, TABLE_NAME_PLAYER)

    print("Erstelle Bilderdatenbank")
    create_graph_table(conn, TABLE_NAME_GRAPHS)

    print("Importiere Graphen")
    insert_graphs(conn, TABLE_NAME_GRAPHS, GRAPH_FOLDER)

    print("Import abgeschlossen.")
    conn.close()

if __name__ == "__main__":
    main()