if (document.cookie === '') {
    document.cookie = "session=yes";
    req = new XMLHttpRequest();
    req.open("POST", "https://scudo-count.bruschetta.cc/increment");
    req.setRequestHeader("Content-Type", "application/json");
    req.send('{"key":"2Z0GxYUE3xNXTF2B"}');
    req.addEventListener('loadend', function () {
        if (req.response != 'Count incremented') {
            console.log('increment fail. http status ' + req.status + ' request state ' + req.readyState + ' response ' + req.response);
        }
    })
}
