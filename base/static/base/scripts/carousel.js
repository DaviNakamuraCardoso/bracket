document.addEventListener("DOMContentLoaded", main);


function main()
{
    const carousels = document.querySelectorAll('.carousel');
    for (let i = 0; i < carousels.length; i++)
    {
        build(i);
        loadCurrentSlide(0, carousels[i]);
    }
}

function build(n)
{
    const pack = document.querySelectorAll(".package")[n];
    const cards = pack.querySelectorAll('.card');
    const ul = document.querySelectorAll(".carousel__track")[n];
    const nav = document.querySelectorAll(".carousel__nav")[n];
    const carousel = document.querySelectorAll(".carousel")[n];

    pack.style.display = 'none';
    carousel.style.height = `${1.8 * parseInt(window.getComputedStyle(cards[0]).height, 10)}px`;


    if (cards.length > 0)
    {
        resizeCards(pack, cards, ul, nav);
        loadCurrentSlide(0, carousel);
    }

    window.addEventListener('resize', () => {
        if (cards.length > 0)
        {
            resizeCards(pack, cards, ul, nav);
            loadCurrentSlide(0, carousel);
        }
    });
}


function resizeCards(pack, cards, ul, nav)
{

    let width = document.querySelector(".carousel__track").offsetWidth;
    let cardWidth = 1.2 * parseInt(window.getComputedStyle(cards[0]).width, 10);

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


function loadCurrentSlide(n, carousel)
{
    const prevButton = carousel.querySelector(".carousel__button--left");
    const nextButton = carousel.querySelector(".carousel__button--right");
    const slides = carousel.querySelectorAll(".carousel__slide");
    const dots = carousel.querySelectorAll(".carousel__indicator");

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
        loadCurrentSlide(n+1, carousel);
    }
    prevButton.onclick = () => {
        loadCurrentSlide(n-1, carousel);
    }
    for (let i = 0; i < dots.length; i++)
    {
        dots[i].onclick = () => {
            loadCurrentSlide(i, carousel);
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
