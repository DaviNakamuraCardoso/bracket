document.addEventListener("DOMContentLoaded", () => {

    const replyButtons = document.querySelectorAll('.notifi-reply-btn');

    replyButtons.forEach(replyButton => {
        // Value can be accept or deny 
        const value = replyButton.dataset.val;

        // The answer is true if the value is equal to 'accept', else false
        var answer = ((value == 'accept') ? true : false)

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
    });
});


function hide(element)
{
    element.style.animationName = 'hide'; 
    element.style.animationPlayState = 'running';
    element.addEventListener('animationend', () => {
        element.style.display = 'none';
    });
}