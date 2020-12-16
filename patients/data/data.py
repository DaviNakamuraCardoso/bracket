def main(): 
    get_drugs()
    get_allergies()
    get_conditions()
    return 


def get_drugs():
    print("Opening drugs file...")
    file_obj = open('drugs.txt', 'r')
    text = file_obj.readlines()
    file_obj.close()

    array = []
    for line in text: 
        words = line.split()
        drug_list = []
        for word in words: 
            if word == "TRUE" or word == "FALSE": 
                break 
            else: 
                drug_list.append(word)

        drug = " ".join(drug_list)
        array.append(drug)
        print(f"Writing {drug}...")
    
    
    result_file = open('drugs.py', 'w')
    print("Writing results...")
    result_file.write('drugs = ' + str(array))
    result_file.close()
    print("Done.")

    
def get_allergies(): 
    file_obj = open('allergies.txt')
    text = file_obj.readlines()
    file_obj.close()
    allergies = []
    for line in text: 
        line = line.strip('\n')
        allergies.append(line)

    allergies.sort()
    python_file = open('allergies.py', 'w')
    python_file.write('allergies = ' + str(allergies))
    python_file.close()

        
def get_conditions(): 
    file_obj = open('conditions.txt')
    text = file_obj.readlines()

    conditions = []
    for line in text: 
        line = line.strip('\n')

        conditions.append(line)

    conditions.sort()

    python_file = open('conditions.py', 'w')
    python_file.write('conditions = ' + str(conditions))
    python_file.close()


    


    

        



if __name__ == '__main__': 
    main()
