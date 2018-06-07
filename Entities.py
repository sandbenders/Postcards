import pandas as pd
import geopy.distance
import random
import numpy as np


class Entities():
    def __init__(self, xlsx_file='data/citiesLatLgn.xlsx'):
        super().__init__()

        self.entities_cities = self.random_cities(xlsx_file)

        # print the entities
        for entity in self.entities_cities:
            print(entity)

    def random_cities(self, file):
        output = []
        # read csv and assign cities
        excel_file = pd.read_excel(file)
        entities = ["postman",
                    "flaubert",
                    "elizabeth",
                    "robert"]

        # generate the entities
        for entity in entities:
            random_sample = excel_file.sample()

            latlgn = (random_sample.latitude.mean(),
                      random_sample.longitude.mean())

            data_entity = {
                entity: {
                    "country": random_sample.country.all(),
                    "city": random_sample.city.all(),
                    "latlgn": latlgn
                }
            }

            print(entity)

            # postman
            if entity == entities[0]:
                postman_latlgn = latlgn
            # flaubert, elizabeth and robert
            else:
                choose_recipient = entity
                while choose_recipient == entity or choose_recipient == entities[0]:
                    choose_recipient = random.choice(entities)
                data_entity[entity]['distance'] = geopy.distance.vincenty(postman_latlgn, latlgn).km
                data_entity[entity]['recipient'] = choose_recipient
                data_entity[entity]['color'] = list(np.random.randint(0, 255, size=3))

            output.append(data_entity)

        return output
