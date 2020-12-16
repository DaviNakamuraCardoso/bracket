def main(): 
    get_areas()
    return 


def get_areas(): 

    # Open the txt file and get an array 
    file_object = open('areas.txt', 'r')
    areas = file_object.readlines()
    areas = [area.strip('\n') for area in areas]

    # Close the file and sort the array 
    file_object.close()
    areas.sort()

    # Create a python file and write the array 
    python_file = open('areas.py', 'w')
    python_file.write('areas = ' + str(areas))

    # Close the file and return 
    python_file.close()
    return 


if __name__ == '__main__': 
    main()
