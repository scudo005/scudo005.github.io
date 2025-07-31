var sound_play = document.getElementById('nav_button');
var buttons = document.getElementsByTagName('button');
sound_play.loop = false;
addEventListener("DOMContentLoaded", (event) => {
    sound_play.play();
    for (var i = 0; i < buttons.length; i++) {
        (function (i) {
            if (buttons.item(i).className === 'button_link') {
                buttons[i].onclick = function () {
                    location.href = buttons.item(i).getAttribute("--href");
                }
            }
        }(i));
    }
});
