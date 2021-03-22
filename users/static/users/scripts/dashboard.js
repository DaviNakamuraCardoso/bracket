import ping, {Load} from '../../base/scripts/message.js';


let VERSION = 0;


function main()
{


    // Creates the page
    getAppointments();

    setInterval(getAppointments, 60000);
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

    let load;
    if (VERSION == 0)
    {
        // Starts the loading animation
        const main = document.querySelector("main");
        load = new Load(main);
        load.start();
    }
    fetch(url)
    .then(response => response.json())
    .then(result => {
        
        if (result.message == "Dashboard up to date.")
        {
            const delays = document.querySelectorAll('.appointments__delay-title');
            for (let i = 0; i < delays.length; i++)
            {
                const hour = delays[i].querySelector(".appointments__delay-title-hours");
                const minute = delays[i].querySelector(".appointments__delay-title-minutes");

                let hours = parseInt(hour.innerHTML) || 0;
                let minutes = parseInt(minute.innerHTML) || 0;

                if (!minutes && !hours)
                {
                    continue;
                }

                minutes++;

                minute.innerHTML = (minutes >= 60)? "" : `${minutes}min`;


                hour.innerHTML = (minutes >= 60)? `${hours+1}h`: (hours >= 1)? `${hours}h` : '';


                console.log(hours);
                console.log(minutes);
            }
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

        const snippet = document.querySelector("#dashboard__snippet");
        snippet.innerHTML = "";

        let curr = [];

        for (let i = 0; i < divisions.length; i++)
        {
            const template = document.querySelector("#appointment").content.cloneNode(true).children[0];
            const node = serialize(template);

            const link = document.querySelector("#dashboard__link").content.cloneNode(true).children[0];
            const l = serialize(link);

            const appointments = divisions[i].appointments;
            const model = divisions[i].object;

            let current = [];

            template.id = model.id;

            node['division-title'].innerHTML = model.title;
            node['division-image'].src = model.image;

            l['image'].src = model.image;
            link.href = `#${model.id}`;

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
                    case "checked":
                    {
                        checked++;
                        tr.classList.add("appointment__row--inactive");
                        break;
                    }
                    case "confirmed":
                    {
                        confirmed++;
                    }
                    default:
                    {
                        current.push(appointment);
                        curr.push(appointment);
                        action.append(buttonContainer);
                        listen(buttonContainer, appointment.id);
                        break;

                    }
                }
            }

            if (type == "clinic")
            {
                const header = document.querySelector("#header").content.cloneNode(true).children[0];
                const h = serialize(header);

                // Set up the info for the current appointment, if any
                h['now-body-title'].innerHTML = current[0]?.patient ?? '-';
                h['now-time'].innerHTML = current[0]?.time ?? '-';

                // Set up the info for the next appointment, if any
                h['next-body-title'].innerHTML = current[1]?.patient ?? '-';

                // Set the delay

                const hours = current[0]?.delay[2] || null;
                const minutes = current[0]?.delay[3] || null;

                let delay;
                h['delay-title-hours'].innerHTML = (hours) ? `${hours}h` : '';
                h['delay-title-minutes'].innerHTML = (minutes) ? `${minutes}min` : '';

                h['delay-title'].classList.add(`appointments__delay-${current[0]?.delay[1] ?? 'none'}`);

                node['body-container'].append(header);
            }

            divisionsContainer.append(template);

        }


        if (type == "doctor")
        {

            const header = document.querySelector("#header").content.cloneNode(true).children[0];
            const h = serialize(header);

            // Set up the info for the current appointment, if any
            h['now-body-title'].innerHTML = curr[0]?.patient ?? '-';
            h['now-time'].innerHTML = curr[0]?.time ?? '-';

            // Set up the info for the next appointment, if any
            h['next-body-title'].innerHTML = curr[1]?.patient ?? '-';

            // Set the delay
            const hours = curr[0]?.delay[2] || null;
            const minutes = curr[0]?.delay[3] || null;

            let delay;
            h['delay-title-hours'].innerHTML = (hours)? `${hours}h` : '';
            h['delay-title-minutes'].innerHTML = (minutes)? `${minutes}min` : '';

            h['delay-title'].classList.add(`appointments__delay-${curr[0]?.delay[1] ?? 'none'}`);

            divisionsContainer.prepend(header);

        }
        const h = serialize(document.querySelector('.appointments__header'));

        h['total'].innerHTML = total;
        h['checked'].innerHTML = checked;
        h['cancelled'].innerHTML = cancelled;
        h['confirmed'].innerHTML = confirmed;


        if (VERSION == 0)
        {
            load.stop();
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
