import pandas as pd
import geopy.distance
import random
import numpy as np


class Entities():
    def __init__(self, xlsx_file='data/citiesLatLgn.xlsx'):
        super().__init__()
        self.xlsx_file = xlsx_file

    def random_cities(self):
        output = []
        # read csv and assign cities
        excel_file = pd.read_excel(self.xlsx_file)
        entities = ['postman',
                    'flaubert',
                    'elizabeth',
                    'robert']

        # generate the entities
        for entity in entities:
            random_sample = excel_file.sample()

            latlgn = (random_sample.latitude.mean(),
                      random_sample.longitude.mean())

            data_entity = dict()
            data_entity['entity'] = entity
            data_entity['country'] = random_sample.country.all()
            data_entity['city'] = random_sample.city.all()
            data_entity['latlgn'] = latlgn

            # postman
            if entity == entities[0]:
                postman_latlgn = latlgn
            # players
            else:
                choose_recipient = entity
                while choose_recipient == entity or choose_recipient == entities[0]:
                    choose_recipient = random.choice(entities)
                data_entity['distance'] = geopy.distance.vincenty(postman_latlgn, latlgn).km
                data_entity['recipient'] = choose_recipient

            hit = {
                'iteration': 0 if entity == entities[0] else 512,
                'size': random.randint(10, 255)
            }

            pos = {
                'x': int(np.interp(latlgn[0], [-90, 90], [0, 1920])),
                'y': int(np.interp(latlgn[1], [-180, 180], [0, 1080]))
            }

            data_entity['color'] = list(np.random.randint(0, 255, size=3))
            data_entity['hit'] = hit
            data_entity['pos'] = pos

            output.append(data_entity)

        return output
