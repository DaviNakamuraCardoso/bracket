function main()
{
    const email = document.querySelector('.login__button--email');
    email.onclick = login;
}


function login()
{
    const oauth = document.querySelector(".login__oauth");
    oauth.style.display = 'none';

    const form = document.querySelector(".login__email");
    form.style.display = 'flex';
    form.querySelector("#id_username").focus(); 
}


document.addEventListener("DOMContentLoaded", main);
