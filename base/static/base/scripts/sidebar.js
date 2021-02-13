document.addEventListener("DOMContentLoaded", updateSidebar);


function updateSidebar()
{
    const navItems = document.querySelectorAll('.accordeon'); 
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
}
