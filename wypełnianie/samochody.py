import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import scipy.stats as stats

#https://www.kaggle.com/datasets/ander289386/cars-germany
#https://www.kaggle.com/datasets/nehalbirla/motorcycle-dataset

rng = np.random.default_rng()
data_car = pd.read_csv(os.path.dirname(__file__) + '/inputs/samochody.csv')
data_bike = pd.read_csv(os.path.dirname(__file__) + '/inputs/motocykle.csv')

def get_car_weights():

    n = len(data_car)
    weights = data_car.value_counts(['make', 'model'], normalize=True)
    make = np.array([weights.index[i][0] for i in range(len(weights))])
    model = np.array([weights.index[i][1] for i in range(len(weights))])
    return make, model, weights.to_numpy()


def get_bike_weights():

    n = len(data_bike)
    weights = data_bike.value_counts(['marka', 'model'], normalize=True)
    make = np.array([weights.index[i][0] for i in range(len(weights))])
    model = np.array([weights.index[i][1] for i in range(len(weights))])
    return make, model, weights.to_numpy()


def get_year(min_year = 1993, max_year = 2023):

    year = np.floor(np.random.normal((min_year+max_year)/2, 4.5)).astype(int)
    year = min(max_year, year)
    year = max(min_year, year)
    return year


def get_gear(weights, is_car):

    if is_car:
        weights = weights.value_counts('gear', normalize=True)
        return rng.choice(np.array(weights.index), p=weights)
    else:
        return 'Automatyczna' if rng.random() < 0.25 else 'Manualna'


def get_fuel(weights, is_car):

    if is_car:
        weights = weights.value_counts('fuel', normalize=True)
        return rng.choice(np.array(weights.index), p=weights)
    else:
        return 'Benzyna'


def get_post_accident(accident_prob = 0.15):

    return rng.random() < accident_prob


def get_hp(weights, is_car):
    if is_car:
        weights = weights.value_counts('hp', normalize=True)
        return rng.choice(np.array(weights.index), p=weights)
    else:
        return np.floor(rng.uniform(15, 120)).astype(int)


def get_color(colors, weights):

    return rng.choice(colors, p=weights)


def get_body_type(body_types, weights, is_car):
    if is_car:
        return rng.choice(body_types, p=weights)
    else:
        return ''


def get_engine_capacity(hp, is_car):
    if is_car:
        random_factor = np.floor(rng.normal(0, 1)).astype(int)/10
        return max(0.6, round(hp * 16 / 1000 + random_factor, 1))
    else:
        random_factor = np.floor(rng.normal(0, 1)).astype(int)/100
        return max(0.05, round(hp * 7 / 1000 + random_factor, 1))


def get_doors(is_car, door_prob = 0.25):
    if is_car:
        return 3 if rng.random() < door_prob else 5
    else:
        return 0
    

def get_num_of_seats(is_car, seat_prob = 0.25):
    if is_car:
        u = rng.random()
        if u < 0.01:
            return 7
        elif u > 0.25:
            return 5
        else:
            return 2
    else:
        return 1
    

def get_car_data():
    data_car = pd.read_csv(os.path.dirname(__file__) + '/inputs/samochody.csv')
    data_bike = pd.read_csv(os.path.dirname(__file__) + '/inputs/motocykle.csv')
    return data_car, data_bike

# def create_car():

#     is_car = rng.random() < 0.5
#     colors = np.array(('czarny', 'biały', 'szary', 'srebrny', 'niebieski', 'czerwony', 'brązowy', 'złoty', 'żółty', 'inny'))
#     colors_weights = np.array((0.22, 0.19, 0.18, 0.15, 0.10, 0.09, 0.03, 0.02, 0.01, 0.01))

#     if is_car:
#         index = rng.choice(len(make_list_car), p=car_weights)
#         make, model = make_list_car[index], model_list_car[index]
#         weights = data_car[(data_car['make'] == make) & (data_car['model'] == model)]
#         body = np.array(('SUV', 'Hatchback', 'Sedan', 'Kombi', 'Coupe', 'Van', 'Minivan', 'Kabriolet'))
#         body_weights = np.array((0.25, 0.25, 0.23, 0.17, 0.06, 0.03, 0.009, 0.001))
#     else:
#         index = rng.choice(len(make_list_bike), p=bike_weights)
#         make, model = make_list_bike[index], model_list_bike[index]
#         weights = False
#         body = False
#         body_weights = False

#     wheels = 4 if is_car else 2
#     year = get_year()
#     gear = get_gear(weights, is_car)
#     fuel = get_fuel(weights, is_car)
#     post_accident = get_post_accident()
#     hp = get_hp(weights, is_car)
#     color = get_color(colors, colors_weights)
#     body_type = get_body_type(body, body_weights, is_car)
#     engine_capacity = get_engine_capacity(hp, is_car)
#     doors = get_doors(is_car)
#     seats = get_num_of_seats(is_car)
#     available = get_availability()
    
#     return [make, model, wheels, year, body_type, post_accident, color, fuel, engine_capacity, gear, doors, available]


# def create_table(n):
    
#     df = pd.DataFrame(columns=['marka', 'model', 'liczba_kół', 'rok_produkcji', 'typ_nadwozia', 'czy_powypadkowy', 'kolor', 'typ_paliwa', 'pojemość_silnika', 'skrzynia_biegów', 'liczba_drzwi', 'czy_dostępny'])
#     for i in range(n):
#         row = create_car()
#         df.loc[i] = row
#     return df


# if __name__ == '__main__':
#     make_list_car, model_list_car, car_weights = get_car_weights()
#     make_list_bike, model_list_bike, bike_weights = get_bike_weights()

#     print(create_table(20))
