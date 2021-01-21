document.addEventListener("DOMContentLoaded", () => {

    const replyButtons = document.querySelectorAll('.notifi-reply-btn');

    replyButtons.forEach(replyButton => {
        let answer; 
        if (replyButton.dataset.val == 'accept')
        {
            answer = true;
        }
        else 
        {
            answer = false;
        }

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
            });
        }
    });
});