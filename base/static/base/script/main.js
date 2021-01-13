document.addEventListener("DOMContentLoaded", () => 
{
    const box = document.querySelector("#box");
    const bell = document.querySelector("#bell");

    bell.addEventListener('click', () => {
        box.classList.toggle('open');
    });

    const notificationsLength = document.querySelectorAll('.notifi-item').length;

    if (notificationsLength > 0)
    {
        const number = document.querySelector('.notifi-number');
        number.innerHTML = notificationsLength;
    }
    

});


        