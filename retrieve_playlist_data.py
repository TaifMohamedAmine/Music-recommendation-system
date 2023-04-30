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

rap_playlist_id = "2ykQBenlmpQr8L6LZpOLA6"

scopes = 'user-read-currently-playing user-top-read'


def get_playlist_tracks(playlist_name, playlist_id): 
    '''
    this function retrieves the users playlist, get all of the tracks in that playlist, then gets the audio features of them,
      finally saves them in csv file
    '''

    # get the number of tracks in the list
    playlist = sp.playlist(playlist_id=playlist_id)
    total_tracks = playlist['tracks']['total']
    print("the total number of tracks : ", total_tracks)
    
    
    # Let's get the all the track ids of our playlist
    i = 0
    playlist_tracks= []
    while total_tracks > 0 :
        offset = i 
        for j in range(len(sp.playlist_items(playlist_id=playlist_id, limit= 100)['items'])) :
            try :
                track_id = sp.playlist_items(playlist_id=playlist_id, offset=offset)['items'][j]['track']['id'] # adds to a list of track ids 
                playlist_tracks.append(track_id)
                print('track ',j, 'has the id : ', track_id)
            except :
                break
        i += 100
        total_tracks -= 100
    
    print("*"*200)
    
    # Let's now get the features of the tracks ids we got from the playlist  
    track_features = []
    for k in range(len(playlist_tracks)): 
        track_id = playlist_tracks[k]
        feature_dic = sp.audio_features(track_id)[0]
        feature_dic.pop('duration_ms') # no need for duration
        track_ft = list(feature_dic.values())
        no_str_fts = [item for item in track_ft if not isinstance(item, str)]
        print("track ", k ,"has this features :", no_str_fts)
        track_features.append(no_str_fts)
    
    # Let's now right this playlist content in a csv file
    print("now let's write "+playlist_name+" in a csv file :")
    with open(playlist_name+'_playlist.csv', "w") as f :
        writer = csv.writer(f)

        for row in track_features : 
            writer.writerow(row)


    return track_features 

sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(client_id = client_id, client_secret = client_secret , redirect_uri="http://localhost:3000", scope=scopes, requests_timeout = 10))

try:
    # Let's extract the name and id of my playlists 
    my_playlists = []
    for i in range(10) : 
        playlist_name, playlist_id = sp.current_user_playlists()['items'][i]['name'], sp.current_user_playlists()['items'][i]['id']
        tmp = [playlist_name, playlist_id]
        my_playlists.append(tmp)
        print(playlist_name, playlist_id)

    # now let's write our playlists in csv files 
    for playlist_name , playlist_id in my_playlists : # for 
        playlist_tracks = get_playlist_tracks(playlist_name, playlist_id)

    ''' 
    # my top artists :o
    my_top_artists = []
    for j in range(10) :
        top_artist, artist_id = sp.current_user_top_artists()['items'][j]['name'], sp.current_user_top_artists()['items'][j]['name']
        my_top_artists.append([top_artist, artist_id])
        print(top_artist)'''

except spotipy.SpotifyOauthError as e: # refresh the access token 
    sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(client_id = client_id, client_secret = client_secret , redirect_uri="http://localhost:3000", scope=scopes))









