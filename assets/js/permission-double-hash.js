var pass = prompt("Please insert the password to access this page.", "")
var goodIdea = 'stocazzo'
var hashpass = digestMessage(goodIdea).then((result1) => digestMessage(pass).then(
    (result) => {
        if (result === result1)
            console.log("access")
            else
                window.location.replace("/unauthorized.html");
        return result
    }
));
async function digestMessage(message) {
    const pass = new TextEncoder().encode(message);
    const hashBuf = await window.crypto.subtle.digest("SHA-256", pass);
    if (Uint8Array.prototype.toHex) {
        return new Uint8Array(hashBuf).toHex();
    }
    else{
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashHex = hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
    }
    console.log(hashHex)
    return hashHex;
}
