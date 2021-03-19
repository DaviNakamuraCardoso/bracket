import choices from './choices.js';
import cropexp from './cropper.js';

let TYPES = [];

/**
* @name main
* @function
* @global
* @returns {Void}
*/
function main()
{
    // Get the form container and its buttons
    let page = 0;
    const container = document.querySelector("#main__div");
    const form = container.querySelector(".register__form");

    let user = element("user");
    const type = element("type");

    if (user.children.length != 0)
    {
        form.append(user)
        page++;
        user.style.left = '0';
        type.style.left = '100%';
        user.querySelector('.button__next').onclick = () =>
        {
            type.style.left = '0';
            user.style.left = '100%';
        }
    }
    else
    {
        type.style.left = '0';
    }

    form.append(type);

    const buttonContainer = type.querySelector(".button__container");
    const buttons = buttonContainer.querySelectorAll(".register__button");


    for (let i = 0; i < buttons.length; i++)
    {
        buttons[i].onclick = () =>
        {
            update(i, form, page+1);
        }
    }

    const yes = type.querySelector("button");
    buttonContainer.style.display = 'none';

    yes.onclick = () =>
    {
        buttonContainer.style.display = 'flex';
    }

    cropexp(user);
}


/**
* @name update
* @function
* @global
* @return {void}
*/
function update(value, container, page)
{
    // Get all the templates
    const doctor = element("doctor");
    const clinic = element("clinic");


    switch(value)
    {

        // Only doctor
        case 0:
            container.append(doctor);
            TYPES.push('doctor');
            break;
        // Only clinic
        case 1:
            container.append(clinic);
            TYPES.push('clinic');
            break;
        // Both doctor and clinic
        case 2:
            container.append(doctor);
            container.append(clinic);
            TYPES.push('clinic');
            TYPES.push('doctor');
            break;
    }

    // Update the choice fields and location
    choices(container);
    cropexp(clinic);

    load(page);
}


/**
@name load
@function
@global
@param n {Integer}
@returns {Void}
*/
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
        const input = document.querySelector('[name=types]');

        input.name = 'types';
        input.type = 'hidden';
        input.value = TYPES.join();

        // Convert the next button into a submit button
        next.type = 'submit';
    }
}


/**
* @name element
* @function
* @global
* @param {string} id
* @returns {DOMObject} f
*/
function element(id)
{

    // Get the template
    const template = document.querySelector(`#${id}__form`);

    // Return a new node
    return (template.content.cloneNode(true).children[0]);
}


// Call the main function
main();
