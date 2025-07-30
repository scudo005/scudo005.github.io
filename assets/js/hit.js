// add this code to every page when CORS problem is resolved
req = new XMLHttpRequest();
req.open("POST", "https://scudo-count.bruschetta.cc/increment");
req.setRequestHeader("Content-Type", "application/json");
req.send('{"key":"2Z0GxYUE3xNXTF2B"}');
if (req.responseText != 'success'){
    console.log('increment fail. http status ' + req.status +' request state ' + req.readyState);
}