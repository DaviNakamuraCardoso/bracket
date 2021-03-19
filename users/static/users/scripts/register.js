import choices from './choices.js';
import cropexp from './cropper.js';

let TYPES = [];

/**
* @name main
* @function
* @global
* @returns {void}
*/
function main()
{
    // Get the form container and its buttons
    const container = document.querySelector("#main__div");
    const buttons = container.querySelectorAll('.register__button');
    const buttonContainer = container.querySelector(".button__container");

    for (let i = 0; i < buttons.length; i++)
    {
        buttons[i].onclick = () =>
        {
            buttonContainer.style.display = 'none';
            update(i, container.querySelector('form'));
        }
    }
}


/**
* @name update
* @function
* @global
* @return {void}
*/
function update(value, container)
{
    // Get all the templates
    let user = element("user");
    const doctor = element("doctor");
    const clinic = element("clinic");


    // If the user has already provided all the necessary info, skip
    const size = user.children.length;

    if (size == 0)
    {
        // If it is a regular user, redirect to the index page
        if (value == 0)
        {
            location.replace('/');
        }

    }
    // If we don't have the user address or picture, add the container
    else
    {
        container.append(user);
    }

    switch(value)
    {

        // Only doctor
        case 1:
            container.append(doctor);
            TYPES.push('doctor');
            break;
        // Only clinic
        case 2:
            container.append(clinic);
            TYPES.push('clinic');
            break;
        // Both doctor and clinic
        case 3:
            container.append(doctor);
            container.append(clinic);
            TYPES.push('clinic');
            TYPES.push('doctor');
            break;
    }

    // Update the choice fields and location
    choices(container);
    cropexp();

    load(0);

}


function load(n)
{
    const forms = document.querySelectorAll('.form__container');
    for (let i = 0; i < forms.length; i++)
    {
        forms[i].style.left = `${(i-n) * 100}%`;
    }

    const current = forms[n];
    const next = current.querySelector(".button__next");

    if (n < forms.length - 1)
    {
        next.onclick = () =>
        {
            load(n+1);
        }
    }
    else
    {
        // Create an input with all the selected types
        const input = document.createElement('input');

        input.name = 'types';
        input.type = 'hidden';
        input.value = TYPES.join();
        current.append(input);

        // Convert the next button into a submit button
        next.type = 'submit';
    }
}


/**
* @name element
* @function
* @global
* @param {String} id
* @return {Void}
*/
function element(id)
{

    // Get the template
    const template = document.querySelector(`#${id}__form`);

    // Return a new node
    return (template.content.cloneNode(true));
}




// Call the main function
main();
