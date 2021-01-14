document.addEventListener("DOMContentLoaded", () => 
{
    const icons = document.querySelectorAll(".icon");

    icons.forEach(icon => {
        icon.addEventListener('click', () => {
            const box = icon.parentElement.lastElementChild;
            box.classList.toggle('open');
        });



    });
        const notificationsLength = document.querySelectorAll('.notifi-item').length;

    if (notificationsLength > 0)
    {
        const number = document.querySelector('.notifi-number');
        number.innerHTML = notificationsLength;
    }
    

});


        