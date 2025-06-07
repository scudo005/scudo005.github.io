var links = Array.from(document.querySelectorAll('a'));
var sound_play = document.getElementById('nav_button');
var buttons = document.getElementsByTagName('button');

sound_play.play();

/*if (navigator.getAutoplayPolicy(sound_play) != 'allowed') {
    alert('Please enable autoplay to hear navigation sounds.');
}*/

// magical function: I spent like an hour making this. LOL
for (var i = 0; i < buttons.length; i++) {
    (function (i) {
        if (buttons.item(i).className === 'button_link') {
            buttons[i].onclick = function () {
                setInterval(function () { location.href = links[i - 1] }, 64);
            }
        }
    }(i));
}

