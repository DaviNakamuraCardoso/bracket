document.addEventListener("DOMContentLoaded", () => 
{
    const icons = document.querySelectorAll(".icon");


    icons.forEach(icon => {
    
        const box = icon.parentElement.lastElementChild;
        icon.addEventListener('click', () => {
            box.classList.toggle('open');
            
        });
        box.onmouseover = () => {
            document.removeEventListener('click');
        
        }
        box.onmouseout = () => {
            document.addEventListener('click', () => {
                box.classList.remove('open');
            });
        }



    });
        const notificationsLength = document.querySelectorAll('.notifi-item').length;

    if (notificationsLength > 0)
    {
        const number = document.querySelector('.notifi-number');
        number.innerHTML = notificationsLength;
    }
    

});


        