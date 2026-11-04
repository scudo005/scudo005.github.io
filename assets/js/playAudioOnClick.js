var sound_play = document.getElementById('nav_button');
var buttons = document.getElementsByTagName('button');
sound_play.loop = false;
addEventListener("DOMContentLoaded", (event) => {
    try {
        sound_play.play();
    } catch (err) {
        // Blink sucks, so it ignores this try-catch block and craps its pants.
        document.getElementById('main').appendChild(document.createElement('br'))
        document.getElementById('main').appendChild(document.createElement('br'))
        document.getElementById('main').appendChild(document.createElement('h4').appendChild(document.createTextNode("If you want to experience the Windows XP click sounds, please reload the page.")))
    }

    for (var i = 0; i < buttons.length; i++) {
        (function (i) {
            if (buttons.item(i).className === 'button_link') {
                buttons[i].onclick = function () {
                    location.href = buttons.item(i).getAttribute("href");
                }
            }
        }(i));
    }
});
