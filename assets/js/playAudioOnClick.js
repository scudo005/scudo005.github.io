var links = Array.from(document.querySelectorAll('a'));
var sound_play = document.getElementById('nav_button');
var buttons = document.getElementsByTagName('button');
sound_play.loop = false;
addEventListener("DOMContentLoaded", (event) => {
    sound_play.play();
    for (var i = 0; i < buttons.length; i++) {
        (function (i) {
            if (buttons.item(i).className === 'button_link') {
                buttons[i].onclick = function () {
                    location.href = links[i - 1];
                }
            }
        }(i));
    }
});
// not working
sound_play.addEventListener("ended", (event) => {
    new AbortController().abort('stopped reloading');
    sound_play.remove();
})
