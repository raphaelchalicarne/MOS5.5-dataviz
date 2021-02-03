#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 16:13:54 2021

@author: raphael
"""

# %% Imports
import csv
import numpy as np
import time
import os

# %%
country_list = ["france", "belgique", "suisse", "autriche", "allemagne", "danemark", "republique_tcheque",
                "royaume-uni", "italie", "espagne", "argentine", "bolivie", "bresil", "chili", "colombie", "equateur", "paraguay"]
nb_countries = len(country_list)

# Load top 200 of each country
top_countries = np.empty((nb_countries, 201, 367), dtype=object)
for i_country, country in enumerate(country_list):
    top_countries[i_country] = np.loadtxt(
        'top_' + country + '_200_spotify.csv', delimiter=",", dtype=object)

# Calculate number of common tracks per day and country
nb_common_tracks = np.empty((366, nb_countries, nb_countries), dtype=int)
nb_common_tracks_flat = np.empty((366, nb_countries*nb_countries), dtype=int)

for date_index in range(366):
    for i_country, country_1 in enumerate(country_list):
        for j_country, country_2 in enumerate(country_list):
            if j_country < i_country:
                nb_common_tracks[date_index, i_country,
                                 j_country] = nb_common_tracks[date_index, j_country, i_country]
            elif j_country == i_country:
                nb_common_tracks[date_index, i_country, j_country] = 200
            else:
                country_1_date_tracks = top_countries[i_country,
                                                      1:, date_index + 1]
                country_2_date_tracks = top_countries[j_country,
                                                      1:, date_index + 1]
                common_tracks = np.intersect1d(
                    country_1_date_tracks, country_2_date_tracks)
                nb_common_tracks_day = len(common_tracks)

                nb_common_tracks[date_index, i_country,
                                 j_country] = nb_common_tracks_day

    nb_common_tracks_flat[date_index] = nb_common_tracks[date_index].ravel()

with open('nb_common_tracks.csv', mode='w') as common_tracks_csv:
    common_tracks_writer = csv.writer(
        common_tracks_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    common_tracks_writer.writerows(nb_common_tracks_flat)
