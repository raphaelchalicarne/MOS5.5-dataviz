#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 17:01:13 2021

@author: raphael
"""

#%% Imports 
import csv
import numpy as np
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import spotify_client  # Contient les ID client de Spotify

#%% Spotify credentials
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

#%% Functions
def get_artists(track_data):
    artist_list = [artist_dict['name']
                   for artist_dict in track_data['artists']]
    return ";".join(artist_list)

#%% Load tracks ID list we already have
top_200_af_array = np.loadtxt(
    'top_200_af_spotify.csv', delimiter=",", dtype=object, skiprows=1, usecols=(12))

#%% Load unique tracks ID list of Argentina
argentina_unique_tracks = np.array([])

t0 = time.time()
csv_array = np.loadtxt(
    'top_argentine_200_spotify.csv', delimiter=",", dtype=object)
argentina_unique_tracks = np.concatenate(
    (argentina_unique_tracks, np.unique(csv_array[1:, 1:])))
unique_tracks_list = np.unique(argentina_unique_tracks)
unique_tracks_list = unique_tracks_list[1:]
print("Temps de calcul unique_tracks_list :",
  "{0:.2f}".format(time.time()-t0), "secondes")

#%% Call to Spotify API about missing data
t1 = time.time()
spotify_dict = {}
for argentina_track_id in argentina_unique_tracks:
    if (argentina_track_id not in top_200_af_array):
        track_af = sp.audio_features(argentina_track_id)[0]
        if track_af != None:
            spotify_dict[argentina_track_id] = track_af

            track_data = sp.track(argentina_track_id)
            track_name = track_data['name']
            track_artists = get_artists(track_data)

            spotify_dict[argentina_track_id]['name'] = track_name
            spotify_dict[argentina_track_id]['artists'] = track_artists
            
print("Temps de calcul spotify_dict :",
      "{0:.2f}".format(time.time()-t1), "secondes")

#%% Write missing data in new CSV file
with open('top_200_argentine_af_spotify.csv', mode='w', newline='') as csv_spotify_af:
    fieldnames = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
                  'valence', 'tempo', 'type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms', 'time_signature', 'name', 'artists']
    writer = csv.DictWriter(csv_spotify_af, fieldnames=fieldnames,
                            delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    writer.writeheader()
    for track_af in spotify_dict.values():
        if track_af != None:
            writer.writerow(track_af)