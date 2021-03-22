
export default function ping(message)
{
    const div = document.createElement('div');
    const html = document.querySelector('html');

    div.innerHTML = message;
    div.className = "ping";

    html.append(div);
}


export class Load
{
    constructor(parent)
    {
        this.element = document.getElementById("loading__template").content.cloneNode(true).children[0];
        this.parent = parent;
        this.parent.append(this.element);
    }

    start()
    {
        this.element.classList.toggle('loading__show', true);
    }

    stop()
    {
        this.element.classList.toggle('loading__show', false);
    }

}
