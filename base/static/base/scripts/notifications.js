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
  // Notification container
  const dropItem = replyButton.parentElement.parentElement.parentElement;

  // Value can be 'accept' or 'deny'
  const value = replyButton.dataset.val;

  // The answer is true if the value is equal to 'accept', else false
  const answer = ((value == 'accept') ? true : false);
  const clinic_id = document.querySelector("#clinic-id").value;
  const origin = dropItem.querySelector(".drop-title").innerHTML;

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
        clinic_id: clinic_id
      })
    })
    .then(response => response.json())
    .then(result => {
      console.log(result.message);
      dropItem.style.display = 'none';

    });
  }
}





function loadNotifications()
{
    const url = document.querySelector()
}
