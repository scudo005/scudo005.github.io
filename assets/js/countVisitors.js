jsc = document.getElementById('js-count');
req = new XMLHttpRequest();
req.open("GET", "https://scudo-count.bruschetta.cc/count");
req.setRequestHeader("Accept", "application/json");
req.onload = () => {
    if (req.status != 200) {
        console.log('Invalid request status ' + req.status);
    }
    if (req.readyState != 4) {
        console.log('Request not completed correctly. Current state:  ' + req.readyState);
    }
}
req.send();
req.addEventListener('loadend', function () {
    jsc.appendChild(document.createTextNode(req.response));
});
