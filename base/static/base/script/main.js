document.addEventListener("DOMContentLoaded", () => 
{
    const icons = document.querySelectorAll(".icon");


    icons.forEach(icon => addIconListeners(icon));
    
    const notificationsLength = document.querySelectorAll('.notifi-item').length;

    if (notificationsLength > 0)
    {
        const number = document.querySelector('.notifi-number');
        number.innerHTML = notificationsLength;
    }
    

});


function toggleClass(box) 
{
    box.classList.toggle('open');
}


function removeClass(box)
{
    box.classList.remove('open');
}

function addIconListeners(icon)
{
    const box = icon.parentElement.lastElementChild;

    icon.onclick = () => {
        toggleClass(box);
    }

}
        