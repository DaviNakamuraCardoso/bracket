document.addEventListener("DOMContentLoaded", updateSidebar);


function updateSidebar()
{
    const burger = document.querySelector("#sidebar__button");
    burger.onclick = open;

}

function open()
{
    const sidebar = document.querySelector("#sidebar");
    const burger = document.querySelector("#sidebar__button-content");
    const main = document.querySelector("#main");
    sidebar.classList.toggle('open');
    burger.classList.toggle('open');
    main.classList.toggle('open');

}
