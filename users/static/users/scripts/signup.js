import positions from './geolocation.js';

function main()
{
    navigator.geolocation.getCurrentPosition(positions);
}

main();
