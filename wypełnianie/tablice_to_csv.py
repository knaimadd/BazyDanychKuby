import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import scipy.stats as stats

data = pd.read_csv(os.path.dirname(__file__) + '/inputs/motocykle.xls')['name'].to_numpy()
data = [data[i].split(' ') for i in range(len(data))]
newdata = pd.DataFrame()
newdata['marka'] = [data[i][0] for i in range(len(data))]
newdata['model'] = [' '.join(data[i][1:]) for i in range(len(data))]
newdata.to_csv('motocykle.csv')