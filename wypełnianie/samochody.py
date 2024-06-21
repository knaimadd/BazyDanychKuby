import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import scipy.stats as stats

#https://www.kaggle.com/datasets/ander289386/cars-germany?resource=download&SSORegistrationToken=CfDJ8CHCUm6ypKVLpjizcZHPE71bepU_g-gOSWMMBfpILdhkVvNxYBLLHBkEde9SvmJI5F9CbwU3nn8zJqgAKsaekpJXb0TTeheMUpM52uNoG0CMdIPGNa_SPqtc3gGcs78vgM2xfuQpPgRUL4PI0MH-toeVff2WR5AKx5oSe-nnNTR3KtSXPmK5A8lzXNbPbFVy_14hkRXEDwOjbr3UrOenAsO9PRpLhikLr1E9smfQtyDeYkJfqevywPF6CbwB3L-sgThk-AtFGqzaokWL7c-RI2T85KdAbNqf3idFlkk_s9fNiMmuxNkmCMJcCZDKP6EYFpMg-7nM78GYcqQT6JBZRlbV6ZJiAA&DisplayName=Oskar%20Matysik&messageId=invalidEmail&field=Email

def get_car_weights():

    n = len(data)
    weights = data.value_counts(['make', 'model'], normalize=True)
    make = np.array([weights.index[i][0] for i in range(len(weights))])
    model = np.array([weights.index[i][1] for i in range(len(weights))])
    #weights[0] = 1 - sum(weights[1:])
    return make, model, weights.to_numpy()


def get_year(min_year = 1993, max_year = 2023):

    year = np.floor(np.random.normal((min_year+max_year)/2, 4.5)).astype(int)
    year = min(max_year, year)
    year = max(min_year, year)
    return year


def get_gear(make, model):

    weights = data[(data['make'] == make) & (data['model'] == model)]
    weights = weights.value_counts('gear', normalize=True)
    return rng.choice(np.array(weights.index), p=weights)


def get_fuel(make, model):

    weights = data[(data['make'] == make) & (data['model'] == model)]
    weights = weights.value_counts('fuel', normalize=True)
    return rng.choice(np.array(weights.index), p=weights)


def get_post_accident(accident_prob = 0.2):

    return rng.random() < accident_prob


def get_hp(make, model):

    weights = data[(data['make'] == make) & (data['model'] == model)]
    weights = weights.value_counts('hp', normalize=True)
    return rng.choice(np.array(weights.index), p=weights)


def get_color():

    colors = np.array(('czarny', 'biały', 'szary', 'srebrny', 'niebieski', 'czerwony', 'brązowy', 'złoty', 'żółty', 'inny'))
    weights = np.array((0.22, 0.19, 0.18, 0.15, 0.10, 0.09, 0.03, 0.02, 0.01, 0.01))
    return rng.choice(colors, p=weights)


def get_body_type():

    types = np.array(('SUV', 'Hatchback', 'Sedan', 'Kombi', 'Coupe', 'Van', 'Minivan', 'Kabriolet'))
    weights = np.array((0.25, 0.25, 0.23, 0.17, 0.06, 0.03, 0.009, 0.001))
    return rng.choice(types, p=weights)


def get_engine_capacity(hp):

    random_factor = np.floor(rng.normal(0, 1)).astype(int)/10
    return max(0.6, round(hp * 16 / 1000 + random_factor, 1))


def get_doors(door_prob = 0.25):

    return 3 if rng.random() < door_prob else 5


def create_car():

    make_list, model_list, car_weights = get_car_weights()

    index = rng.choice(len(make_list), p=car_weights)
    make, model = make_list[index], model_list[index]
    year = get_year()
    gear = get_gear(make, model)
    fuel = get_fuel(make, model)
    post_accident = get_post_accident()
    hp = get_hp(make, model)
    color = get_color()
    body_type = get_body_type()
    engine_capacity = get_engine_capacity(hp)
    doors = get_doors()
    available = True
    value = 1000
    
    return [make, model, 4, year, body_type, post_accident, color, fuel, engine_capacity, gear, doors, available, value]


def create_table(n):
    
    df = pd.DataFrame(columns=['marka','model','liczba_kół', 'rok_produkcji', 'typ_nadwozia','czy_powypadkowy','kolor','typ_paliwa', 'pojemość_silnika', 'skrzynia_biegów', 'liczba_drzwi', 'czy_dostępny', 'wartość'])
    for i in range(n):
        row = create_car()
        df.loc[i] = row
    return df

if __name__ == '__main__':
    
    rng = np.random.default_rng()
    data = pd.read_csv(os.path.dirname(__file__) + '/inputs/samochody.csv')

    print(create_table(50))




    
    #weights = get_car_model(data)
    #print(weights.keys())