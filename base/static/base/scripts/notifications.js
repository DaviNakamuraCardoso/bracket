import dropNode from './main.js';
import ping from './message.js';

let LAST = 0;


document.addEventListener("DOMContentLoaded", () => {
    LAST = update();

    const url = document.querySelector("#notification__url").value;

    setInterval(() => {
        loadNotifications(url);
    }, 10000);


});


function update()
{
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

    // For all of them, listen for replies
    for (let j = 0; j < replyButtons.length; j++)
    {
        listenForReply(replyButtons[j], Math.floor(j / 2));

    }

    const id = (notifications.length > 0) ? notifications[0].id.split("__")[1] : 0;

    return (id);

}


function listenForReply(replyButton, index)
{
    // Notification container
    const dropItem = document.querySelectorAll('.drop__back')[index];

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
            ping(result.message);
            toggleNotification(index, false);
            let dropFront = document.querySelectorAll('.drop__notification')[index];
            dropFront.remove();
            dropItem.remove();

        });
    }
}


function loadNotifications(url)
{
    const api = `${url}/${parseInt(LAST)}`;

    fetch(api)
    .then(response => response.json())
    .then(result => {
        if (result.message == "All notifications up to date.")
        {
            return;
        }

        // Containers for front and back
        const frontContainer = document.querySelector(".drop__first");
        const backContainer = document.querySelector('.drop__second');

        // Templates
        const templateFront = document.querySelector("#notification__front");
        const templateBack = document.querySelector("#notification__back");

        // Add drop for both templates, to allow clicking



        const notifications = result.notifications;

        for (let i = 0; i < notifications.length; i++)
        {
            let element = fill(templateFront, templateBack, notifications[i]);
            dropNode(element.back);
            dropNode(element.front);

            frontContainer.prepend(element.front);
            backContainer.prepend(element.back);
        }
        LAST = update();
    });

}


function fill(template1, template2, notification)
{
    // New elements for front and back
    const front = template1.content.cloneNode(true);
    const back = template2.content.cloneNode(true);


    // Serialize
    const f = serialize(front.children[0]);
    const b = serialize(back.children[0]);



    // Front
    f['title'].innerHTML =  notification.origin;
    f['timestamp'].innerHTML = notification.time;
    f['notification'].id = `notification__${notification.id}`;

    // Back text
    b['title'].innerHTML = notification.origin;
    b['text'].innerHTML = notification.text;

    // Back buttons
    b['button--deny drop'].dataset.url = notification.url;
    b['button--accept drop'].dataset.url = notification.url;
    b['input'].value = notification.object_id;

    return {
        front: front.children[0],
        back: back.children[0]
    }

}


/**
@name serialize
@function
@global
@param {Element} node - DOM Element
@returns {Object} containing all the node elements in a Object hashed by className
*/
function serialize(node)
{
    const children = node.getElementsByTagName("*");
    let serialized = {}
    for (let i = 0; i < children.length; i++)
    {
        let name = children[i].className.split('__')[1]
        serialized[name] = children[i];
    }

    let name = node.className.split('__')[1];
    serialized[name] = node;


    return (serialized);

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
