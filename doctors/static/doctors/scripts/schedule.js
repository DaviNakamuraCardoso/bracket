document.addEventListener("DOMContentLoaded", () => {

    const nextButton = document.querySelector("#next"); 
    
    nextButton.onclick = updateAllCards; 


           
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
    newElement.querySelector('.day-title').innerHTML = `${tag} 0${index}`;
    
    newElement.id = `${tag}_${index}`;
    newElement.className = "day-card";

    return (newElement);

}

function updateAllCards()

{
        const days = document.querySelector("#days"); 
        const checkBoxes = document.querySelectorAll(".checkbox-input");
        const formContainer = document.querySelector("#form-container"); 
        const container = document.querySelector('#container'); 


        let daysArray = []; 
        container.innerHTML = ""; 
        checkBoxes.forEach(checkBox => {
            if (checkBox.checked)
            {
                const day = checkBox.parentElement.querySelector('.checkbox-span').innerHTML; 
                const mainDiv = document.createElement('div');
                const button = document.createElement("button"); 
                const dayContainer = document.createElement('div'); 
                const input = document.createElement('input'); 
                const cp = copyElement(formContainer, day, 1); 

                mainDiv.id = day; 
                daysArray.push(day); 
                days.value = daysArray.join();
                input.name = `${day}_num`; 
                input.id = `${day}_num`; 
                input.type = "hidden"; 
                input.value = 1; 
                
                dayContainer.className = "day-container";

                button.type = 'button'; 
                button.innerHTML = `New Shift for ${day}`; 
                button.onclick = () => {
                    input.value++;
                    
                    dayContainer.append(copyElement(formContainer, day, input.value)); 
                    updateRemovers();
                }

                
                dayContainer.append(cp);
                
                mainDiv.append(dayContainer); 
                mainDiv.append(input); 
                mainDiv.append(button); 
                container.append(mainDiv); 
                updateRemovers(); 
            }
        });

}


function updateRemovers()
{
    const removers = document.querySelectorAll('.day-close'); 
    removers.forEach(remover => {
        remover.onclick = () => {
            
            const card = remover.parentElement; 
            const day = card.id.split("_")[0]; 
            const input = document.querySelector(`#${day}_num`); 
            let value = input.value; 
            
            if (parseInt(value) == 1)
            {
                const checkBox = document.querySelector(`#checkbox_${day}`); 
                checkBox.checked = false; 
                updateAllCards(); 
                


                
            }
            else
            {
                input.value--; 
                card.remove(); 
            }

        }

    })
    


}

