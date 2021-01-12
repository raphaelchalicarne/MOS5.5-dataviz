#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 08:59:20 2021

@author: raphael
"""
# %% Imports
import csv
import numpy as np
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import spotify_client #Contient les ID client de Spotify

#%%
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


def get_artists(track_data):
    artist_list = [artist_dict['name']
                   for artist_dict in track_data['artists']]
    return ";".join(artist_list)


country_list = np.array(['france', 'bresil', 'allemagne', 'royaume-uni', 'espagne', 'italie', 'chili', 'colombie',
                         'suisse', 'bolivie', 'autriche', 'belgique', 'equateur', 'danemark', 'republique_tcheque', 'paraguay'])
country_unique_tracks = np.array([])


t0 = time.time()
for i_country, country in enumerate(country_list):
    csv_array = np.loadtxt(
        'top_' + country + '_200_spotify.csv', delimiter=",", dtype=object)
    country_unique_tracks = np.concatenate(
        (country_unique_tracks, np.unique(csv_array[1:, 1:])))
unique_tracks_list = np.unique(country_unique_tracks)
unique_tracks_list = unique_tracks_list[1:]
print("Temps de calcul unique_tracks_list :",
      "{0:.2f}".format(time.time()-t0), "secondes")

t1 = time.time()
spotify_dict = {}
for track_id in unique_tracks_list:
        if (spotify_dict.get(track_id) == None) & (track_id != ''):
            track_af = sp.audio_features(track_id)[0]
            if track_af != None:
                spotify_dict[track_id] = track_af

                track_data = sp.track(track_id)
                track_name = track_data['name']
                track_artists = get_artists(track_data)

                spotify_dict[track_id]['name'] = track_name
                spotify_dict[track_id]['artists'] = track_artists

print("Temps de calcul spotify_dict :",
      "{0:.2f}".format(time.time()-t1), "secondes")

with open('top_200_af_spotify.csv', mode='w', newline='') as csv_spotify_af:
    fieldnames = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
                  'valence', 'tempo', 'type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms', 'time_signature', 'name', 'artists']
    writer = csv.DictWriter(csv_spotify_af, fieldnames=fieldnames,
                            delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    writer.writeheader()
    for track_af in spotify_dict.values():
        if track_af != None:
            writer.writerow(track_af)


# %%
bo_track_id = '717QGTmZdkemDaCo1vQHG0'
bo_track_data = sp.track(bo_track_id)
get_artists(bo_track_data)

# %%
country = 'paraguay'
csv_array = np.loadtxt(
    'top_' + country + '_200_spotify.csv', delimiter=",", dtype=object)
tracks = np.unique(csv_array[1:, 1:])
