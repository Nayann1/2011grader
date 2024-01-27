from configparser import ConfigParser
import random

config = ConfigParser()
config.read("powset.n")

def generate_problem(min_value, max_value):
    firstval = random.randint(min_value, max_value)
    secondval = random.randint(min_value, max_value)
    return firstval, secondval

firstval, secondval = generate_problem(int(config['inputs']['min_value']), int(config['inputs']['max_value']))

output_format = config['inputs']['output_format'].format(first=firstval, second=secondval)



print(output_format)
