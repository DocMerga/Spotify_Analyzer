import sqlite3
import pandas as pd

def drop_db():
    conn = sqlite3.connect("Spotify_Analyzer\\main_database.sqlite")
    cur = conn.cursor()

    cur.executescript("""   DROP TABLE IF EXISTS AllStreams;
                            DROP TABLE IF EXISTS Reason;
                            DROP TABLE IF EXISTS Boolean;
                            DROP TABLE IF EXISTS PlaylistItem;
                            DROP TABLE IF EXISTS Playlist;
                            DROP TABLE IF EXISTS Track;
                            DROP TABLE IF EXISTS Track_Artist;
                            DROP TABLE IF EXISTS Album;
                            DROP TABLE IF EXISTS Album_Type;
                            DROP TABLE IF EXISTS Release_Date_Precision;
                            DROP TABLE IF EXISTS Album_Artist;
                            DROP TABLE IF EXISTS Artist;
                            DROP TABLE IF EXISTS Location;
                            DROP TABLE IF EXISTS Artist_Genre;
                            DROP TABLE IF EXISTS Country;
                            DROP TABLE IF EXISTS CountryList;
                            DROP TABLE IF EXISTS Genre;
                            DROP TABLE IF EXISTS Isrc;                            
                            """)
    cur.close()
    conn.close()


def generate_db():

    conn = sqlite3.connect("Spotify_Analyzer\\main_database.sqlite")
    cur = conn.cursor()

    cur.executescript("""CREATE TABLE IF NOT EXISTS AllStreams (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        ts TEXT UNIQUE,                        
                        ms_played INTEGER,
                        spotify_track_uri TEXT,
                        spotify_episode_uri TEXT,
                        spotify_track_id TEXT,
                        reason_start_id INTEGER,
                        reason_end_id INTEGER,
                        platform_id INTEGER,
                        shuffle_id INTEGER,
                        skipped_id INTEGER,
                        offline_id INTEGER,
                        track_id INTEGER
                        );

                    CREATE TABLE IF NOT EXISTS Platform (
                        id INTEGER NOT NULL PRIMARY KEY,
                        name TEXT UNIQUE
                    );

                    CREATE TABLE IF NOT EXISTS Reason (
                        id INTEGER NOT NULL PRIMARY KEY,
                        reason TEXT UNIQUE
                        );
                        
                    CREATE TABLE IF NOT EXISTS Boolean (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        boolean TEXT UNIQUE
                        );
                    
                    INSERT OR IGNORE INTO Boolean (boolean) VALUES ("null");
                    INSERT OR IGNORE INTO Boolean (boolean) VALUES ("true");
                    INSERT OR IGNORE INTO Boolean (boolean) VALUES ("false");
                    
                    CREATE TABLE IF NOT EXISTS PlaylistItem (
                            id INTEGER NOT NULL PRIMARY KEY,
                            added_at TEXT,
                            added_by_id TEXT,
                            track_id INTEGER,
                            playlist_id INTEGER,
                            UNIQUE (added_at, track_id, playlist_id)
                        );
                    
                    CREATE TABLE IF NOT EXISTS Playlist (
                            id INTEGER NOT NULL PRIMARY KEY,
                            name TEXT,
                            spotify_id TEXT UNIQUE
                        );
                    
                    CREATE TABLE IF NOT EXISTS Track (
                        id INTEGER NOT NULL PRIMARY KEY,
                        duration INTEGER,
                        explicit INTEGER,
                        isrc TEXT,
                        isrc_id INTEGER,
                        spotify_id TEXT UNIQUE,
                        name TEXT,
                        popularity INTEGER,
                        album_id INTEGER,
                        playcount INTEGER,                        
                        info_retrieved INTEGER,
                        acousticness REAL,
                        danceability REAL,
                        energy REAL,
                        instrumentalness REAL,
                        key INTEGER,
                        liveness REAL,
                        loudness REAL,
                        mode INTEGER,
                        speechiness REAL,
                        tempo  REAL,
                        time_signature INTEGER,
                        valence REAL,
                        audio_features_retrieved INTEGER
                        );
                    
                    CREATE TABLE IF NOT EXISTS Track_Artist (
                            track_id INTEGER,
                            artist_id INTEGER,
                            PRIMARY KEY (track_id, artist_id)
                        );

                        CREATE TABLE IF NOT EXISTS Album (
                            id INTEGER NOT NULL PRIMARY KEY, 
                            album_type_id INTEGER,
                            total_tracks INTEGER,
                            spotify_id TEXT UNIQUE,
                            name TEXT,
                            release_date TEXT,
                            release_date_precision_id TEXT,
                            popularity INTEGER,
                            playcount INTEGER,
                            info_retrieved INTEGER
                        );

                        CREATE TABLE IF NOT EXISTS Album_Type (
                            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            name TEXT UNIQUE
                        );

                        INSERT OR IGNORE INTO Album_Type (name) VALUES ("album");
                        INSERT OR IGNORE INTO Album_Type (name) VALUES ("single");
                        INSERT OR IGNORE INTO Album_Type (name) VALUES ("compilation");

                        CREATE TABLE IF NOT EXISTS Release_Date_Precision (
                            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            name TEXT UNIQUE
                        );

                        INSERT OR IGNORE INTO Release_Date_Precision (name) VALUES ("year");
                        INSERT OR IGNORE INTO Release_Date_Precision (name) VALUES ("month");
                        INSERT OR IGNORE INTO Release_Date_Precision (name) VALUES ("day");

                        CREATE TABLE IF NOT EXISTS Album_Artist (
                            album_id INTEGER,
                            artist_id INTEGER,
                            PRIMARY KEY (album_id, artist_id)
                        );

                        CREATE TABLE IF NOT EXISTS Artist (
                            id INTEGER NOT NULL PRIMARY KEY,
                            spotify_id TEXT UNIQUE,
                            name TEXT,
                            popularity INTEGER,
                            followers INTEGER,
                            playcount INTEGER,
                            info_retrieved INTEGER,
                            location_id INTEGER,
                            location_retrieved INTEGER,
                            start TEXT,
                            end TEXT,
                            musicbrainz_retrieved INTEGER,
                        );

                        CREATE TABLE IF NOT EXISTS Location (
                            id INTEGER NOT NULL PRIMARY KEY,
                            city TEXT,
                            countrylist_id INTEGER,
                            playcount INTEGER,
                            latitude FLOAT,
                            longitude FLOAT,
                            coordinates_retrieved INTEGER,
                            UNIQUE (city, countrylist_id)
                        );

                        CREATE TABLE IF NOT EXISTS Artist_Genre (
                            artist_id INTEGER,
                            genre_id INTEGER,
                            PRIMARY KEY (artist_id, genre_id)
                        );

                        CREATE TABLE IF NOT EXISTS Country (
                            id INTEGER NOT NULL PRIMARY KEY,
                            name TEXT UNIQUE,
                            playcount INTEGER,
                            countrylist_id INTEGER
                        );

                        CREATE TABLE IF NOT EXISTS CountryList (
                            id INTEGER NOT NULL PRIMARY KEY,
                            country TEXT UNIQUE,
                            alpha2 TEXT UNIQUE,
                            alpha3 TEXT UNIQUE,
                            numeric_code INTEGER,
                            latitude FLOAT,
                            longitude FLOAT,
                            playcount INTEGER
                        );

                        CREATE TABLE IF NOT EXISTS Genre (
                            id INTEGER NOT NULL PRIMARY KEY,
                            name TEXT UNIQUE,
                            playcount INTEGER
                        );

                        CREATE TABLE IF NOT EXISTS Isrc (
                            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            country_short TEXT UNIQUE,
                            country TEXT,
                            playcount INTEGER
                        );
                    """)
    
    #reads in isrc countries from external text file and inserts them into main_database.sqlite
    fh = open(r"Spotify_Analyzer\data\isrc_countries.txt", "r", encoding="utf8")
    for line in fh:
        country_short = line[:2]
        country = line[2:].strip()
        cur.execute("INSERT OR IGNORE INTO Isrc (country_short, country, playcount) VALUES (?, ?, 0)", (country_short, country))        
    conn.commit()
    fh.close()

    countryList = pd.read_csv(r"Spotify_Analyzer\data\country-coord.csv")
    i=0
    len_index = len(countryList.index)
    while i < len_index:
        cur.execute("""INSERT OR IGNORE INTO CountryList    (country, alpha2, alpha3, numeric_code, latitude, longitude, playcount)
                                                    VALUES  (?,?,?,?,?,?,0)""", 
                                                            (countryList.iloc[i]["Country"], countryList.iloc[i]["Alpha-2 code"], countryList.iloc[i]["Alpha-3 code"],
                                                             int(countryList.iloc[i]["Numeric code"]), countryList.iloc[i]["Latitude (average)"], countryList.iloc[i]["Longitude (average)"]))
        i = i+1
    conn.commit()
    cur.close()
    conn.close()


