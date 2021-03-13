document.addEventListener("DOMContentLoaded", main);

function main()
{
    removeExtraForms();
    updateStars();
    formSubmissions();

    let page = loadRates(0);



}


function updateStars()
{
    const stars = document.querySelectorAll('.star__input');

    for (let i = 0; i < stars.length; i++)
    {
        // Event listener when the star is clicked
        stars[i].onchange = () =>
        {
            // Setting all the other starboxes to unchecked
            for (let j = 0; j < stars.length; j++)
            {
                if (j != i)
                {

                    stars[j].checked = false;
                }
            }
        }
    }
}


function removeExtraForms()
{
    const forms = document.querySelectorAll('.rate__form');
    for (let i = 0; i < forms.length-1; i++)
    {
        forms[i].remove();
    }
}


function formSubmissions()
{
    const forms = document.querySelectorAll('.rate__form');
    for (let i = 0; i < forms.length; i++)
    {
        forms[i].onsubmit = () => {
            return rate(forms[i])
        };

    }


}


function rate(form)
{
    const csrftoken = form.querySelector("[name=csrfmiddlewaretoken]").value;
    const request = new Request(
        form.action,
        {headers:{"X-CSRFToken": csrftoken}}
    );

    const body = form.querySelector(".rate__body");
    const stars = form.querySelectorAll(".star__input");
    const isDoctor = form.querySelector(".rate__is-doctor").value == 1;

    let rate;

    for (let i = 0; i < stars.length; i++)
    {
        if (stars[i].checked)
        {
            rate = stars.length - i;
            break;
        }
    }

    fetch(request, {
        method: 'POST',
        body: JSON.stringify({
            body: body.value,
            rate: rate,
            is_doctor: isDoctor
        })
    })
    .then(response => response.json())
    .then(result => {
        const rate = result.rate;

        const comments = document.querySelector('.comments');
        comments.prepend(element(rate));

        form.remove();
        return (false);

    });
    return (false);
}

function serialize(node)
{
    let serialized = {};
    const children = node.getElementsByTagName("*");

    for (let i = 0; i < children.length; i++)
    {
        let name = children[i].className.split("__")[1];
        serialized[name] = children[i];
    }

    return (serialized);
}


function element(rate)
{

    const template = document.querySelector("#comment").content.cloneNode(true);
    const children = serialize(template.children[0]);

    children['user'].innerHTML = rate.user.title;
    children['picture'].src = rate.user.image;

    children['comment'].innerHTML = rate.comment;
    children['time'].innerHTML = rate.time;

    const star = document.createElement('div');
    const deadStar = document.createElement('div');

    deadStar.className = 'fas-icon star dead__star';
    star.className = 'fas-icon star';

    for (let i = 0; i < 5; i++)
    {
        if (i < rate.rate)
        {
            children['stars'].append(star.cloneNode(true));
        }
        else
        {
            children['stars'].append(deadStar.cloneNode(true));
        }
    }


    const comments = document.querySelector(".comments");

    return (template.children[0]);
}


function loadRates(page)
{
    window.onscroll = undefined;

    const container = document.querySelector('.comments');
    const url = container.dataset.url;

    fetch(`${url}/${page}`)
    .then(response => response.json())
    .then(result => {
        const rates = result.rates;
        for (let i = 0; i < rates.length; i++)
        {
            container.append(element(rates[i]));
        }
        window.onscroll = () => {

            if (window.innerHeight + window.scrollY >= document.body.offsetHeight + window.innerHeight * 0.12)
            {
                loadRates(page+1)
            }

        }

    });

}
