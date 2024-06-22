import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import scipy.stats as stats
import translators as tsl

def to_polish():

    data = pd.read_csv(os.path.dirname(__file__) + '/inputs/czesci.csv').transpose().index.to_numpy()
    for i in range(len(data)):
        data[i] = tsl.translate_text(data[i], 'google', 'en', 'pl')
        print(i)
    pd.DataFrame(data).to_csv(os.path.dirname(__file__) + '/inputs/goofy_ahh_czesci.csv')

if __name__ == '__main__':
    czesci_data = pd.read_csv(os.path.dirname(__file__) + '/inputs/czesci_pl.csv')
    marka, model, kolor = 'Ford', 'Focus', 'Srebrny'