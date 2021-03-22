document.addEventListener("DOMContentLoaded", () =>
{
    const icons = document.querySelectorAll(".icon");
    const drops = document.querySelectorAll(".dropdown");
    drops.forEach(drop => addDropListener(drop));
    icons.forEach(icon => addIconListeners(icon));

    document.addEventListener('click', () => {

        const e = window.event;
        const x = e.clientX;
        const y = e.clientY;

        const element = document.elementFromPoint(x, y);

        if (!element.classList.contains('drop'))
        {
            closeAllDrops(icons);
        }

    });



});


function toggleClass(box)
{
    box.classList.toggle('open');
}

function addDropListener(drop)
{
    const children = drop.getElementsByTagName("*");
    for (let i = 0; i < children.length; i++)
    {
        children[i].classList.add('drop');
    }
    drop.classList.add('drop');
}

export default function dropNode(drop)
{
    addDropListener(drop);
}


function removeClass(box)
{
    box.classList.toggle('open', false);
}

function closeAllDrops(icons)
{
    icons.forEach(icon => {
        let box = icon.parentElement.lastElementChild;
        removeClass(box);
    });
}


function addIconListeners(icon)
{
    const box = icon.parentElement.lastElementChild;

    icon.onclick = () => {
        toggleClass(box);
    }

}
