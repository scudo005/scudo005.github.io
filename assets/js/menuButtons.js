// really ugly array generation
let menu_buttons = Array.from(document.getElementsByClassName("menu-button"));
let projects = Array.from(document.getElementsByClassName("project-list"));
menu_buttons[0].setAttribute("aria-selected", "true");

for (let h = 1; h < projects.length; h++) {
    projects[h].className = 'invisible';
}

for (var i = 0; i < menu_buttons.length; i++) {
    (function (i) {
        menu_buttons[i].onclick = function () {
            menu_buttons[i].setAttribute("aria-selected", "true"); // make our button selected
            projects[i].classList.remove('invisible') // makes only one visible
            projects[i].attributes.removeNamedItem('class'); // just to be really sure
            for (var j = 0; j < menu_buttons.length; j++) {
                if (j != i) {
                    menu_buttons[j].setAttribute("aria-selected", "false"); // deselect all other buttons
                    projects[j].className = 'invisible'; // hide all other lists
                }
            }
        }
    }(i));
}
