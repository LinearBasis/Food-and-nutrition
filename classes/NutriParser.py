import pandas as pd
import numpy as np
import requests
import json

class NutruientParser:
    df = pd.read_csv("epi_r.csv")
    df_nutr_one = pd.read_csv("../../Nutrition-recommendations/data/Nutrients.csv")
    df_nutr_two = pd.read_csv("../../Nutrition-recommendations/data/food_components.csv")
    df_nutr = pd.concat([df_nutr_one, df_nutr_two], axis = 0, ignore_index=True)
    def __init__(self, product_name):
        self.product_name = product_name

        self.r = requests.get(
            f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key=O9O8y67XB59UcnngfKt1eP4yX7Vm0ro7N66HxQtm&query={product_name}", verify = False
        )
        self.json_data = self.r.json()

    def parse_product(self, name_of_micro):
        if self.json_data.get('foods') is None:
            return None
        for index in range(len(self.json_data["foods"])):
            num = 0
            tmp = 0
            for i in self.json_data["foods"][index]["foodNutrients"]:
                if name_of_micro in i["nutrientName"]:
                    num += 1
                    tmp += i['value']
        if num == 0:
            return 0
        return(tmp / num)

    def parse_nutricious_values_per_product(self):
        df = pd.Series(dtype=float)
        for name in df_nutr["Nutrient"]:
            mean = self.parse_product(name)
            if mean is None:
                return None
            df[name] = mean
        return(df)

# parser = NutruientParser("ab")
# parser.parse_nutricious_values_per_product()
