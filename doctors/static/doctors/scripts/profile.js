document.addEventListener("DOMContentLoaded", () => {
    const invite = document.querySelector('#invite');
    invite.onclick = () => {
        invite.classList.toggle('clicked');
    }
});