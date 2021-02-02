document.addEventListener("DOMContentLoaded", () => {

    const checkBoxes = document.querySelectorAll(".day-input");
    const nextButton = document.querySelector("#next"); 
        checkBoxes.forEach(checkBox => {
            if (checkBox.checked)
            {
                console.log(checkBox.value);                
            }
        });
        
    updateTimePickers(); 

});


function updateTimePickers() 
{
    const pickers = document.querySelectorAll('.picker'); 
    pickers.forEach(picker => {
        picker.addEventListener('change', () => {

            let date = picker.value; 
            picker.parentElement.querySelector(".time").value = date;
        });

    }); 
}