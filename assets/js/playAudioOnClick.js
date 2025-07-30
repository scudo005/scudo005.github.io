var links = Array.from(document.querySelectorAll('a'));
var sound_play = document.getElementById('nav_button');
var buttons = document.getElementsByTagName('button');

// this check works only on Firefox; on Chromium, it just plays the sound.
if (navigator.getAutoplayPolicy(sound_play) === 'allowed') {
    sound_play.play();
}

if (navigator.userAgent.includes("Mozilla/5.0 (Android")) {
    var domBody = document.getElementById('main');
    var warnBox = document.createElement('p');
    var warnTxt = document.createTextNode('Warning: this site is currently broken under Firefox for Android, and I do not know why. For an optimal experience on mobile, please use a Chromium-based browser.');
    warnBox.appendChild(warnTxt);
    domBody.appendChild(warnBox);
}

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
