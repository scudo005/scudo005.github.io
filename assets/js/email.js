const link = document.createElement('a');
const node = document.createTextNode('here');
const parent = document.getElementById('mail');
link.appendChild(node);
link.title = 'here';
link.href = 'mailto:scudo005@outlook.com';
parent.appendChild(link);