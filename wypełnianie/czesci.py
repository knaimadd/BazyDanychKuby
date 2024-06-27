import pandas as pd
import os

def get_data_parts():
    data_parts = pd.read_csv(os.path.dirname(__file__) + '/inputs/czesci_pl.csv')
    return data_parts
