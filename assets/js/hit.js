// add this code to every page when CORS problem is resolved
req = new XMLHttpRequest();
req.open("POST", "https://scudo-count.bruschetta.cc/increment");
req.setRequestHeader("Content-Type", "application/json");
req.onload = () => {
    if (req.readyState != 4 && req.status != 201) {
        document.getElementById('main').appendChild(document.createElement('p').appendChild(document.createTextNode("Error calling the increment API. HTTP: " + req.responseText + " status: " + req.status)));
    }
}
req.send('{"key":"2Z0GxYUE3xNXTF2B"}');