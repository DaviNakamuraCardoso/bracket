import startCalendar, {DAYS, MONTHS, thisDay, pad} from '../../users/scripts/calendar.js';
import ping from '../../base/scripts/message.js';

document.addEventListener('DOMContentLoaded', () => {
    const d = new Date();

    const templates = document.querySelectorAll('.calendar__wrapper');
    for (let i = 0; i < templates.length; i++)
    {
        startCalendar(templates[i], d.getMonth(), d.getFullYear(), doctorsLoad);

    }
});


function doctorsLoad(template)
{
    const doctor = template.querySelector(".doctor").value;
    const clinic = template.querySelector(".clinic").value || '*';
    const area = template.querySelector(".area").value || '*';


    fetch(`/doctors/${doctor}/days/${clinic}/${area}`)
    .then(response => response.json())
    .then(result => {
        const days = template.querySelectorAll('.day');
        days.forEach(day => {
            let index = parseInt(day.id);

            if (!day.classList.contains('invalid'))
            {
                result.days.forEach(weekday => {
                    if (index % 7 == DAYS[weekday])
                    {
                        day.classList.add('active', true);

                        day.onclick = () => {
                          template.querySelectorAll(".selected").forEach(selected => selected.classList.toggle('selected', false));
                          day.classList.toggle('selected', true);
                          loadDay(template, day);
                        }
                    }
                });
            }
        });
    });
}


function loadDay(template, element)
{
    const day = element.querySelector('.ball').innerHTML;
    const month = MONTHS.indexOf(template.querySelector(".month-title").innerHTML);
    const year = template.querySelector(".year-title").innerHTML;
    const doctor = template.querySelector(".doctor").value;

    const button = template.querySelector(".button__close");
    fetch(`/doctors/${doctor}/${year}/${month}/${day}`)
    .then(response => response.json())
    .then(result => {

        if (result.message == "Not authorized.")
        {
            const paths = window.location.href.split('/');
            const next = window.location.href.split('/').slice(3, paths.length).join('/');
            window.location.replace(`${result.url}?next=/${next}`);
        }

        let dayInfo = result.day;
        const dayPlanner = template.querySelector(".day-planner");
        const hours = template.querySelector('.hours');
        const appointments = template.querySelector(".appointments");
        const schedule = template.querySelector(".schedule");
        hours.innerHTML = '';
        appointments.innerHTML = '';

        dayPlanner.classList.toggle('open', true);
        schedule.classList.toggle('visible', false);



        button.onclick = () => {
            dayPlanner.classList.toggle('open', false);
            schedule.classList.toggle('visible', false);
        }
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
                    appointmentDiv.classList.toggle('closed', false);
                }
            }
        }

        updateAllAppointments(template);

    });

}


function updateAllAppointments(template)
{
    const appointments = template.querySelectorAll('.appointment');
    const schedule = template.querySelector(".schedule");
    const children = serializeNode(schedule, 'schedule');

    const day = template.querySelector(".selected").querySelector('.ball').innerHTML;
    const month = MONTHS.indexOf(template.querySelector(".month-title").innerHTML);
    const year = template.querySelector(".year-title").innerHTML;
    const doctor = template.querySelector(".doctor").value;

    appointments.forEach(appointment => {
        if (!appointment.classList.contains('closed'))
        {
            appointment.onclick = () => {


                appointments.forEach(appointment => appointment.classList.toggle('chosen__appointment', false));
                appointment.classList.toggle('chosen__appointment', true);

                const index = appointment.id.split('_')[1];
                fetch(`/doctors/${doctor}/${year}/${month}/${day}/${index}`)
                .then(response => response.json())
                .then(result => {


                    console.log(result);


                    const shift = result.shift;
                    const clinic = shift.clinic;

                    children['hour'].innerHTML = `${stripSeconds(result.hour[0])}-${stripSeconds(result.hour[1])}`;
                    children['day'].innerHTML = `${shift.day}, ${day}/${month}/${year}`;

                    children['clinic'].innerHTML = clinic.title;
                    children['clinic_image'].src = clinic.image;
                    children['location-title fas-text address'].innerHTML = clinic.address;
                    children['areas'].innerHTML = '';

                    children['doctor'].innerHTML = shift.doctor.title;
                    children['doctor_image'].src = shift.doctor.image;

                    shift.areas.forEach(area => {
                        let option = document.createElement('option');
                        option.value = area;
                        option.innerHTML = area;
                        children['areas'].append(option);
                    });

                    children['areas'].value = shift.areas[0];

                    children['area-info'].innerHTML = result.appointment.area;
                    children['user-info'].innerHTML = result.appointment.user;

                    let remove;

                    if (appointment.classList.contains('chosen'))
                    {
                        children['form'].style.display = 'none';
                        children['form-info'].style.display = 'flex';
                        remove = true;

                    }
                    else
                    {
                        children['form'].style.display = 'flex';
                        children['form-info'].style.display = 'none';
                        remove = false;
                    }

                    const csrfToken = template.querySelector('[name=csrfmiddlewaretoken]').value;
                    const request = new Request(
                        children['form'].action,
                        {headers: {'X-CSRFToken': csrfToken}}

                    );

                    function fetchSchedule() {

                        children['submit'].disabled = true;
                        children['cancel'].disabled = true;
                        
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
                                'shift': shift.id,
                                'remove': remove

                            })
                        })
                        .then(response => response.json())
                        .then(result => {
                            ping(result.message);

                            if (!remove)
                            {


                                children['area-info'].innerHTML = children['areas'].value;
                                children['user-info'].innerHTML = children['user'].value;


                                children['form'].style.display = 'none';
                                children['form-info'].style.display = 'flex';
                            }
                            else
                            {
                                children['form'].style.display = 'flex';
                                children['form-info'].style.display = 'none';

                            }
                            appointment.classList.toggle('chosen', !remove);
                            remove = !remove;

                            children['submit'].disabled = false;
                            children['cancel'].disabled = false;

                        });
                        return false;


                    }
                    children['form'].onsubmit = fetchSchedule;
                    children['cancel'].onclick = fetchSchedule;

                    schedule.classList.toggle('visible', true);

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


function serializeNode(node, name)
{

    const children = node.getElementsByTagName("*");
    let table = {};
    for (let i = 0; i < children.length; i++)
    {
        table[children[i].className.replace(`${name}-`, '')] = children[i];

    }

    return (table);
}


function stripSeconds(hour)
{
    return (hour.split(':').slice(0,2).join(':'));
}
