import pandas as pd

# read in keys from separte csv file
keys = pd.read_csv("../Spotify_Analyzer_hidden/keys.csv", delimiter=";", index_col=0, header=None)

#Spotify
def oauth():
    return {     
        #Playlist-Analyzer2
        "client_id": keys.loc["Spotify_client_id"][1],
        "client_secret": keys.loc["Spotify_client_secret"][1]
    }

def oauthChatGPT(): 
    return {
        "API_key": keys.loc["ChatGPT_API_key"][1]
    }

def oauthGoogleMaps():
    return {
        "API_key": keys.loc["GoogleMaps_API_key"][1],
        "Secret": keys.loc["GoogleMaps_secret"][1]
    }