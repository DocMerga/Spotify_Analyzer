##requestToken.py is used to GET access_token from Spotify Web API using client_id and client_secret
#hidden.oauth contains the client_id and client_secret
import requests
import hidden

def requestToken():
    #URL for Token request
    AUTH_URL = 'https://accounts.spotify.com/api/token'

    #saves client_id and client_secret from hidden.oauth() (returns dictonary) in var client
    client = hidden.oauth()

    #post a request to Spotify using the "client_credentials" authentification method and gets json object containing the token as return
    auth_response = requests.post(AUTH_URL, {
        "grant_type": 'client_credentials',
        "client_id": client["client_id"],
        "client_secret": client["client_secret"], 
    })

    auth_response_data = auth_response.json()
    access_token = auth_response_data["access_token"]

    #print("Access Token:", access_token)
    return access_token
    