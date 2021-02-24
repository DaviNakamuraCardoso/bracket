document.addEventListener("DOMContentLoaded", updateSidebar);


function updateSidebar()
{
    const navItems = document.querySelectorAll('.accordeon');
    const burger = document.querySelector("#sidebar__button");
    for (let i = 0; i < navItems.length; i++)
    {
        let navItem = navItems[i];
        let navHeader = navItem.querySelector('.navbar-button');
        navHeader.onclick = () => {
            let navContent = navItem.querySelector('.nav-content');
            navContent.classList.toggle('open');
            navHeader.classList.toggle('active');


        }
    }

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
