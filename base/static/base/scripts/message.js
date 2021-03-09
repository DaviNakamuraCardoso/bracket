
export default function ping(message)
{
    const div = document.createElement('div');
    const html = document.querySelector('html');

    div.innerHTML = message;
    div.className = "ping";

    html.append(div); 




}
