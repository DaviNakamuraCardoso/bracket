document.addEventListener("DOMContentLoaded", () => {

    // Get the reply buttons
    const replyButtons = document.querySelectorAll('.notifi-reply-btn');

    // For all of them, 
    replyButtons.forEach(replyButton => {
        listenForReply(replyButton);
    });
});


function listenForReply(replyButton) 
{
        // Value can be 'accept' or 'deny' 
        const value = replyButton.dataset.val;

        // The answer is true if the value is equal to 'accept', else false
        var answer = ((value == 'accept') ? true : false);

        // When a button is clicked, send a PUT request to the server, with the answer
        replyButton.onclick = () => {
            fetch(replyButton.dataset.url, {
                method: "PUT", 
                body: JSON.stringify({
                    confirm: answer 
                })
            })
            .then(response => response.json())
            .then(result => {
                console.log(result.message);
                const dropItem = replyButton.parentElement.parentElement.parentElement;
                dropItem.style.display = 'none';

            });
        }
}
