
const PALETTE = [
    '#4387f5',
    '#EC5272',
    '#6FFACB',
    '#996FFB'
]
function main()
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
            }
            dataTable.addRows(rows);

            chart.draw(dataTable, options);

            container.querySelectorAll('g')[3].querySelectorAll('text').forEach(text => {text.style.fill = 'white'; });

            google.visualization.events.addListener(chart, 'select', () => {
                console.log(chart.getSelection());
                console.log("Clicked");
            }); 
        });


    }
}

    document.addEventListener("DOMContentLoaded", main);
