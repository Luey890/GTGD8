let timer

function resetTimer() {
    clearTimeout(timer);
    timer = setTimeout(() => {
        alert("You have been logged out due to inactivity.");
        window.location.href = "/logout";
    }, 300000); 
}


window.onload = resetTimer;
window.onmousemove = resetTimer;
window.onmousedown = resetTimer; 
window.ontouchstart = resetTimer; 
window.onclick = resetTimer;     
window.onkeydown = resetTimer;
if ("serviceWorker" in navigator) { 
    window.addEventListener("load", function () {
        navigator.serviceWorker
        .register("/serviceworker.js") 
        .then((res) => console.log("Service worker registered"))
        .catch((err) => console.log("Service worker not registered", err));
    });
}

