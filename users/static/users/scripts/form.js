function main()
{
    // Get all forms in the page
    const forms = document.querySelectorAll('.form__form');

    // Loop over each form
    for (let i = 0; i < forms.length; i++)
    {
        // Add event listener on submission
        forms[i].onsubmit = () =>
        {

        }
    }
}


function serialize(form)
{
    let data = {};
    const inputs = forms.querySelectorAll('input');
    for (let i = 0; i < inputs.length; i++)
    {
        data[inputs[i].name] = inputs[i].value;
    }

    return (JSON.stringify(data));
}
