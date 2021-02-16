
document.addEventListener("DOMContentLoaded", eventListener); 

function eventListener()
{
    const navItems = document.querySelectorAll('.profile-nav-item'); 
    for (let i=0; i < navItems.length; i++)
    {
        let item = navItems[i]; 
        console.log(item); 

        item.addEventListener('click', () => {
            showTab(i); 


        });
    }
    showTab(0); 
}


function showTab(n)
{
    const tabs =  document.querySelectorAll('.tab'); 
    const track = document.querySelector('.bar'); 
    for (let i = 0; i < tabs.length; i++)
    {
        if (i == n)
        {
            tabs[i].style.display = 'block'; 
            track.style.left = `${i*33}%`; 
        }
        else 
        {
            tabs[i].style.display = 'none'; 
        }
    }


}