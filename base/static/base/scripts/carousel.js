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
    const carousel = document.querySelector(".carousel");

    pack.style.display = 'none';


    resizeCards(pack, cards, ul, nav);
    loadCurrentSlide(0);

    window.onresize = () => {
        resizeCards(pack, cards, ul, nav);
        loadCurrentSlide(0); 

    };


}


function resizeCards(pack, cards, ul, nav)
{

    let width = document.querySelector(".carousel").offsetWidth;
    let cardWidth = 1.7 * parseInt(window.getComputedStyle(cards[0]).width, 10);

    ul.innerHTML = '';
    nav.innerHTML = '';

    // Prevent floating points or zero divisions
    let numberOfCards = Math.max(1, Math.floor(width / cardWidth));


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
