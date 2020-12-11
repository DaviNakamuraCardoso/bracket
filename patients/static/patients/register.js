document.addEventListener('DOMContentLoaded', () => 
{
    const values = [];
    const allergies = document.querySelector("#allergies");
    const form = document.querySelector('form');
    const list = document.querySelector("#list");
    allergies.onkeyup = function(event) 
    {
        if (event.key == 'Enter') 
        {
            // Adding the allergy value to the list 
            values.push(allergies.value);

            // Creating an li element to show the allergy
            const li = document.createElement('li');
            const btn = document.createElement('button');
            const val = document.createElement('span');

            val.innerHTML = allergies.value;
            btn.innerHTML = 'x';

            

            btn.addEventListener('click', () => {

                const element = btn.parentElement;
                const v = element.firstChild;
                const index = values.indexOf(v.innerHTML);
            
                console.log(index);
                console.log(v);
                values.splice(index, 1);
                element.remove();
            });


            // Adding the allergy to the list
            li.append(val);
            li.append(btn);

            list.append(li);

            // Reset the textarea value
            allergies.value = '';

        }
    }


    form.onsubmit = () => 
    {
        allergies.value = values.join();
        return true;
    }



});