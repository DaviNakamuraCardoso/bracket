import csv 
import pprint
from cities import cities
from sorted_cities import latitude_sorted


def main(): 
    #create_py('csv/uscities.csv')
    #update_cities('csv/municipios.csv')
    pprint.pprint(cities)


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
            states[state['\ufeffcodigo_uf']] = {'id': state['uf'], 'state':state['nome']}
    
        for city in br_cities: 
            
            cities.append({
                'city': city['nome'], 
                'state_id': states[city['codigo_uf']]['id'], 
                'state': states[city['codigo_uf']]['id'], 
                'lat': float(city['latitude']), 
                'lng': float(city['longitude']), 
                'timezone': "Not available" 
            })
        
        py_file = open('cities.py', 'w')

        py_file.write(f"cities = {pprint.pformat(cities)}")

        py_file.close()

    return 


if __name__ == '__main__': 
    main()


        