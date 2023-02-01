magicButton = document.getElementById("magic-button");
magicModal = document.getElementById("nav-content");
magicListener = magicButton.addEventListener("click", toggleMagicModal);

listButton = document.getElementById("list-add");
listModal = document.getElementById("list-modal");
listArticle = document.getElementById("list-article");
listListener = listButton.addEventListener("click", toggleListModal);

listClose = document.getElementById("list-close");
listCloseListener = listClose.addEventListener("click", toggleListModal);

function killModal(modal) {
    if (modal == magicModal) {
        magicButton.classList.remove('nav-profile-active');
    }

    modal.classList.add('invisible');
    modal.classList.remove('visible');
}

function toggleMagicModal() {
    toggleModal(magicModal)
}

function toggleListModal() {
    toggleModal(listModal)
}

function toggleModal(modal) {
    if (modal == magicModal) {
        magicButton.classList.add('nav-profile-active');
    }
    if (modal.classList.contains('invisible') == true) {
        modal.classList.add('visible');
        modal.classList.remove('invisible');
    } else {
        killModal(modal);
    }
}

/* out-of-focus click handling */
/* killModal is invoked pre-emptively */

document.addEventListener('click', event => {
    const magicButtonClick = magicButton.contains(event.target);
    const magicModalClick = magicModal.contains(event.target);

    const listButtonClick = listButton.contains(event.target);
    const listArticleClick = listArticle.contains(event.target);

    if (!magicButtonClick && !magicModalClick) {
        killModal(magicModal);
    }

    if (!listButtonClick && !listArticleClick) {
        killModal(listModal);
    }

})

document.addEventListener("keydown", ({key}) => {
    if (key === "Escape") {
        killModal(magicModal);
        killModal(listModal);
    }
})

