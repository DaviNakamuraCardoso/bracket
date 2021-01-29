import csv 
from pprint import pformat 


def main(): 
    pass


def create_py(filename): 
    with open(filename) as csvfile: 
        reader = csv.reader(csvfile)
        cities = []

        for row in reader: 
            cities.append(row)
        
        py_file = open('cities.py', 'w')

        py_file.write(f'cities = {pformat(cities)}')

        py_file.close()


if __name__ == '__main__': 
    main()


        