import csv 
from pprint import pformat 

def main(): 
    get_cities('uscities.csv')


def get_cities(filename): 
    cities = []
    with open(filename) as csvfile: 
        reader = csv.reader(csvfile)
        for row in reader: 
            cities_string = f"{row[0]}, {row[2]}"
            cities_tuple = (cities_string, cities_string)
            cities.append(cities_tuple)
    
    python_file = open('cities.py', 'w')
    python_file.write(f'cities = {pformat(cities)}')
            

if __name__ == '__main__': 
    main()
