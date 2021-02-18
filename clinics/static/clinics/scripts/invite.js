
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
            handleAdd(button);
        }
    }
    // If it is a doctor asking to join a clinic, call the handleAsk function
    else if (button.dataset.type == "ask")
    {
        button.onclick = () => {
            handleAsk(button);
        }
    }
}


/**
* @name handleAdd
* @function
* @global
* @param {element} button - The button that was clicked
* @return {void} Sends a request to the server with the clinic in which the
* doctor should be added
// */
function handleAdd(button)
{
    // Prevents the user from double clicking the button
    button.style.pointerEvents = 'none';

    // Send a get request to the server, asking for the right set of clinics
    console.log(button.dataset.url);
    fetch(button.dataset.url)
    .then(response => response.json())
    .then(result => {

        const clinics = result;
        // Selects the popUp datalist

        const datalist = document.querySelector("#cities");

        // Adds the clinics to the datalist
        for (let i = 0; i < clinics.clinics.length; i++)
        {
            let option = document.createElement('option');
            option.value = clinics.clinics[i].id;
            option.label = clinics.clinics[i].name;
            datalist.append(option);
        }

        // Show the form
        const form = document.querySelector("#pop-up");
        form.className = 'show';
        form.onsubmit = () => {

          // Get the clinic id
          const id = document.querySelector('[name=clinic]').value;


          // Prevents from cross script attacks
          const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
          const request = new Request(
              form.action,
              {headers: {"X-CSRFToken": csrftoken}}
          );

          // Asynchronously sends a request to the server with the clinic id
          fetch(request, {
            method: 'PUT',
            mode: 'same-origin',
            body: JSON.stringify({
              "clinic_id": id
            })
          })

          // Parse to JSON
          .then(response => response.json())

          // Show the message
          .then(result => {
              console.log(result);
              return false;
          });
          return false;
        }
    });
}


/**
* @name handleAsk
* @function
* @global
* @param {element} button - The clicked button
* @return {void} - Sends a request to the server to add a ask the clinic admin
* to join.
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
    const join = (button.dataset.value == 'request') ? true : false;

    // Fetches the url with the CSRF token
    fetch(request, {
        method: 'PUT',
        mode: 'same-origin',
        body: JSON.stringify({
            'request': join
        })
    })

    // Parse the response to JSON
    .then(response => response.json())

    // Display the message as a notification
    .then(result => {
        console.log(result.message);
    });


}

/**
* @name handleLeave
* @function
* @global
* @param {element} button - The clicked button
* @return {void}
*/
function handleLeave(button)
{
  const token = document.querySelector("[name=csrfmiddlewaretoken]").value;
  const request = new Request(
    button.dataset.url,
    {headers: {'X-CSRFToken': token}}
  );

  fetch(request, {
    method: "DELETE",
    mode: 'same-origin'
  })
  .then(response => response.json())
  .then(result => {
    console.log(result);
    button.dataset.type = 'ask';
    button.dataset.url = result.url;
    button.dataset.value = 'request'; 
  })

}

// Starts the function when the content is loaded
document.addEventListener("DOMContentLoaded", main);
