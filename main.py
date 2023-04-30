import os 
from requests import post, get
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth


import csv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

scopes = 'user-read-currently-playing user-top-read'

sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(client_id = client_id, client_secret = client_secret , redirect_uri="http://localhost:3000", scope=scopes))

try:
    # Let's extract the name and id of my playlists 
    my_playlists = []
    for i in range(10) : 
        playlist_name, playlist_id = sp.current_user_playlists()['items'][i]['name'], sp.current_user_playlists()['items'][i]['id']
        tmp = [playlist_name, playlist_id]
        my_playlists.append(tmp)
        print(playlist_name, playlist_id)
    ''' 
    # my top artists :o
    my_top_artists = []
    for j in range(10) :
        top_artist, artist_id = sp.current_user_top_artists()['items'][j]['name'], sp.current_user_top_artists()['items'][j]['name']
        my_top_artists.append([top_artist, artist_id])
        print(top_artist)'''

    # Now let's extract the tracks of each  playlist : 
    
    print("*"*200)
    playlist_name, playlist_id = my_playlists[4][0],my_playlists[4][1] # let's select our 5th playlist : rap again
    playlist_tracks= []
    for j in range(len(sp.playlist_items(playlist_id=playlist_id, limit= 100)['items'])) :
        track_id = sp.playlist_items(playlist_id=playlist_id)['items'][j]['track']['id'] # adds to a list of track ids 
        playlist_tracks.append(track_id)
        print('track ',j, 'has the id : ', track_id)

    # Let's extract the track features of the given playlist

    print("*"*200)
    track_features = []
    for k in range(len(playlist_tracks)): 
        track_id = playlist_tracks[k]
        feature_dic = sp.audio_features(track_id)[0]
        feature_dic.pop('duration_ms')
        track_ft = list(feature_dic.values())
        no_str_fts = [item for item in track_ft if not isinstance(item, str)]
        print("track ", k ,"has this features :", no_str_fts)
        track_features.append(track_features)



except spotipy.SpotifyOauthError as e: # refresh the access token 
    sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(client_id = client_id, client_secret = client_secret , redirect_uri="http://localhost:3000", scope=scopes))







