document.addEventListener("DOMContentLoaded", () => {
    // Getting all the notification items
    const notifications = document.querySelectorAll('.drop__notification');
    for (let i = 0; i < notifications.length; i++)
    {
        notifications[i].onclick = () => {
            toggleNotification(i, true);
            document.querySelector(".drop__return").onclick = () => {
                toggleNotification(i, false); 
            }
        }
    }

    // Get the reply buttons
    const replyButtons = document.querySelectorAll('.drop__button');

    // For all of them,
    replyButtons.forEach(replyButton => {
        listenForReply(replyButton);
    });
});


function listenForReply(replyButton)
{
    // Notification container
    const dropItem = replyButton.parentElement.parentElement.parentElement;

    // Value can be 'accept' or 'deny'
    const value = replyButton.dataset.val;

    // The answer is true if the value is equal to 'accept', else false
    const answer = ((value == 'accept') ? true : false);
    const object_id = document.querySelector('#object-id').value;
    const origin = dropItem.querySelector(".drop__title").innerHTML;

    // Prevent Cross-site forgery
    const token = document.querySelector("[name=csrfmiddlewaretoken]").value;
    const request = new Request(
        replyButton.dataset.url,
        {headers: {"X-CSRFToken": token}}
    );

    // When a button is clicked, send a PUT request to the server, with the answer
    replyButton.onclick = () => {
        fetch(request, {
            method: "PUT",
            mode: 'same-origin',
            body: JSON.stringify({
                origin: origin,
                accept: answer,
                object_id: object_id
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result.message);
            dropItem.remove();


        });
    }
}


function loadNotifications()
{
    const url = document.querySelector()
}


function toggleNotification(index, open)
{
    const back = document.querySelectorAll(".drop__back")[index];
    const second = document.querySelector('.drop__second');
    const others = document.querySelector('.drop__first');

    second.classList.toggle('open', open);
    back.classList.toggle('open', open);
    others.classList.toggle('closed', open);
}
