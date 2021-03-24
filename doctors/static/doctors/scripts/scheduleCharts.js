
const PALETTE = [
    '#4387f5',
    '#EC5272',
    '#6FFACB',
    '#996FFB'
]

function buildChart()
{
    google.charts.load("current", {packages:["timeline"]});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {

        const container = document.getElementById('timeline');
        const chart = new google.visualization.Timeline(container);
        const dataTable = new google.visualization.DataTable();

        fetch(container.dataset.api)
        .then(response => response.json())
        .then(shifts => {
            dataTable.addColumn({ type: 'string', id: 'Day' });
            dataTable.addColumn({ type: 'string', id: 'Areas' });
            dataTable.addColumn({ type: 'string', id: 'style', role: 'style' });
            dataTable.addColumn({ type: 'date', id: 'Start' });
            dataTable.addColumn({ type: 'date', id: 'End' });

            let rows = [];
            let colors = [];

            for (let i = 0; i < shifts.length; i++)
            {
                const shift = shifts[i];
                const clinic = shift.clinic.title;
                let color;
                let index;

                if (colors.includes(clinic))
                {
                    index = colors.indexOf(clinic);
                }
                else
                {
                    colors.push(clinic);
                    index = colors.length - 1;
                }

                color = PALETTE[index];

                rows.push([shift.day, shift.areas.join(), color, new Date(0, 0, 0, shift.start[0], shift.start[1]), new Date(0, 0, 0, shift.end[0], shift.end[1])]);
            }

            const options = {
                timeline: { rowLabelStyle: {fontName: 'Helvetica', fontSize: 24 },
                barLabelStyle: { fill: "#ffffff", fontName: 'Garamond', fontSize: 14 },
                showBarLabels: false},
                chartArea: {
                    top: 6,
                    right: 6,
                    bottom: 6,
                    left: 6,
                    height: '100%',
                    width: '100%'
                },
                orientation: 'vertical',
            }
            dataTable.addRows(rows);
            chart.draw(dataTable, options);

            google.visualization.events.addListener(chart, 'select', () => {
                let index = chart.getSelection()[0].row;
                const edit = document.querySelector('.schedule__shifts');
                const shifts = edit.querySelectorAll(".shift__form");

                for (let i = 0; i < shifts.length; i++)
                {
                    shifts[i].classList.toggle('visible', i == index);
                }

                shifts[index].querySelector(".day-title").innerHTML = rows[index][0];
            });

            google.visualization.events.addListener(chart, 'onmouseover', e => {
                e.row;                 

            });
        });
    }
}

export default buildChart;
