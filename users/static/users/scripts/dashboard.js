import ping from '../../base/scripts/message.js';


function main()
{
    const appointments = document.querySelectorAll(".appointment__");
    for (let i = 0; i < appointments.length; i++)
    {
        listen(appointments[i]);
    }
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


document.addEventListener("DOMContentLoaded", main);
