req = new XMLHttpRequest();
req.open("GET", "https://scudo-count.bruschetta.cc/count");
req.setRequestHeader("Accept", "application/json"); // server always has this header
req.onload = () => { // checking server and request status
    if (req.status != 200) {
        console.log('Invalid request status ' + req.status);
    }
    if (req.readyState != 4){
        console.log('Request not completed correctly. Current state:  ' + req.readyState);
    }
}
req.send(); // sending get request
req.addEventListener('loadend', show); // wait for it to finish loading
function show(){
    console.log('server response: ' + req.response)
    if (req.response === ''){
            document.getElementById('main').appendChild(document.createElement('p').appendChild(document.createTextNode('Something went wrong. See the browser console for details.')));
    }
    document.getElementById('main').appendChild(document.createElement('p').appendChild(document.createTextNode(req.response)));
}


