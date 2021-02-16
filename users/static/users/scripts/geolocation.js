export default function setPosition(position)
{
    let lat = position.coords.latitude;
    let lng = position.coords.longitude;

    fetch(`/auth/location/${lat}/${lng}`)
    .then(response => response.json())
    .then(result => {
        const cities = result.cities; 
        const form = document.querySelector("form");
        const selects = document.querySelectorAll(".city-field");
        console.log(result); 
        console.log(selects); 
        selects.forEach(select => {
            cities.forEach(city => {
                const option = document.createElement('option');
                option.innerHTML = city['city'];
                option.value = city['id']; 
                select.add(option); 

            });
    
        }); 
        
    })

}