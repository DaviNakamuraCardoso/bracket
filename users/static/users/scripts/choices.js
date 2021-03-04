/**
* @name choices
* @function
* @global
* @param {Element} form - Form
* @return {void}
*/
export default function choices(form)
{
    const choices = document.querySelectorAll('.choices');
    choices.forEach(choice => {
        const divField = choice.firstElementChild;
        const input = divField.firstElementChild;
        const ul = choice.children[1].firstElementChild;
        const hiddenInput = choice.lastElementChild;

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
