#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 08:59:20 2021

@author: raphael
"""
# %% Imports
import csv
import numpy as np

country_list = ['france', 'bresil', 'allemagne', 'royaume-uni', 'espagne', 'italie', 'chili', 'colombie',
                'suisse', 'bolivie', 'autriche', 'belgique', 'equateur', 'danemark', 'republique_tcheque', 'paraguay']

country = 'france'

csv_array = np.loadtxt('top_' + country + '_200_spotify.csv', delimiter=",", dtype=object)

# with open('top_' + country + '_200_spotify.csv', mode='rb') as spotify_csv:
#         spotify_reader = csv.reader(
#             spotify_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#         for row in spotify_reader:
#             print(', '.join(row))