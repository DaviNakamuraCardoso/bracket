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
    const type = container.dataset.type;

    fetch(url)
    .then(response => response.json())
    .then(result => {
        const divisions = result.appointments;

        for (let i = 0; i < divisions.length; i++)
        {
            const template = document.querySelector("#appointment").content.cloneNode(true).children[0];
            const node = serialize(template);

            const appointments = divisions[i].appointments;

            for (let j = 0; j < appointments.length; j++)
            {
                const tr = document.createElement('tr');
                const appointment = appointments[j];

                const hour = document.createElement('td');
                const patient = document.createElement('td');
                const area = document.createElement('td');
                const status = document.createElement('td');
                const action = document.createElement('td');


                // Content
                const statusContent = document.createElement('div');

                hour.innerHTML = appointment.time;
                patient.innerHTML = appointment.patient;
                area.innerHTML = appointment.area;
                statusContent.innerHTML = appointment.status;


                statusContent.className = 'appointment__status';
                statusContent.classList.add(`appointment__status--${appointment.status.split(" ").join("_")}`);

                status.append(statusContent);

                tr.append(hour);
                tr.append(patient);
                tr.append(area);
                tr.append(status);
                tr.append(action);

                node['body'].append(tr);

                switch(type)
                {
                    case "clinic":
                    {
                        const header = document.querySelector("#header").content.cloneNode(true).children[0];
                        const h = serialize(header);
                        console.log(header); 

                    }
                }

            }

            switch(type)
            {
                case "doctor":
                {

                    break;
                }
            }

            container.append(template);

        }

        VERSION = result.version;


    });
}


function serialize(node)
{
    const children = node.getElementsByTagName("*");
    let object = {};
    for (let i = 0; i < children.length; i++)
    {
        const name = children[i].className.split("__")[1];
        object[name] = children[i];
    }
    return (object);
}
document.addEventListener("DOMContentLoaded", main);
