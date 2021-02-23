document.addEventListener("DOMContentLoaded", main);



function main()
{
    build();
    loadCurrentSlide(0);

}

function build()
{
    const pack = document.querySelector("#package");
    const cards = pack.querySelectorAll('.card');
    const ul = document.querySelector(".carousel__track");
    const nav = document.querySelector(".carousel__nav");

    pack.style.display = 'none';


    loadCurrentSlide(0);
    resizeCards(pack, cards, ul, nav);

    window.onresize = () => {
        resizeCards(pack, cards, ul, nav);
        loadCurrentSlide(0);

    };


}


function resizeCards(pack, cards, ul, nav)
{

    ul.innerHTML = '';
    nav.innerHTML = '';
    let width = window.innerWidth;
    let numberOfCards = Math.floor(width / 400);


    for (let i = 0; i < cards.length / numberOfCards; i++)
    {
        let li = document.createElement('li');
        let indicator = document.createElement('button');

        li.className = "carousel__slide";
        indicator.className = "carousel__indicator";


        for (let j = 0; j < numberOfCards; j++)
        {
            if (i*numberOfCards + j < cards.length)
            {
                li.append(cards[i*numberOfCards + j]);

            }
        }
        if (i === 0)
        {
            indicator.classList.toggle('current-slide', true);
        }

        ul.append(li);
        nav.append(indicator);

    }


}


function loadCurrentSlide(n)
{
    const prevButton = document.querySelector(".carousel__button--left");
    const nextButton = document.querySelector(".carousel__button--right");
    const slides = document.querySelectorAll(".carousel__slide");
    const dots = document.querySelectorAll(".carousel__indicator");

    for (let i = 0; i < slides.length; i++)
    {
        slides[i].style.left = `${(i-n) * 100}%`;
        dots[i].classList.toggle('current-slide', i==n);

    }


    show(prevButton);
    show(nextButton);

    if (n === 0)
    {
        hide(prevButton);
    }

    if (n === slides.length-1)
    {
        hide(nextButton);
    }

    nextButton.onclick = () => {
        loadCurrentSlide(n+1);
    }
    prevButton.onclick = () => {
        loadCurrentSlide(n-1);
    }
    for (let i = 0; i < dots.length; i++)
    {
        dots[i].onclick = () => {
            loadCurrentSlide(i); 
        }

    }



}

function hide(element)
{
    element.style.pointerEvents = 'none';
    element.style.opacity = 0;

}

function show(element)
{
    element.style.pointerEvents = 'auto';
    element.style.opacity = 1;
}
