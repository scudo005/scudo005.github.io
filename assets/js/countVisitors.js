req = new XMLHttpRequest();
req.open("GET", "https://scudo-count.bruschetta.cc/count");
req.setRequestHeader("Accept", "application/json");
req.onload = () => {
    if (req.readyState === 4 && req.status === 201) {
        // add this when the CORS problem is fixed.
        //document.getElementById('main').appendChild(document.createElement('p').appendChild(document.createTextNode(req.responseText + req.status)));
        console.log(JSON.parse(req.responseText));
        console.log(req.status);
    }
    else {
        console.log("error:");
        console.log(req.status);
    }
}
req.send();
