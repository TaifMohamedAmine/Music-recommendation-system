import pandas as pd
import csv

'''
we downloaded some csv files of different genres of music and gathered them into a csv file data.csv
download url : https://www.kaggle.com/datasets/siropo/spotify-multigenre-playlists-data

'''

cols = ['id','danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature']
total_tracks = 0 

with open('data.csv', "w") as f :
    writer = csv.writer(f)
    for item in ["alternative_music_data.xls","blues_music_data.xls","hiphop_music_data.xls","indie_alt_music_data.csv","metal_music_data.csv", "pop_music_data.csv","rock_music_data.csv"]: 
        data = pd.read_csv(item)[cols].values.tolist()
        print("the number of tracks is : ", len(data))
        total_tracks += len(data)
        for row in data : 
            writer.writerow(row)
print("the total number of tracks is : ", total_tracks)






