import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import scipy.stats as stats

def get_data_parts():
    data_parts = pd.read_csv(os.path.dirname(__file__) + '/inputs/czesci_pl.csv')
    return data_parts
