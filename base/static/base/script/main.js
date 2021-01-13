document.addEventListener("DOMContentLoaded", () => 
{
    const box = document.querySelector("#box");
    const bell = document.querySelector("#bell");

    bell.addEventListener('click', () => {
        box.classList.toggle('open');
    });

});


        