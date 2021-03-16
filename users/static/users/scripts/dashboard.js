import ping from '../../base/scripts/message.js';


let VERSION = 0;


function main()
{
    getAppointments();
    setInterval(getAppointments, 10000);
}


function listen(container, id)
{
    const url = `${container.dataset.url}/${id}`;
    const csrftoken = container.querySelector("[name=csrfmiddlewaretoken]").value;
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
                getAppointments();

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


        const divisions = result.appointments;

        // Variables to be shown in the counters
        let confirmed = 0;
        let cancelled = 0;
        let checked = 0;
        let total = 0;

        const divisionsContainer = document.querySelector(".appointments__divisions");
        divisionsContainer.innerHTML = "";


        for (let i = 0; i < divisions.length; i++)
        {
            const template = document.querySelector("#appointment").content.cloneNode(true).children[0];
            const node = serialize(template);

            const link = document.querySelector("#dashboard__link").content.cloneNode(true).children[0];
            const l = serialize(link);

            const appointments = divisions[i].appointments;
            const model = divisions[i].object;

            template.id = model.id;

            node['division-title'].innerHTML = model.title;
            node['division-image'].src = model.image;

            l['image'].src = model.image;
            link.href = `#${model.id}`;

            const snippet = document.querySelector("#dashboard__snippet");
            snippet.append(link);

            total += appointments.length;
            for (let j = 0; j < appointments.length; j++)
            {
                //
                const tr = document.createElement('tr');
                const appointment = appointments[j];

                // Create td for all the appointment info
                const hour = document.createElement('td');
                const patient = document.createElement('td');
                const area = document.createElement('td');
                const status = document.createElement('td');
                const action = document.createElement('td');

                // Status tag
                const statusContent = document.createElement('div');

                // Action buttons
                const buttonContainer = document.querySelector("#buttons__container").content.cloneNode(true).children[0];

                // Fill the table row with info
                hour.innerHTML = appointment.time;
                patient.innerHTML = appointment.patient;
                area.innerHTML = appointment.area;
                statusContent.innerHTML = appointment.status;

                // Fill the status and set its class name
                statusContent.className = 'appointment__status';
                statusContent.classList.add(`appointment__status--${appointment.status.split(" ").join("_")}`);

                status.append(statusContent);


                tr.className = "appointment__row";

                // Append all the data to the row
                tr.append(hour);
                tr.append(patient);
                tr.append(area);
                tr.append(status);
                tr.append(action);

                // Append the row to the table
                node['body'].append(tr);

                // Update counter variables based on the status
                switch(appointment.status)
                {
                    case "cancelled":
                    {
                        tr.classList.add("appointment__row--inactive");
                        cancelled++;
                        break;
                    }
                    case "confirmed":
                    {
                        action.append(buttonContainer);
                        listen(buttonContainer, appointment.id);
                        confirmed++;
                        break;
                    }
                    case "checked":
                    {
                        checked++;
                        tr.classList.add("appointment__row--inactive");
                        break;
                    }
                    default:
                    {
                        action.append(buttonContainer);
                        listen(buttonContainer, appointment.id);
                        break;

                    }
                }
            }

            if (type == "clinic")
            {
                const header = document.querySelector("#header").content.cloneNode(true).children[0];
                node['body-container'].append(header);
            }

            divisionsContainer.append(template);

        }


        if (type == "doctor")
        {
            const header = document.querySelector("#header").content.cloneNode(true).children[0];
            divisionsContainer.prepend(header);

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
