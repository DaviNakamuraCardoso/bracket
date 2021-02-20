import csv
import pprint
from cities import cities


def main():
    global cities
    #create_py('csv/uscities.csv')
    #update_cities('csv/municipios.csv')
    sort_cities(cities)


def create_py(filename):
    cities = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            cities.append({
                'city': row['city'],
                'state_id': row['state_id'],
                'state': row['state_name'],
                'lat': float(row['lat']),
                'lng': float(row['lng']),
                'timezone': row['timezone']
            })

        py_file = open('cities.py', 'w')

        py_file.write(f'cities = {pprint.pformat(cities)}')

        py_file.close()


def update_cities(filename):
    global cities

    with open(filename) as cities_file:

        br_cities = csv.DictReader(cities_file)
        states_file = open('csv/estados.csv')
        br_states = csv.DictReader(states_file)

        states = {}
        for state in br_states:
            states[state['\ufeffcodigo_uf']] = {'id': state['uf'], 'state':state['nome'], 'timezone': state['timezone']}

        for city in br_cities:

            cities.append({
                'city': city['nome'],
                'state_id': states[city['codigo_uf']]['id'],
                'state': states[city['codigo_uf']]['id'],
                'lat': float(city['latitude']),
                'lng': float(city['longitude']),
                'timezone': states[city['codigo_uf']]['timezone']
            })

        py_file = open('cities.py', 'w')

        py_file.write(f"cities = {pprint.pformat(cities)}")

        py_file.close()

    return


def sort_cities(array):
    by_x = sorted(array, key=lambda array: array['lat'])
    by_x_file = open('sorted_cities.py', 'w')
    by_x_file.write(f'latitude_sorted = {pprint.pformat(by_x)}\n')
    pprint.pprint(by_x)


if __name__ == '__main__':
    main()
