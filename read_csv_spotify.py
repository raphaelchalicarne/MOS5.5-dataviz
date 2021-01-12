#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 08:59:20 2021

@author: raphael
"""
# %% Imports
import csv
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

# Set environment variables
# os.environ['SPOTIPY_CLIENT_ID'] = 'app_spotify_client_id'
# os.environ['SPOTIPY_CLIENT_SECRET'] = 'app_spotify_client_secret'

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

country_list = ['france', 'bresil', 'allemagne', 'royaume-uni', 'espagne', 'italie', 'chili', 'colombie',
                'suisse', 'bolivie', 'autriche', 'belgique', 'equateur', 'danemark', 'republique_tcheque', 'paraguay']

# country = 'france'
for country in country_list:
    csv_array = np.loadtxt('top_' + country + '_200_spotify.csv', delimiter=",", dtype=object)
    spotify_dict = {}
    for position_i in range(1, 201):
        for date_j in range(1, 367):
            track_id = csv_array[position_i, date_j]
            if (spotify_dict.get(track_id) == None):
                spotify_dict[track_id] = sp.audio_features(track_id)
    
with open('top_200_af_spotify.csv', mode='w', newline='') as csv_spotify_af:
    fieldnames = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms', 'time_signature']
    writer = csv.DictWriter(csv_spotify_af, fieldnames=fieldnames)
    
    writer.writeheader()
    for track_af in spotify_dict.values():
        if track_af[0] != None:
            writer.writerow(track_af[0])


