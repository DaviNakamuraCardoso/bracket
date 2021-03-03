document.addEventListener("DOMContentLoaded", eventListener);
window.onpopstate = function(event) {
    showTab(event.state.section);
}


function eventListener()
{

    let hrefArray = window.location.href.split('/');
    const navItems = document.querySelectorAll('.profile-nav-item');

    for (let i=0; i < navItems.length; i++)
    {
        let item = navItems[i];
        item.addEventListener('click', () => {

            showTab(i);
        });
    }
    const paths = ['', '/about', '/ratings'];
    const tab = Math.max(0, paths.indexOf(`/${hrefArray[5]}`));
    showTab(tab);
}


function showTab(n)
{
    let hrefArray = window.location.href.split('/');

    const basePath = hrefArray.slice(3, 5).join('/');
    const paths = ['', '/about', '/ratings'];

    const navItems = document.querySelectorAll('.profile-nav-item');
    const tabs =  document.querySelectorAll('.tab');
    const track = document.querySelector('.bar');
    for (let i = 0; i < tabs.length; i++)
    {
        if (i == n)
        {
            tabs[i].style.display = 'block';
            navItems[i].classList.toggle('active', true);
            track.style.left = `${i*33}%`;
            history.pushState({section: n}, "", `/${basePath}${paths[n]}`);
        }
        else
        {
            tabs[i].style.display = 'none';
            navItems[i].classList.toggle('active', false);
        }
    }
}
