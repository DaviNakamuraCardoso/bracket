import setPosition from './geolocation.js';

document.addEventListener('DOMContentLoaded', () =>
{
    let types = ['user'];

    const nextButton = document.querySelector("#next");

    nextButton.onclick = () => {

        const checkBoxes = document.querySelectorAll('.checkbox-input');
        checkBoxes.forEach(checkBox => {

            const value = checkBox.value;
            if (checkBox.checked)
            {
                types.push(value);
                if (value == 'doctor')
                {
                    const specificForm = document.querySelector(`#${value}-form`);
                    specificForm.innerHTML;
                    specificForm.append(copyElement(document.getElementById(value)));
                }

            }
        });
        const typesInput = document.querySelector("#id_types");
        typesInput.value = types.join();

        updateChoices();
        navigator.geolocation.getCurrentPosition(setPosition);

        next(types, 0, nextButton);

    }
});


function next(array, index, button)
{
    const type = array[index];
    if (type == 'doctor' || type == 'user')
    {
        const e = document.querySelector(`#${array[index]}-form`);
        show(e.firstElementChild);
        
        if (index == array.length-1 || !array.slice(index+1, array.length).includes('doctor'))
        {
            button.type = 'submit';
        }
        else
        {
            validate(e);

            button.onclick = () =>
            {
                hide(e);
                next(array, index+1, button);
            }
        }
    }
    else
    {
        if (!array.slice(index, array.length).includes('doctor'))
        {
            button.type = 'submit';
        }
        else
        {
            next(array, index+1, button);
        }
    }






}


function show(element)
{
    element.classList.toggle('hidden', false);
}


function hide(element)
{
    element.classList.toggle('hidden', true);
}


function copyElement(element)
{
    const newElement = element.cloneNode(true);
    const descendents = newElement.getElementsByTagName("*");
    for (var i = 0; i < descendents.length; i++)
    {
        var e = descendents[i];
        if (e.id != '')
        {
            e.id = `${e.id}_copy`;
        }
    }
    return (newElement);
}


function validate(element)
{
    const button = document.querySelector("#next");
    const inputs = element.querySelectorAll('input');

    button.disabled = true;
    for (let i = 0; i < inputs.length; i++)
    {
        inputs[i].addEventListener('input', () => {
            let values = [];
            inputs.forEach(input => {
                if (input.required)
                {
                    values.push(input.value)

                }

            });

            button.disabled = values.includes('');
        });
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
        const form = document.querySelector('#signup');

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
    console.log(array);
}
