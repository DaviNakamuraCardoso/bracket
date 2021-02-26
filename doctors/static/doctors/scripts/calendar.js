import startCalendar, {DAYS, MONTHS, thisDay, pad} from '../../users/scripts/calendar.js'

document.addEventListener('DOMContentLoaded', () => {
    const d = new Date();

    startCalendar(d.getMonth(), d.getFullYear(), doctorsLoad);
    doctorsLoad();
});


function doctorsLoad()
{
    const doctor = document.querySelector("#doctor").value;
    fetch(`/doctors/${doctor}/days`)
    .then(response => response.json())
    .then(result => {
        const days = document.querySelectorAll('.day');
        days.forEach(day => {
            let index = parseInt(day.id);

            if (!day.classList.contains('invalid'))
            {
                result.days.forEach(weekday => {
                    if (index % 7 == DAYS[weekday])
                    {
                        day.classList.add('active', true);

                        day.onclick = () => {
                          document.querySelectorAll(".selected").forEach(selected => selected.classList.toggle('selected', false));
                          day.classList.toggle('selected', true);
                          loadDay(day);
                        }


                    }

                });
            }
        });
    });
}


function loadDay(element)
{
    const day = element.querySelector('.ball').innerHTML;
    const month = MONTHS.indexOf(document.querySelector("#month-title").innerHTML);
    const year = document.querySelector("#year-title").innerHTML;
    const doctor = document.querySelector("#doctor").value;
    fetch(`/doctors/${doctor}/${year}/${month}/${day}`)
    .then(response => response.json())
    .then(result => {

        if (result.message == "Not authorized.")
        {
            const paths = window.location.href.split('/');
            console.log(paths);
            const next = window.location.href.split('/').slice(3, paths.length).join('/');
            console.log(next);
            window.location.replace(`${result.url}/?next=/${next}`);
        }

        let dayInfo = result.day;
        const dayPlanner = document.querySelector(".day-planner");
        const hours = document.querySelector('#hours');
        const appointments = document.querySelector("#appointments");
        hours.innerHTML = '';
        appointments.innerHTML = '';

        dayPlanner.classList.toggle('open', true);

        let start = thisDay(year, month, day, dayInfo[0][0]);
        let end = thisDay(year, month, day, dayInfo[dayInfo.length-1][1]);

        let heightCounter = 0;
        for (let i = start.getHours(); i <= Math.ceil(end.getHours() + (end.getMinutes() / 60)); i++)
        {
            let span = document.createElement('span');
            span.innerHTML = `${pad(i, 2, 0)}:00`;
            hours.append(span);
            heightCounter++;
        }
        end = thisDay(year, month, day, `${heightCounter + start.getHours() -1}:00:00`);

        hours.style.height = `${heightCounter*200}px`;
        const absoluteSize = hours.offsetHeight;
        appointments.style.height = `${absoluteSize}px`;
        for (let i = 0; i < dayInfo.length; i++)
        {
            const appointment = dayInfo[i];
            const appointmentDiv = document.createElement('div');
            const appointmentStart = thisDay(year, month, day, appointment[0]);
            const appointmentDelta = thisDay(year, month, day, appointment[1]) - appointmentStart;
            const dayDelta = end - start;
            const position = (appointmentStart - start) / dayDelta;
            const size = appointmentDelta / dayDelta;

            appointmentDiv.className = "appointment";
            appointmentDiv.id = `appointment_${i}`;
            appointmentDiv.style.top = `${position*100}%`;
            appointmentDiv.innerHTML = `${stripSeconds(appointment[0])}-${stripSeconds(appointment[1])}`;

            appointmentDiv.style.height = `${absoluteSize * size - 2}px`;

            appointments.append(appointmentDiv);


            for (let j = 0; j < result.appointments.length; j++)
            {
                if (i == result.appointments[j])
                {
                    appointmentDiv.classList.toggle('closed', true);
                }
            }
            for (let k = 0; k < result.user_appointments.length; k++)
            {
                if (i == result.user_appointments[k])
                {
                    appointmentDiv.classList.toggle('chosen', true);
                }
            }
        }
        updateAllAppointments();
    });
}


function updateAllAppointments()
{
    const appointments = document.querySelectorAll('.appointment');
    const schedule = document.querySelector("#schedule");
    const children = serializeNode(schedule);

    const day = document.querySelector(".selected").querySelector('.ball').innerHTML;
    const month = MONTHS.indexOf(document.querySelector("#month-title").innerHTML);
    const year = document.querySelector("#year-title").innerHTML;
    const doctor = document.querySelector("#doctor").value;

    appointments.forEach(appointment => {
        if (!appointment.classList.contains('closed') && !appointment.classList.contains('chosen'))
        {
            appointment.onclick = () => {
                const index = appointment.id.split('_')[1];
                fetch(`/doctors/${doctor}/${year}/${month}/${day}/${index}`)
                .then(response => response.json())
                .then(result => {

                    const shift = result.shift;
                    const clinic = shift.clinic;
                    children['title'].innerHTML = `${stripSeconds(result.hour[0])}-${stripSeconds(result.hour[1])}`;
                    children['location-title'].innerHTML = clinic.address;
                    children['areas-datalist'].innerHTML = '';

                    shift.areas.forEach(area => {
                        let option = document.createElement('option');
                        option.value = area;
                        children['areas-datalist'].append(option);
                    });

                    children['areas'].value = shift.areas[0];

                    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                    const request = new Request(
                        children['form'].action,
                        {headers: {'X-CSRFToken': csrfToken}}

                    );

                    children['form'].onsubmit = () => {

                        fetch(request, {
                            method: 'POST',
                            mode: 'same-origin',
                            body: JSON.stringify({
                                'index': index,
                                'day': day,
                                'month': month,
                                'year': year,
                                'patient': children['user'].value,
                                'area': children['areas'].value,
                                'shift': shift.id

                            })
                        })
                        .then(response => response.json())
                        .then(result => {
                            console.log(result.message);
                            appointment.classList.toggle('chosen', true);

                        });
                        return false;


                    }
                });
            }
        }
        else if (appointment.classList.contains('chosen'))
        {
            appointment.onclick = () => {

            }
        }
    });
}


function serializeNode(node)
{

    const children = node.getElementsByTagName("*");
    let table = {};
    for (let i = 0; i < children.length; i++)
    {
        table[children[i].id.replace(`${node.id}-`, '')] = children[i];

    }

    return (table);
}


function stripSeconds(hour)
{
    return (hour.split(':').slice(0,2).join(':'));
}
