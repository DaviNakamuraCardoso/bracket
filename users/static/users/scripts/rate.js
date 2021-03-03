document.addEventListener("DOMContentLoaded", main);

function main()
{
    removeExtraForms();
    updateStars();
}


function updateStars()
{
    const stars = document.querySelectorAll('.star__input');

    for (let i = 0; i < stars.length; i++)
    {
        // Event listener when the star is clicked
        stars[i].onchange = () =>
        {
            // Setting all the other starboxes to unchecked
            for (let j = 0; j < stars.length; j++)
            {
                if (j != i)
                {

                    stars[j].checked = false;
                }
            }
        }
    }
}

function removeExtraForms()
{
    const forms = document.querySelectorAll('.rate__form');
    for (let i = 0; i < forms.length-1; i++)
    {
        forms[i].remove();
    }
}
