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
]; 


document.addEventListener('DOMContentLoaded', () => {

    const d = new Date(); 
    startCalendar(d.getMonth(), d.getFullYear()); 
    
}); 


function startCalendar(month, year)
{
    const calendar = document.querySelector("#month"); 
    const monthTitle = document.querySelector("#month-title"); 
    const yearTitle = document.querySelector("#year-title"); 

    calendar.innerHTML = "<tr><th>Sunday</th> <th>Monday</th> <th>Tuesday</th> <th>Wednesday</th> <th>Thursday</th> <th>Friday</th> <th>Saturday</th></tr>"; 
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

                day.onclick = () => {
                    loadDay(year, month, dayNum); 
                }

                if (index < result.start || index > result.end)
                {
                    day.classList.add('invalid'); 
                }
                index++;


            }
            calendar.append(row); 
            
        }
    });
    const previousMonth = document.querySelector("#prev-month"); 
    const nextMonth = document.querySelector("#next-month"); 
    previousMonth.onclick = () => {
        if (month > 0)
        {
            startCalendar(month-1, year)
        }
        else 
        {
            startCalendar(11, year-1)
        }

    }
    nextMonth.onclick = () => {
        if (month < 11)
        {
            startCalendar(month+1, year);
        }
        else 
        {
            startCalendar(0, year+1)
        }
    }

    const previousYear = document.querySelector("#prev-year"); 
    const nextYear = document.querySelector("#next-year");

    previousYear.onclick = () => {
        startCalendar(month, year-1); 
    }

    nextYear.onclick = () => {
        startCalendar(month, year+1);
    }
    loadEssentials(); 
    
    
    

}

function loadEssentials()
{
    doctorsLoad(); 
}


function doctorsLoad()
{
    fetch('/doctors/louis.pasteur/days')
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
                    
                    }

                }); 
            }
        }); 
    });
}


function loadDay(year, month, day)
{
    console.log(year); 
    console.log(month); 
    console.log(day); 
    fetch(`/doctors/louis.pasteur/${year}/${month}/${day}`)
    .then(response => response.json())
    .then(result => {
        const dayPlanner = document.querySelector(".day-planner"); 
        dayPlanner.classList.toggle('open'); 

    }); 
}