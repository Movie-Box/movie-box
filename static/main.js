// Nav Bar
document.addEventListener('DOMContentLoaded', () => {

    // Get all "navbar-burger" elements
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

    // Check if there are any navbar burgers
    if ($navbarBurgers.length > 0) {

        // Add a click event on each of them
        $navbarBurgers.forEach(el => {
            el.addEventListener('click', () => {

                // Get the target from the "data-target" attribute
                const target = el.dataset.target;
                const $target = document.getElementById(target);

                // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
                el.classList.toggle('is-active');
                $target.classList.toggle('is-active');

            });
        });
    }

});
// Navbar End

// BacttoTop
const button = document.querySelector("#back2top");
BACK2TOP(button, 200);

function BACK2TOP(selector, offset, prop = 'all', time = '300', effect = 'ease', delay = 0) {
    const WIN_SCROLLED = function () {
        if (document.body.scrollTop > offset || document.documentElement.scrollTop > offset) {
            const STYLES = {
                opacity: '1',
                visibility: 'visible',
                transform: 'translateY(0)',
                transition: `${prop} ${time}ms ${effect} ${delay}ms`
            }
            Object.assign(selector.style, STYLES);

        } else {
            const STYLES = {
                opacity: '0',
                visibility: 'hidden',
                transform: 'translateY(100%)',
                transition: `${prop} ${time}ms ${effect} ${delay}ms`
            }
            Object.assign(selector.style, STYLES);
        }
    };

    const SCROLL_EVT = function () {

        document.documentElement.scrollTo({
            top: 0,
            left: 0,
            behavior: 'smooth'
        });


    };

    //Target Element i.e Button
    const SELECTOR_LISTENER = selector.addEventListener("click", SCROLL_EVT);

    //Target Element i.e Button Show/Hide on scroll
    const WINDOW_LISTENER = window.addEventListener('scroll', WIN_SCROLLED);

    return SELECTOR_LISTENER;
    return WINDOW_LISTENER;
}
// BacttoTop End 