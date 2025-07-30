req = new XMLHttpRequest();
req.open("GET", "https://scudo-count.bruschetta.cc/count");
req.setRequestHeader("Accept", "application/json");
req.onload = () => {
    if (req.status != 201) {
        console.log('Invalid request status ' + req.status);
    }
    if (req.readyState != 4){
        console.log('Request not completed correctly. Current state:  ' + req.readyState);
    }
}
req.send();
vis = '';
try{
    vis = JSON.parse(req.responseText);
}
catch (SyntaxError){
    console.log('Invalid JSON data: ' + req.responseText);
    document.getElementById('main').appendChild(document.createElement('p').appendChild(document.createTextNode('Something went wrong. See the browser console for details.')));
}
document.getElementById('main').appendChild(document.createElement('p').appendChild(document.createTextNode(vis)));
