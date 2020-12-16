document.addEventListener("DOMContentLoaded", () => {
    const types = document.querySelectorAll(".type");
    types.forEach(type => {
       type.onclick = function() 
        {
           showForm(this.dataset.type);  
        }
    });

});


function showForm(type)
{
    // Change the basic form style
    const basic = document.querySelector("#basic");
    basic.className = type;

    // Hide all divs besides the selected one
    const divs = document.querySelectorAll(".type");
    divs.forEach(div => {
        if (div.id != type)
        {
            div.style.display =  'none';
        }
        else 
        {
            div.style.animationName = "show";
        }

    });


}