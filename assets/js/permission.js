var pass = prompt("Please insert the password to access this page.", "")
var badIdea = "68585251d17afaec3d0dd2f5315ee5a826a708d3c94fb60b534c820c5997aa69"
var test = digestMessage(pass).then(
    (result) => {
	if (result === badIdea)
	    alert("ok");
	else
	    alert("no");
	console.log(result);
	return result
    }
);
console.log("a: "+test);
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
