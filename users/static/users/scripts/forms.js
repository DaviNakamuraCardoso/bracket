function main()
{
    const fields = document.querySelectorAll(".field");
    for (let i = 0; i < fields.length; i++)
    {
        let input = fields[i].querySelector('input') || fields[i].querySelector('textarea');
        console.log(input);
        validate(input);
        input.onkeyup = () => {
            validate(input);
        };
    }

}


function validate(element)
{
    element.parentElement.classList.toggle('valid__input', element.value != "");

}


document.addEventListener("DOMContentLoaded", main);
