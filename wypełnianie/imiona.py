import numpy as np
import pandas as pd
import os

data_l_m = pd.read_csv(os.path.dirname(__file__) + "/inputs/nazwiska_meskie.csv")
last_names_m = data_l_m["Nazwisko aktualne"].to_numpy()
weights_l_m = data_l_m["Liczba"].to_numpy() 

weights_l_m = weights_l_m/np.sum(weights_l_m) # normalization (sum of all man is 20976785 so the date seems to be good)

data_f_m = pd.read_csv(os.path.dirname(__file__) + "/inputs/imiona_meskie.csv")
first_names_m = data_f_m["IMIĘ_PIERWSZE"].to_numpy()
weights_f_m = data_f_m["LICZBA_WYSTĄPIEŃ"].to_numpy()

weights_f_m = weights_f_m/np.sum(weights_f_m) # normalization (sum of all man is 21208298)

def random_man_name() -> tuple:
    return np.random.choice(first_names_m, p = weights_f_m).title(), np.random.choice(last_names_m, p = weights_l_m).title()

data_l_w = pd.read_csv(os.path.dirname(__file__) + "/inputs/nazwiska_zenskie.csv")
last_names_w = data_l_w["Nazwisko aktualne"].to_numpy()
weights_l_w = data_l_w["Liczba"].to_numpy() 

weights_l_w = weights_l_w/np.sum(weights_l_w) # normalization (sum of all woman is 21479386)

data_f_w = pd.read_csv(os.path.dirname(__file__) + "/inputs/imiona_zenskie.csv")
first_names_w = data_f_w["IMIĘ_PIERWSZE"].to_numpy()
weights_f_w = data_f_w["LICZBA_WYSTĄPIEŃ"].to_numpy()

weights_f_w = weights_f_w/np.sum(weights_f_w) # normalization (sum of all woman is 22465060)

def random_woman_name() -> tuple:
    return np.random.choice(first_names_w, p = weights_f_w).title(), np.random.choice(last_names_w, p = weights_l_w).title()

def person_probability(first_name, last_name, gender):
    if gender == "M":
        first_i = np.argmax(first_names_m == first_name)
        first_p = weights_f_m[first_i]
        last_i = np.argmax(last_names_m == last_name)
        last_p = weights_l_m[last_i]
    else:
        first_i = np.argmax(first_names_w == first_name)
        first_p = weights_f_w[first_i]
        last_i = np.argmax(last_names_w == last_name)
        last_p = weights_l_w[last_i]
    return first_p, last_p, first_p * last_p

if __name__ == "__main__":
    print(f"\nrandom man name: {random_man_name()}")
    print(f"random woman name: {random_woman_name()}")

    AG = person_probability("ADRIAN", "GALIK", "M")
    print(f"\nAdrian probabilit: {AG[0]}\nGalik probability: {AG[1]}\nAdrian Galik probability: {AG[2]}")

    TS = person_probability("TOMASZ", "STROIŃSKI", "M")
    print(f"\nTomasz probabilit: {TS[0]}\nStroiński probability: {TS[1]}\nTomasz Stroiński probability: {TS[2]}")   
