##Reads the playlist tracks from a specified playlist

#request for GET to interact with Spotify. json to dump playlist data with indent. sqllite for database generation
import requests
import json
import sqlite3
import pprint
import time

def dump(access_token, spotify_playlist_id):
    #Header line specified for Spotify authentification
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }    
    BASE_URL_PLAYLIST = "https://api.spotify.com/v1/" #Base URL for interaction with spotify endpoints

    path = "Spotify_Analyzer\\dump\\" + spotify_playlist_id + ".sqlite" #path for database dump
    conn = sqlite3.connect(path)
    cur = conn.cursor()

    #Potentially already available data will be deleted
    cur.execute("DROP TABLE IF EXISTS Tracks")
    cur.execute("""CREATE TABLE IF NOT EXISTS Tracks(
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    track BLOB)""")

    limit = 50
    offset = 0
    songsLeft = True

    while songsLeft:
        #GET Method for json of playlist items (headers for authentification). 
        #limit= number of tracks (Default: 20. Minimum: 1. Maximum: 50)
        #offset = The index of the first item to return. Default: 0 (the first item). Use with limit to get the next set of items.
        playlist_data = requests.get(BASE_URL_PLAYLIST + "playlists/" + spotify_playlist_id + "/tracks", 
                                    headers=headers,
                                    params={"limit": limit, "offset": offset}) 

        #Transforms return form GET into json.
        playlist_data = playlist_data.json()

        #FOR DEBUGGING
        #print(json.dumps(playlist_data, indent=4))

        songs = playlist_data["items"]

        #dumps json string for eacht Track into the Database
        for item in songs:
            #print(json.dumps(item))
            #x = json.dumps(item)
            cur.execute('INSERT INTO Tracks (track) VALUES (?)',(json.dumps(item), ))
        conn.commit() 

        print(f"Tracks {offset} to {offset+limit} from overall {playlist_data['total']} tracks retrieved")   
  
        #Checks if there are still tracks to retrieve (playlist_data["total"]=overall number of tracks in playlist) --> Stops loop if not
        #also sets the offset for the next loop iteration    
        try:
            if offset + limit < playlist_data["total"]:
                songsLeft = True
                offset = offset + limit
                time.sleep(1)
            else:
                print(f"All {playlist_data['total']} tracks from playlist {spotify_playlist_id} retrieved")
                songsLeft = False
        except:
            print("Error: Unexpected loop end")
            break
    
    cur.close()
    conn.close()