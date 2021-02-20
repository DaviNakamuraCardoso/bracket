const DAYS = {
    "Sunday": 0,
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thursday": 4,
    "Friday": 5,
    "Saturday": 6,
}

const MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]


// Starts a basic calendar
function startCalendar(month, year, fill)
{
    const calendar = document.querySelector("#month");
    const monthTitle = document.querySelector("#month-title");
    const yearTitle = document.querySelector("#year-title");
    const calendarBody = calendar.querySelector('tbody');

    calendarBody.innerHTML = '';


    monthTitle.innerHTML = MONTHS[month];
    yearTitle.innerHTML = year;

    fetch(`/auth/calendar/${year}/${month}`)
    .then(response => response.json())
    .then(result => {

        let index = 0;
        for (let i = 0; i < 6; i++)

        {
            const row = document.createElement('tr');
            for (let j = 0; j < 7; j++)
            {


                const day = document.createElement('td');
                const div = document.createElement('div');

                let dayNum = result.calendar[index];
                div.innerHTML = dayNum;
                div.className = "ball";
                day.className = "day";
                day.id = index;

                day.append(div);
                row.append(day);

                if (index < result.start || index >= result.end)
                {
                    day.classList.add('invalid');
                }
                index++;


            }
            calendarBody.append(row);

        }
    });
    const previousMonth = document.querySelector("#prev-month");
    const nextMonth = document.querySelector("#next-month");
    previousMonth.onclick = () => {
        if (month > 0)
        {
            startCalendar(month-1, year, fill);
        }
        else
        {
            startCalendar(11, year-1, fill);
        }

    }
    nextMonth.onclick = () => {
        if (month < 11)
        {
            startCalendar(month+1, year, fill);
        }
        else
        {
            startCalendar(0, year+1, fill);
        }
    }

    const previousYear = document.querySelector("#prev-year");
    const nextYear = document.querySelector("#next-year");

    previousYear.onclick = () => {
        startCalendar(month, year-1, fill);
    }

    nextYear.onclick = () => {
        startCalendar(month, year+1, fill);
    }
    fill();

}


function thisDay(year, month, day, hourString)
{
    return (new Date(`${year}/${month}/${day} ${hourString}`));
}


function pad(n, width, z) {
  z = z || '0';
  n = n + '';
  return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}



export default startCalendar
export {DAYS, MONTHS, thisDay, pad}
