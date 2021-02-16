import setPosition from './geolocation.js'; 


function documentEvents()
{
    navigator.geolocation.getCurrentPosition(setPosition); 

}

document.addEventListener("DOMContentLoaded", documentEvents); 