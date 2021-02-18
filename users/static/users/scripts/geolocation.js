/**
* @name setPosition
* @function
* @global
* @param {Object} position - Object containing the info about the user location
* @return {void} - Selects the city input datalist and fills with the results
*/
export default function setPosition(position)
{
    // Get both coordinates we need
    let lat = position.coords.latitude;
    let lng = position.coords.longitude;

    // Fetches our own API for a list of the nearest cities
    fetch(`/auth/location/${lat}/${lng}`)

    // Parse the response to JSON data
    .then(response => response.json())

    // Adds the results to the datalist
    .then(result => {
        // Get the list of cities
        const cities = result.cities;

        // Get the form and the select fields
        const form = document.querySelector("form");
        const selects = document.querySelectorAll(".city-field");

        // For each input field adds all the cities
        selects.forEach(select => {

            // For each city, creates an element and adds it
            cities.forEach(city => {

                // Creates an option element for each city
                const option = document.createElement('option');
                option.innerHTML = city['city'];
                option.value = city['id'];

                // Adding the element to the select field
                select.add(option);

            });

        });

    })

}
