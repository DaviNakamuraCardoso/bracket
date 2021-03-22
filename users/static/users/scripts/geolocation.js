/**
* @name locations
* @function
* @global
* @param {Object} position - Object containing the info about the user location
* @return {void} - Selects the city input datalist and fills with the results
*/
function locations(position)
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
        const selects = document.querySelectorAll(".location__select");
        selects.forEach(select => {select.innerHTML = '';});
        // For each input field adds all the cities
        selects.forEach(select => {

            // For each city, creates an element and adds it
            cities.forEach(city => {

                // Creates an option element for each city
                const option = document.createElement('option');
                option.innerHTML = `${city['city']}, ${city['state_id']}`;
                option.value = city['id'];

                // Adding the element to the select field
                select.append(option);

            });
            select.focus();
        });
    });
};


function getLocations(form, card)
{
    //
    const searchBox = form.querySelector(".location__search");
    const search = searchBox.value;
    const datalist = card.querySelector(".location__select");

    // Fetch the cities API
    fetch(`${form.action}?city=${search}`)

    // Parse the response to JSON data
    .then(response => response.json())

    // Get the returned cities
    .then(cities => {
        datalist.innerHTML = '';

        for (let i = 0; i < cities.length; i++)
        {
            let option = document.createElement('option');

            option.innerHTML = `${cities[i].city}, ${cities[i].state_id}`;
            option.value = cities[i].id;


            datalist.append(option);
        }
        datalist.focus();

        return (false);

    });
    return false;
};


function main()
{
    // Get all the location pickers
    const containers = document.querySelectorAll(".location__picker");

    for (let i = 0; i < containers.length; i++)
    {
        const container = containers[i];
        const button = container.querySelector('.location__button');
        const select = container.querySelector(".location__select");

        // Card and wrapper
        const card = container.querySelector(".location__card");
        const wrapper = container.querySelector(".location__wrapper");

        // Buttons
        const myLocation = card.querySelector(".location__use");
        const search = card.querySelector('.location__form');
        const confirm = card.querySelector(".location__confirm");

        // Show the card when the button is clicked
        button.onclick = () => { wrapper.classList.toggle('location__wrapper--show', true); };
        myLocation.onclick = () => { navigator.geolocation.getCurrentPosition(locations); };
        search.onsubmit = () => { return getLocations(search, container); };
        confirm.onclick = () => {
            wrapper.classList.toggle('location__wrapper--show', false);

            button.querySelector(".location__text").innerHTML = select.options[select.selectedIndex].innerHTML || 'Select your city';

        };


    }
};

main();
