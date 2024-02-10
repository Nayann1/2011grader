import random
def random_unique(minmax, n=2):
    unique_values = random.sample(range(minmax[0], minmax[1] + 1), 2)
   
    return unique_values
