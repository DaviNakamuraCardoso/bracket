import ping from '../../base/scripts/message.js';

let VERSION = 0;

function main()
{
    getAppointments();
}


function listen(appointment)
{
    const container = appointment.querySelector(".appointment__buttons");
    const url = container.dataset.url;
    const csrftoken = appointment.querySelector("[name=csrfmiddlewaretoken]").value;
    console.log(csrftoken);
    const request = new Request(
        url,
        {headers:{"X-CSRFToken": csrftoken}}
    );

    const buttons = container.querySelectorAll(".appointment__button");

    for (let i = 0; i < buttons.length; i++)
    {
        buttons[i].onclick = () =>
        {
            fetch(request, {
                method: 'PUT',
                body: JSON.stringify({
                    check: buttons[i].dataset.value=='check'
                })
            })
            .then(response => response.json())
            .then(result => {
                ping(result.message);

            });

        }
    }
}


function getAppointments()
{
    const container = document.querySelector(".appointments__container");
    const url = `${container.dataset.url}/${VERSION}`;

    fetch(url)
    .then(response => response.json())
    .then(result => {
        console.log(result);
        const template = document.querySelector("#appointment").content.cloneNode(true).children[0];
        console.log(template); 
        VERSION = result.version;

    });
}

document.addEventListener("DOMContentLoaded", main);
