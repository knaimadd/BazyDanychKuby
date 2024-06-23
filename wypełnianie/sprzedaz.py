import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import scipy.stats as stats

# work in progress...

def get_price(make, model, engine_capacity, ):

    weights = data[(data['make'] == make) & (data['model'] == model)]
    weights = weights.value_counts('price', normalize=True)

    return rng.choice(np.array(weights.index)*4, p=weights)


def get_installments():

    installments = np.array((1, 6, 12, 18))
    weights = np.array(0.4, 0.3, 0.2, 0.1)
    return rng.choice(installments, p=weights)


if __name__ == '__main__':

    data = pd.read_csv(os.path.dirname(__file__) + '/inputs/samochody.csv')
    rng = np.random.default_rng()

    
    