document.addEventListener("DOMContentLoaded", () => {

    const checkBoxes = document.querySelectorAll(".checkbox-input");
    const nextButton = document.querySelector("#next"); 
    const formContainer = document.querySelector("#form-container"); 
    const container = document.querySelector('#container'); 
    nextButton.onclick = () => {

        let index = 0;
        checkBoxes.forEach(checkBox => {
            if (checkBox.checked)
            {
                const day = checkBox.parentElement.querySelector('.checkbox-span').innerHTML; 
                const mainDiv = document.createElement('div');
                const button = document.createElement("button"); 
                const cp = copyElement(formContainer, day, index); 
                const dayContainer = document.createElement('div'); 
                const input = document.createElement('input'); 

                mainDiv.id = day; 
                input.type = "hidden"; 
                input.value = index+1;

                dayContainer.className = "day-container";

                button.type = 'button'; 
                button.innerHTML = `New Shift for ${day}`; 
                button.onclick = () => {
                    index++; 
                    input.value = index+1;
                    
                    dayContainer.append(copyElement(formContainer, day, index)); 
                }

                
                dayContainer.append(cp);
                
                mainDiv.append(dayContainer); 
                mainDiv.append(input); 
                mainDiv.append(button); 
                container.append(mainDiv); 
            }
        });
    }
    
});

function copyElement(element, tag, index)
{
    const newElement = element.cloneNode(true);
    const descendents = newElement.getElementsByTagName("*");
    for (var i = 0; i < descendents.length; i++)
    {
        var e = descendents[i];
        if (e.id)
        {
            e.id = `${e.id}_${tag}_${index}`;
            e.name = `${e.name}_${tag}_${index}`

        }
    }
    newElement.querySelector('.day-title').innerHTML = `${tag} 0${index+1}`;
    
    newElement.id = `${tag}_${index}`;
    newElement.className = "day-card";

    return (newElement);

}

