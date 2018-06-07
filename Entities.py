import pandas as pd
import geopy.distance
import random
import numpy as np


class Entities():
    def __init__(self, xlsx_file='data/citiesLatLgn.xlsx'):
        super().__init__()
        self.xlsx_file = xlsx_file

    def random_cities(self):
        data_entity = dict()
        # read csv and assign cities
        excel_file = pd.read_excel(self.xlsx_file)

        entities = ['postman',
                    'flaubert',
                    'elizabeth',
                    'robert']

        random_sample = excel_file.sample()
        postman_latlgn = (random_sample.latitude.mean(),
                          random_sample.longitude.mean())

        # generate the entities
        for i in range(0, 4):
            random_sample = excel_file.sample()

            latlgn = (random_sample.latitude.mean(),
                      random_sample.longitude.mean())

            if i != 0:
                choose_recipient = i
                while choose_recipient == i:
                    choose_recipient = random.randint(1, 3)
            else:
                choose_recipient = 0

            data_entity[i] = {
                'entity': entities[i],
                'country': random_sample.country.all(),
                'city': random_sample.city.all(),
                'latlgn': latlgn if i != 0 else postman_latlgn,
                'distance': geopy.distance.vincenty(postman_latlgn, latlgn).km,
                'recipient': choose_recipient,
                'hit': {
                    'iteration': 0 if i == 0 else 512,
                    'size': random.randint(10, 255)
                },
                'pos': {
                    'x': int(np.interp(latlgn[0], [-90, 90], [0, 1920])),
                    'y': int(np.interp(latlgn[1], [-180, 180], [0, 1080]))
                },
                'color': list(np.random.randint(0, 255, size=3)),

            }

        return data_entity
