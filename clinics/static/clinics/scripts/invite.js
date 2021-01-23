document.addEventListener("DOMContentLoaded", () => {
    const button = document.querySelector("#invite"); 


    button.onclick = () => {
        inviteHandler(button);
    }
});


function inviteHandler(button)
{
    button.style.pointerEvents = "none";
    let value = button.dataset.val;
    let isInvite; 
    if (value == "accept")
    {
        isInvite = true; 
    }
    else 
    {
        isInvite = false;
    }

    fetch(button.dataset.url, {
        method: "PUT", 
        body: JSON.stringify({
            invite: isInvite 
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result.message);
        if (value == "accept")
        {
            button.dataset.val = "deny";
            button.innerHTML = "Cancel Invitation";
        }
        else 
        {
            button.dataset.val = "accept"; 
            button.innerHTML = "Invite";
        }
        
    });

    button.style.pointerEvents = "auto";

}