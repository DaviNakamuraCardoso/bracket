document.addEventListener('DOMContentLoaded', () => 
{
    // Allergies
    const allergiesArray = [];
    const allergies = document.querySelector("#allergies");
    const allergiesList = document.querySelector("#list");
    
    allergies.onkeyup = function(event) 
    {
        listChoices(event, allergiesArray, allergies, allergiesList);
    }

    // Conditions
    const conditionsArray = [];
    const conditions = document.querySelector("#conditions");
    const conditionsList = document.querySelector("#list2");
     
    conditions.onkeyup = function(event)
    {
        listChoices(event, conditionsArray, conditions, conditionsList);
    }

    // Medications
    const medicationsArray = [];
    const medications = document.querySelector("#medications");
    const medicationsList = document.querySelector("#list3");

    medications.onkeyup = function(event)
    {
        listChoices(event, medicationsArray, medications, medicationsList);
    }
    
    // Keeping track of conditions
    //const conditions = document.querySelector("id");
    
    const form = document.querySelector('form');
    form.onsubmit = () => 
    {
        allergies.value = allergiesArray.join();
        conditions.value = conditionsArray.join();
        medications.value = medicationsArray.join();
        
        return true;
    }

});



function listChoices(event, array, field, list)
{
     
    if (event.key == 'Enter') 
    {
        // Adding the allergy value to the list 
        array.push(field.value);

        // Creating an li element to show the allergy
        const li = document.createElement('li');
        const btn = document.createElement('button');
        const val = document.createElement('span');

        val.innerHTML = field.value;
        btn.innerHTML = 'x';

        btn.addEventListener('click', () => {

            // Deletes the list element when clicked 
            const element = btn.parentElement;
            const v = element.firstChild;
            const index = array.indexOf(v.innerHTML);
            
            array.splice(index, 1);
            element.remove();
        });


        // Adding the allergy to the list
        li.append(val);
        li.append(btn);
        list.append(li);
        // Reset the textarea value
        field.value = '';

    }

    
}