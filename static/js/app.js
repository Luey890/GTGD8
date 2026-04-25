window.addEventListener('unload', function (event) {
        if (document.visibilityState === 'hidden') {

    navigator.sendBeacon('/logout');
        }});

if ("serviceWorker" in navigator) { 
    window.addEventListener("load", function () {
        navigator.serviceWorker
        .register("/serviceworker.js") 
        .then((res) => console.log("Service worker registered"))
        .catch((err) => console.log("Service worker not registered", err));
    });
}

