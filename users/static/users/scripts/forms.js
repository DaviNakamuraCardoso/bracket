function main()
{
    const fields = document.querySelectorAll(".field");
    for (let i = 0; i < fields.length; i++)
    {
        let input = fields[i].querySelector('input');
        validate(input);
        input.onkeyup = () => {
            validate(input);
        };
        input.onfocus = () => {
            fields[i].classList.toggle('valid__input', true);
        }
    }

}


function validate(element)
{
    element.parentElement.classList.toggle('valid__input', element.value != "");

}


document.addEventListener("DOMContentLoaded", main);
