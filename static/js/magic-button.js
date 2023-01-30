magicButton = document.getElementById("magic-button");
dropdownContent = document.getElementById("nav-content");

magicListener = magicButton.addEventListener("click", toggleBurgerMenu);

function killBurgerMenu() {
    magicButton.classList.remove('nav-profile-active');
    dropdownContent.classList.add('invisible');
    dropdownContent.classList.remove('visible');
}

function toggleBurgerMenu() {
    if (dropdownContent.classList.contains('invisible') == true) {
        magicButton.classList.add('nav-profile-active');
        dropdownContent.classList.add('visible');
        dropdownContent.classList.remove('invisible');
    } else {
        killBurgerMenu();
    }
}

/* out-of-focus click handling */

document.addEventListener('click', event => {
    const magicButtonClick = magicButton.contains(event.target)
    const dropdownContentClick = dropdownContent.contains(event.target)

    if (!magicButtonClick && !dropdownContentClick) {
        killBurgerMenu()
    }  
})

document.addEventListener("keydown", ({key}) => {
    if (key === "Escape") {
        killBurgerMenu()
    }
})

