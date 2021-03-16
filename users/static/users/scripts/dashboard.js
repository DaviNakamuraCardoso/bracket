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

        if (result.message == "Dashboard up to date.")
        {
            return;
        }
        console.log(result);
        const divisions = result.appointments;

        // Variables to be shown in the counters
        let confirmed = 0;
        let cancelled = 0;
        let checked = 0;
        let total = 0;

        const divisionsContainer = document.querySelector(".appointments__divisions");


        for (let i = 0; i < divisions.length; i++)
        {
            const template = document.querySelector("#appointment").content.cloneNode(true).children[0];
            const node = serialize(template);

            const appointments = divisions[i].appointments;
            total += appointments.length;

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

                switch(appointment.status)
                {
                    case "cancelled":
                    {
                        cancelled++;
                        break;
                    }
                    case "confirmed":
                    {
                        confirmed++;
                        break;
                    }
                    case "checked":
                    {
                        checked++;
                        break;
                    }
                }
            }

            switch(type)
            {
                case "clinic":
                {
                    const header = document.querySelector("#header").content.cloneNode(true).children[0];
                    divisionsContainer.prepend(header);
                }
            }

            divisionsContainer.append(template);

        }


        const h = serialize(document.querySelector('.appointments__header'));

        h['total'].innerHTML = total;
        h['checked'].innerHTML = checked;
        h['cancelled'].innerHTML = cancelled;
        h['confirmed'].innerHTML = confirmed;


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
