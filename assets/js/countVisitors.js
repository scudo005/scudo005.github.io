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
    //if (req.response === '') {
       // jsc.parentNode.appendChild(document.createElement('p').appendChild(document.createTextNode('Something went wrong. See the browser console for details.')));
       // jsc.remove(); // TODO: why is this breaking the page?
    //}
    jsc.appendChild(document.createTextNode(req.response));
});
