document.addEventListener("DOMContentLoaded", () => 
{
    const icons = document.querySelectorAll(".icon");
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


        