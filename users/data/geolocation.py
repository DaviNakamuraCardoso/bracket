from .sorted_cities import latitude_sorted
import pprint
import sys

LATITUDE_INDEX = 6
LONGITUDE_INDEX = 7


def sort_cities(array):
    by_x = sorted(array, key=lambda array: float(array[6])) 
    by_x_file = open('sorted_cities.py', 'w')
    by_x_file.write(f'latitude_sorted = {pprint.pformat(by_x)}\n')


def bs(n, array, start, end, index): 
    """Binary Search through an array, and returns the index of the closest element in value."""
    middle = round((start + end) / 2)

    if end == start: 
        return end  
    
    elif n > float(array[middle][index]): 
        return bs(n, array, middle+1, end, index)
    
    return bs(n, array, start, middle-1, index)


def locate(lat, lon, distance=0.5): 
    global latitude_sorted, LATITUDE_INDEX, LONGITUDE_INDEX

    l = len(latitude_sorted)
    try: 
        north = bs(lat+distance, latitude_sorted, 0, l, LATITUDE_INDEX)
    except RecursionError: 
        return locate(lat, lon, distance-0.2)
        
    try: 
        south = bs(lat-distance, latitude_sorted, 0, l, LATITUDE_INDEX)
    except RecursionError: 
        return locate(lat, lon, distance-0.2)

    arr = sorted(latitude_sorted[south:north], key=lambda array: float(array[7]))
    l = len(arr)
    try: 

        left = bs(lon-distance, arr, 0, l, LONGITUDE_INDEX)
    except RecursionError: 
        return locate(lat, lon, distance-0.2)

    try: 
        right = bs(lon+distance, arr, 0, l, LONGITUDE_INDEX)
    except RecursionError: 
        return locate(lat, lon, distance-0.2)

    final = sorted(arr[left:right], key=lambda array: ((float(array[LATITUDE_INDEX]) - lat)**2 + (float(array[LONGITUDE_INDEX]) - lon)**2))

    return final 


if __name__ == "__main__": 
    pprint.pprint(locate(40.69, -73.92, 0.5)[:10])

