document.addEventListener('DOMContentLoaded', () => 
{
    
    const userTypeSelect = document.querySelector("select");
    const form = document.querySelector("form");
    const next = document.querySelector("#next");
    const base = document.querySelector("#base");
    

    next.innerHTML = document.querySelector("#patient").innerHTML;
    base.innerHTML = copyElement(document.querySelector("#base-form")).innerHTML;

    updateChoices();
    validate();

    const relations = {
        "clinic": "clinic-base", 
        "patient": "base-form", 
        "doctor": "base-form"
    };

    userTypeSelect.onchange = () => {

        form.action = userTypeSelect.value;

        let text = userTypeSelect.options[userTypeSelect.selectedIndex].text;

        base.innerHTML = copyElement(document.getElementById(relations[text])).innerHTML;
        next.innerHTML = document.getElementById(text).innerHTML;
        updateChoices();

    }



});


function copyElement(element)
{
    const newElement = element.cloneNode(true);
    const descendents = newElement.getElementsByTagName("*");
    for (var i = 0; i < descendents.length; i++)
    {
        var e = descendents[i];
        if (e.id != '')
        {
            e.id = e.id + "_copy";

        }
    }

    return (newElement);

}
function validate()
{
    
    const baseForm = document.querySelector("#base");
    const next = document.querySelector("#next");
    const inputs = baseForm.querySelectorAll('input');
    const button = document.querySelector("#next-btn");

    button.disabled = true;
    next.style.display = 'none';
    for (i = 0; i < inputs.length; i++)
    {
        inputs[i].addEventListener('input', () => {
            let values = [];
            inputs.forEach(v => values.push(v.value));
            button.disabled = values.includes('');

        });
    }
    button.onclick = () => {
        next.style.display = 'block';
        baseForm.style.display = 'none';
        getCities();


    }

}



function updateChoices()
{
    const choices = document.querySelectorAll('.choices');
    choices.forEach(choice => {
        const divField = choice.firstElementChild;
        const input = divField.firstElementChild;
        const ul = choice.children[1].firstElementChild;
        const hiddenInput = choice.lastElementChild;
        const form = document.querySelector('form');

        let array = [];
        input.onchange = () => {

            listChoices(array, input, ul);
        }

        form.addEventListener('submit', () => {
            hiddenInput.value = array.join();
        });

        
    });
}


function listChoices(array, field, list)
{
     
    // Adding the field value to the list 
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

function setPosition(position)
{
    let lat = position.coords.latitude;
    let lng = position.coords.longitude;

    fetch(`/auth/location/${lat}/${lng}`)
    .then(response => response.json())
    .then(result => {
        const cities = result.cities; 
        console.log(cities); 
        const form = document.querySelector("form");
        const select = form.querySelector("#id_city");
        console
        cities.forEach(city => {
            const option = document.createElement('option');
            option.innerHTML = city['city'];
            select.add(option); 

        });
    

    })

}

function getCities()
{
    var positionArr = navigator.geolocation.getCurrentPosition(setPosition);

    
}


