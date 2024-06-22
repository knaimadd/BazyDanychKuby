import faker.providers
import faker.providers.phone_number
import numpy as np
import pandas as pd
import os
import timeit
import string
from unidecode import unidecode

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


# Miasta

cities = pd.read_excel(os.path.dirname(__file__) + "/inputs/miasta_ludnosc.xlsx", sheet_name = "tabl. 22")
# partisioning data based no voivoidship
voi_partision = np.where(cities.iloc()[:,5].isna())[0][1:]
voi_partision = [(voi_partision[i], voi_partision[i+1]) for i in range(len(voi_partision)-1)]
voi_partision.append((voi_partision[-1][1], len(cities.iloc()[:,5])))

pop_in_cities = [cities.iloc()[:,5][voi_partision[i][0]+1:voi_partision[i][1]].array for i in range(len(voi_partision))] # number of peaople per city per voivoidship
sum_pop_in_cities = [np.sum(pop) for pop in pop_in_cities] # sum of people per voivoidship
prob_in_cities = [pop_in_cities[i]/sum_pop_in_cities[i] for i in range(len(pop_in_cities))] # normalized probability of getting a person from city per voivoidship
cities_in_voi = [cities.iloc()[:,1][voi_partision[i][0]+1:voi_partision[i][1]].values for i in range(len(voi_partision))] # names of cities per voivoidship

voi_probability = np.array([5, 3, 1, 4, 3, 2, 2, 4, 1, 1, 3, 3, 2, 2, 4, 3]) # how likely to get city form this voivoidship (based on location to dolnośląskie) 
voi_probability = voi_probability/np.sum(voi_probability)

def random_city():
    voi = np.random.choice(np.arange(0, 16), p = voi_probability)
    return np.random.choice(cities_in_voi[voi], p = prob_in_cities[voi])


# Ulice

# Probably will have to save this to some file, because its quite slow (few seconds) (done)
"""streets = pd.read_csv(os.path.dirname(__file__) + "/inputs/ulica.csv", delimiter=";")
can_live = np.where(streets["CECHA"].isin(["ul.", "pl.", "al."]))[0]
addresses = np.array([(streets["CECHA"].iloc()[can_live[i]] + " " +
             str(streets["NAZWA_2"].iloc()[can_live[i]]) + " " +
             streets["NAZWA_1"].iloc()[can_live[i]]).replace(" nan ", " ") for i in range(len(can_live))])
adresses_df = pd.DataFrame({"address": addresses})
adresses_df.to_csv(os.path.dirname(__file__) + '/inputs/adresy.csv')"""

addresses = pd.read_csv(os.path.dirname(__file__) + '/inputs/adresy.csv')["address"].values


def random_street():
    return np.random.choice(addresses)

used_phone_list = []

def random_phone():
    if np.random.rand() <= 0.002:
        country_code = str(np.random.randint(1, 999))
        phone_number = ""
        for i in range(np.random.randint(8, 13)):
            phone_number += str(np.random.randint(10))
    else:
        country_code = "48"
        phone_number = str(np.random.randint(1000000000, 1999999999))[1:]

    phone = country_code + phone_number
    if phone in used_phone_list:
        return random_phone()
    else:
        used_phone_list.append(phone)
        return phone
    
domains = np.array(["gmail.com", "wp.pl", "onet.pl", "interia.pl", "opayq.com", "yahoo.com", "outlook.com", "vp.pl", "protonmail.com", "o2.pl", "gazeta.pl", 'int.pl'])
domain_weights = np.array([36, 22, 13, 9, 0.1, 1, 3, 4, 2, 10, 2, 0.5])
domain_weights = domain_weights/np.sum(domain_weights)

def random_email(first_name, last_name):
    first_name = unidecode(first_name.lower())
    last_name = unidecode(last_name.lower())
    b = np.random.rand()
    num = ""
    if b <= 0.5:
        num = str(np.random.randint(9999))

    p = np.random.randint(6)
    domain = np.random.choice(domains, p=domain_weights)
    symbol = np.random.choice(np.array([".", "-", "_", ""]))
    if p == 0:
        return first_name[0] + symbol + last_name + num + "@" + domain
    if p == 1:
        return first_name[:3] + symbol + last_name[:min(len(last_name) - 1, np.random.randint(1,10))] + num + "@" + domain
    if p == 2:
        return first_name[0] + symbol + last_name[:min(len(last_name) - 1, np.random.randint(1,10))] + num + "@" + domain
    if p == 3:
        return last_name + num + str(np.random.randint(10)) + "@" + domain
    if p == 4: 
        random_ascii = np.random.choice(list(string.ascii_lowercase), np.random.randint(4, 10)).tolist()
        random_nums = np.random.choice([str(i) for i in range(10)], np.random.randint(1, 10)).tolist()
        random_string = np.array(random_ascii + random_nums)
        np.random.shuffle(random_string[1:])
        r = np.random.randint(2)
        return ["".join(random_string) + "@opayq.com", "".join(random_string) + "@" + domain][r]
    if p == 5:
        return last_name[:min(len(last_name) - 1, np.random.randint(10))] + symbol + first_name[:min(len(last_name) - 1, np.random.randint(10))] + num + "@" + domain


if __name__ == "__main__":
    mname = random_name_man()
    print(f"\nrandom man name: {mname}")
    print(f"random email: {random_email(mname[0], mname[1])}")
    pdm = random_pesel_date_man([1980, 2010])
    print(f"random man pesel and date: {pdm[0]}, {pdm[1]}")
    wname = random_name_woman()
    print(f"random woman name: {wname}")
    print(f"random email: {random_email(wname[0], wname[1])}")
    pdw = random_pesel_date_woman([1980, 2010])
    print(f"random woman pesel and date: {pdw[0]}, {pdw[1]}")
    print(f"random address: {random_city()}, {random_street()}")
    print(f"random phone number: {random_phone()}")
    
    t = timeit.Timer(random_name_man)
    print(f"\n1000 random names generated time: {t.timeit(number=1000)} [s]")
    tp = timeit.Timer(lambda: random_pesel_date_man([1980, 2010]))
    print(f"\n1000 random pesels and dates generated time: {tp.timeit(number=1000)} [s]")
    tc = timeit.Timer(random_city)
    ts = timeit.Timer(random_street)
    print(f"\n1000 random addresses generated time: {tc.timeit(number=1000) + ts.timeit(number=1000)} [s]")
    tn = timeit.Timer(random_phone)
    print(f"\n1000 random phone numbers generated time: {tn.timeit(number=1000)} [s]")
    te = timeit.Timer(lambda: random_email("Adrian", "Galik"))
    print(f"\n1000 random email generated time: {te.timeit(number=1000)} [s]")

    AG = person_probability("ADRIAN", "GALIK", "M")
    print(f"\nAdrian probabilit: {AG[0]}\nGalik probability: {AG[1]}\nAdrian Galik probability: {AG[2]}")

    TS = person_probability("TOMASZ", "STROIŃSKI", "M")
    print(f"\nTomasz probabilit: {TS[0]}\nStroiński probability: {TS[1]}\nTomasz Stroiński probability: {TS[2]}\n")
