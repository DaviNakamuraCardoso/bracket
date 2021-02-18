
/**
* @name main
* @function
* @global
*/
function main()
{
    // Get the invite button
    const button = document.querySelector("#invite");

    // If it is a clinic admin adding a doctor, call the handleAdd function
    if (button.dataset.type == "add")
    {
        button.onclick = () => {
            handleAdd(this);
        }
    }
    // If it is a doctor asking to join a clinic, call the handleAsk function
    else if (button.dataset.type == "ask")
    {
        button.onclick = () => {
            handleAsk(this);
        }
    }
}


/**
* @name handleAdd
* @function
* @global
* @param {Element} button - The button that was clicked
*/
function handleAdd(button)
{
    // Prevents the user from double clicking the button
    button.style.pointerEvents = 'none';

    // Send a get request to the server, asking for the right set of clinics
    fetch(button.dataset.url)

    // Parse the response to JSON
    .then(response => response.json())

    // The server return a array of objects with clinic id and clinic name
    .then(clinics => {

        // Selects the popUp datalist
        const popUp = document.querySelector("#pop-up");

        // Adds the clinics to the datalist
        for (let i = 0; i < clinics.clinics.length; i++)
        {
            let option = document.createElement('option');
            option.value = clinics.clinics[i].id;
            option.label = clinics.clinics[i].name;
            popUp.append(option);
        }

        // Show the form
        const form = popUp.parentElement;
        form.className = 'show';

    })
}


/**
* @name handleAsk
* @function
* @global
* @param {Element} button - The clicked button
*/
function handleAsk(button)
{

    // Prevents double click
    button.style.pointerEvents = 'none';

    // CSRF token to prevent Cross-origin attacks
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const request = new Request(
        button.dataset.url,
        {headers: {'X-CSRFToken': csrftoken}}

    );

    // Invite variable is true when this is a request to join the clinic, and
    // false when is the user wants to cancel the invitation
    const invite = (button.dataset.value == 'request') ? true : false;

    // Fetches the url with the CSRF token
    fetch(request, {
        method: 'POST',
        mode: 'same-origin',
        body: JSON.stringify({
            'invite': invite
        })
    })

    // Parse the response to JSON
    .then(response => response.json())

    // Display the message as a notification
    .then(result => {
        console.log(result.message);
    });


}

document.addEventListener("DOMContentLoaded", main);
