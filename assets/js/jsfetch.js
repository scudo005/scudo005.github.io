// neofetch: os, kernel, uptime, packages, shell, terminal, cpu, gpu, memory
// jsfetch: os (es. Windows), os version if on windows (i doubt kernel ver can be obtained on linux/macos), uptime=no, pack=no,
// shell=browser info (es. Firefox 69), terminal=Navigator.connection.type+Navigator.devicePosture, cpu=Navigator.oscpu/Navigator.userAgent+Navigator.hardwareConcurrency,
// gpu = navigator.gpu, memory = navigator.deviceMemory*1024
let sys = "oscpu: " + navigator.oscpu + "\nua: " + navigator.userAgent + "\ncores:" + navigator.hardwareConcurrency + "\ngpu: " + navigator.gpu + "\nmem: " + navigator.deviceMemory;
document.getElementById('main').appendChild(document.createTextNode(sys));

if (navigator.userAgent.search('x64') != -1){
    document.getElementById('main').appendChild(document.createTextNode('You are running on a '));
}