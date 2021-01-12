# -*- coding: utf-8 -*-
# %% Imports
import requests
import csv
import datetime
import numpy as np

country_list = ['espagne', 'italie', 'chili', 'colombie',
                'suisse', 'bolivie', 'autriche', 'belgique', 'equateur', 'danemark', 'republique_tcheque', 'paraguay']
country_code_list = ['es', 'it', 'cl', 'co',
                     'ch', 'bo', 'at', 'be', 'ec', 'dk', 'cz', 'py']
# country = 'espagne'
# country_code = 'es'

for country_i, country_code in enumerate(country_code_list):
    country = country_list[country_i]

    csv_array = np.zeros((201, 367), dtype=object)

    start_date = datetime.datetime(2020, 1, 1)
    date_generated = [(start_date + datetime.timedelta(days=d)
                       ).strftime("%Y-%m-%d") for d in range(366)]
    csv_array[0] = ["Position"] + date_generated
    csv_array[1:, 0] = [str(position) for position in range(1, 201)]

    for i, date in enumerate(date_generated):
        url = 'https://spotifycharts.com/regional/' + \
            country_code + '/daily/' + date + '/download'
        r = requests.get(url)
        top200 = r.text.split("\n")
        top200 = top200[2:202]
        top200_id = [track.split("/")[-1] for track in top200]
        csv_array[1:, i+1] = top200_id

    with open('top_' + country + '_200_spotify.csv', mode='w') as spotify_csv:
        spotify_writer = csv.writer(
            spotify_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        spotify_writer.writerows(csv_array)
