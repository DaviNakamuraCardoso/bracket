document.addEventListener("DOMContentLoaded", () => {
    
    const userTypeButton = document.querySelector("#id_user_type"); 

    userTypeButton.onchance = () => {
        const type = this.value;
        loadForm(type);
    }
});


function loadForm(type)
{
    const rightForm = document.querySelector(`#id_${type}`);
    if (rightForm.classList.contains('hide'))
    {
        const allForms = document.querySelectorAll('.form');
        allForms.forEach(form => {
            form.classList.toggle('hide', true);
        })

        rigthForm.classList.toggle('hide', false);
    }
}