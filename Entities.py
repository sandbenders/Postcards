import pandas as pd
import geopy.distance


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

            # postman
            if entity == entities[0]:
                postman_latlgn = (random_sample.latitude.mean(),
                                  random_sample.longitude.mean())
                data_entity = {
                    entity: {
                        "country": random_sample.country.all(),
                        "city": random_sample.city.all(),
                        "latlgn": postman_latlgn
                    }
                }
            else:
                # flaubert, elizabeth and robert
                latlgn = (random_sample.latitude.mean(),
                          random_sample.longitude.mean())
                data_entity = {
                    entity: {
                        "country": random_sample.country.all(),
                        "city": random_sample.city.all(),
                        "latlgn": latlgn,
                        "distance": geopy.distance.vincenty(postman_latlgn, latlgn).km
                    }
                }

            output.append(data_entity)

        return output
