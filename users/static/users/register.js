document.addEventListener('DOMContentLoaded', () => 
{
    const title = document.querySelector("#title");

    if (title.innerHTML == 'Patient')
    {
        registerPatient();
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

    // Reset the field value
    field.value = '';
}


function registerPatient()
{

    // Allergies 
    watchSelection('allergies');

    // Medications 
    watchSelection('medications');

    // Conditions 
    watchSelection('conditions');

}


function registerDoctor()
{
    // Areas 
    watchSelection("areas");
}

function watchSelection(id)
{
    // Getting the essential elements 
    let array = [];
    const element = document.querySelector(`#${id}`);
    const elementInput = document.querySelector(`#id_temp_${id}`);
    const elementList = document.querySelector(`#id_temp_${id}_ul`);
    const form = document.querySelector('form');

    elementInput.onchange = function() 
    {
        listChoices(array, elementInput, elementList);
    }

    form.addEventListener("submit", () => 
    {
        element.value = array.join();
    });
}

        
    