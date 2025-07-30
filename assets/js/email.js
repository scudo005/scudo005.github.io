const link = document.createElement('a');
const node = document.createTextNode('here');
link.appendChild(node);
link.title = 'here';
link.href = 'mailto:scudo005@outlook.com';
document.getElementById('mail').appendChild(link);