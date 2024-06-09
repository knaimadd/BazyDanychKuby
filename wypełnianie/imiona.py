import numpy as np
import pandas as pd
import os
import timeit

# Name

data_l_m = pd.read_csv(os.path.dirname(__file__) + "/inputs/nazwiska_meskie.csv")
last_names_m = data_l_m["Nazwisko aktualne"].to_numpy()
weights_l_m = data_l_m["Liczba"].to_numpy() 

weights_l_m = weights_l_m/np.sum(weights_l_m) # normalization (sum of all man is 20976785 so the date seems to be good)

data_f_m = pd.read_csv(os.path.dirname(__file__) + "/inputs/imiona_meskie.csv")
first_names_m = data_f_m["IMIĘ_PIERWSZE"].to_numpy()
weights_f_m = data_f_m["LICZBA_WYSTĄPIEŃ"].to_numpy()

weights_f_m = weights_f_m/np.sum(weights_f_m) # normalization (sum of all man is 21208298)

def random_name_man() -> tuple:
    return np.random.choice(first_names_m, p = weights_f_m).title(), np.random.choice(last_names_m, p = weights_l_m).title()

data_l_w = pd.read_csv(os.path.dirname(__file__) + "/inputs/nazwiska_zenskie.csv")
last_names_w = data_l_w["Nazwisko aktualne"].to_numpy()
weights_l_w = data_l_w["Liczba"].to_numpy() 

weights_l_w = weights_l_w/np.sum(weights_l_w) # normalization (sum of all woman is 21479386)

data_f_w = pd.read_csv(os.path.dirname(__file__) + "/inputs/imiona_zenskie.csv")
first_names_w = data_f_w["IMIĘ_PIERWSZE"].to_numpy()
weights_f_w = data_f_w["LICZBA_WYSTĄPIEŃ"].to_numpy()

weights_f_w = weights_f_w/np.sum(weights_f_w) # normalization (sum of all woman is 22465060)

def random_name_woman() -> tuple:   # seperate function for genders to not repeat ifs
    return np.random.choice(first_names_w, p = weights_f_w).title(), np.random.choice(last_names_w, p = weights_l_w).title()

def person_probability(first_name, last_name, gender) -> tuple:
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

# PESEL and date

dict_not_to_reapeat_man = {}

control_weights = np.array([1,3,7,9,1,3,7,9,1,3])

def control_number(number_str):
    number_arr = np.array([int(d) for d in number_str])
    return 10 - (np.dot(number_arr, control_weights) % 10)

def random_pesel_date_man(years_lims, date_format = "/"):
    year = np.random.randint(years_lims[0], years_lims[1]+1)
    year_no = str(year)[-2:]
    
    month = np.random.randint(12)
    if year <= 1999:
        month_no = str(np.arange(101, 113)[month])[1:] # 3 digits to easier and faster get 1 digit number to start with 0
    else:
        month_no = str(np.arange(21, 33)[month])
    
    if year % 4 == 0:
        days_in_months = np.array([31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
    else:
        days_in_months = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
    day_no = str(np.random.randint(101, days_in_months[month]+101))[-2:]

    pesel = year_no + month_no + day_no

    gender_ordinal = np.random.choice(np.arange(1, 10, 2))
    if year in dict_not_to_reapeat_man:
        rand_ordinal = np.random.choice(dict_not_to_reapeat_woman[year])
        dict_not_to_reapeat_man[pesel + str(gender_ordinal)].remove(rand_ordinal)
    else:
        new = np.arange(1000, 2000)
        rand_ordinal = np.random.choice(new)
        new = new.tolist()
        new.remove(rand_ordinal)
        dict_not_to_reapeat_man[pesel + str(gender_ordinal)] = new
    ordinal_no = str(rand_ordinal)[-3:] + str(gender_ordinal)

    pesel += ordinal_no
    pesel += str(control_number(pesel))
    return pesel, day_no + date_format + str(month+101)[-2:] + date_format + str(year)


dict_not_to_reapeat_woman = {}

def random_pesel_date_woman(years_lims, date_format = "/"):
    year = np.random.randint(years_lims[0], years_lims[1]+1)
    year_no = str(year)[-2:]
    
    month = np.random.randint(12)
    if year <= 1999:
        month_no = str(np.arange(101, 113)[month])[1:] # 3 digits to easier and faster get 1 digit number to start with 0
    else:
        month_no = str(np.arange(21, 33)[month])
    
    if year % 4 == 0:
        days_in_months = np.array([31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
    else:
        days_in_months = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
    day_no = str(np.random.randint(101, days_in_months[month]+101))[-2:]

    pesel = year_no + month_no + day_no

    gender_ordinal = np.random.choice(np.arange(0, 10, 2))
    if year in dict_not_to_reapeat_woman:
        rand_ordinal = np.random.choice(dict_not_to_reapeat_woman[year])
        dict_not_to_reapeat_woman[pesel + str(gender_ordinal)].remove(rand_ordinal)
    else:
        new = np.arange(1000, 2000)
        rand_ordinal = np.random.choice(new)
        new = new.tolist()
        new.remove(rand_ordinal)
        dict_not_to_reapeat_woman[pesel + str(gender_ordinal)] = new
    ordinal_no = str(rand_ordinal)[-3:] + str(gender_ordinal)

    pesel += ordinal_no
    pesel += str(control_number(pesel))
    return pesel, day_no + date_format + str(month+101)[-2:] + date_format + str(year)


    
if __name__ == "__main__":
    print(f"\nrandom man name: {random_name_man()}")
    pdm = random_pesel_date_man([1980, 2010])
    print(f"random man pesel and date: {pdm[0]}, {pdm[1]}")
    print(f"random woman name: {random_name_woman()}")
    pdw = random_pesel_date_woman([1980, 2010])
    print(f"random man pesel and date: {pdw[0]}, {pdw[1]}")
    
    t = timeit.Timer(random_name_man)
    print(f"\n1000 random names generated time: {t.timeit(number=1000)} [s]")
    tp = timeit.Timer(lambda: random_pesel_date_man([1980, 2010]))
    print(f"\n1000 random pesels and dates generated time: {tp.timeit(number=1000)} [s]")

    AG = person_probability("ADRIAN", "GALIK", "M")
    print(f"\nAdrian probabilit: {AG[0]}\nGalik probability: {AG[1]}\nAdrian Galik probability: {AG[2]}")

    TS = person_probability("TOMASZ", "STROIŃSKI", "M")
    print(f"\nTomasz probabilit: {TS[0]}\nStroiński probability: {TS[1]}\nTomasz Stroiński probability: {TS[2]}\n")   
