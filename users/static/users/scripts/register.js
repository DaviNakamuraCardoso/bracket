document.addEventListener('DOMContentLoaded', () => 
{
    
    const userTypeSelect = document.querySelector("select");
    const form = document.querySelector("form");
    const next = document.querySelector("#next");
    

    next.innerHTML = document.querySelector("#patient").innerHTML;

    updateChoices();
    validate();

    userTypeSelect.onchange = () => {

        form.action = userTypeSelect.value;
        let text = userTypeSelect.options[userTypeSelect.selectedIndex].text;
        next.innerHTML = document.getElementById(text).innerHTML;
        updateChoices();

    }



});
function validate()
{
    
    const baseForm = document.querySelector("#base-form");
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

