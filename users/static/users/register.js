document.addEventListener('DOMContentLoaded', () => 
{
    const title = document.querySelector("#title");

    if (title.innerHTML == 'Patient')
    {
        registerPatient();
        console.log("patient it is");
    }
    else if (title.innerHTML == 'Doctor')
    {
        registerDoctor();
    }
    

});



function listChoices(array, field, list)
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

function registerPatient()
{
    // Allergies
    let allergiesArray = [];
    const allergiesInput = document.querySelector("#id_temp_allergies");
    const allergies = document.querySelector("#allergies");
    const allergiesList = document.querySelector("#id_temp_allergies_ul");
    
    allergiesInput.onchange = function() 
    {
        listChoices(allergiesArray, allergiesInput, allergiesList);
    }

    // Conditions
    
    let conditionsArray = [];
    const conditions = document.querySelector("#conditions");
    const conditionsInput = document.querySelector("#id_temp_conditions");
    const conditionsList = document.querySelector("#id_temp_conditions_ul");
     
    conditionsInput.onchange = function()
    {
        listChoices(conditionsArray, conditionsInput, conditionsList);
    }

    // Medications
    let medicationsArray = [];
    const medicationsInput = document.querySelector("#id_temp_medications");
    const medications = document.querySelector("#medications");
    const medicationsList = document.querySelector("#id_temp_medications_ul");

    medicationsInput.onchange = function()
    {
        listChoices(medicationsArray, medicationsInput, medicationsList);
    }
    
    
    const form = document.querySelector('form');
    form.onsubmit = () => 
    {
        allergies.value = allergiesArray.join();
        conditions.value = conditionsArray.join();
        medications.value = medicationsArray.join();
        
        return true;
    }
}


function registerDoctor()
{
    const areas = document.querySelector("#areas");
    let areasArray = [];
    const areasList = document.querySelector("#list");
    const areasInput = document.querySelector("#id_temp_areas");
    areas.style.display = 'none';

    areasInput.onchange = (event) => 
    {
        listChoices(event, areasArray, areasInput, areasList);

    }

    const form = document.querySelector("form");
    form.onsubmit = () => 
    {
        areas.value = areasArray.join();
        return true;
    }
    

}