import pprint
import sys
from .sorted_cities import latitude_sorted
from .cities import cities


LATITUDE_INDEX = 'lat' 
LONGITUDE_INDEX = 'lng' 


def sort_cities(array):
    by_x = sorted(array, key=lambda array: array['lat']) 
    by_x_file = open('sorted_cities.py', 'w')
    by_x_file.write(f'latitude_sorted = {pprint.pformat(by_x)}\n')


def bs(n, array, start, end, index): 
    """Binary Search through an array, and returns the index of the closest element in value."""
    middle = round((start + end) / 2)

    if end == start: 
        return end  
    
    elif n > array[middle][index]: 
        return bs(n, array, middle+1, end, index)
    
    return bs(n, array, start, middle-1, index)


def locate(lat, lng, distance=0.5): 
    global latitude_sorted

    l = len(latitude_sorted)
    try: 
        north = bs(lat+distance, latitude_sorted, 0, l, 'lat')
    except RecursionError: 
        return locate(lat, lng, distance-0.1)
        
    try: 
        south = bs(lat-distance, latitude_sorted, 0, l, 'lat')
    except RecursionError: 
        return locate(lat, lng, distance-0.1)

    arr = sorted(latitude_sorted[south:north], key=lambda array: float(array['lng']))
    l = len(arr)
    try: 

        left = bs(lng-distance, arr, 0, l, 'lng')
    except RecursionError: 
        return locate(lat, lng, distance-0.1)

    try: 
        right = bs(lng+distance, arr, 0, l, 'lng')
    except RecursionError: 
        return locate(lat, lng, distance-0.1)

    final = sorted(arr[left:right], key=lambda array: ((array['lat'] - lat)**2 + (array['lng'] - lng)**2))

    return final 


if __name__ == "__main__": 
    sort_cities(cities)

