const CACHE_NAME = "catalogue-assets-v1"; 
const assets = [
    "/",
    "/static/css/style.css",
    "/static/js/app.js",
    "/static/images/logo.png",
    "/static/images/favicon.png",
    "/static/icons/icon-128x128.png",
    "/static/icons/icon-192x192.png",
    "/static/icons/icon-384x384.png",
    "/static/icons/icon-512x512.png",
    "/static/icons/desktop_screenshot.png",
    "/static/icons/mobile_screenshot.png",
];

self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return Promise.all(
                assets.map(url => {
                    return cache.add(url).catch(err => console.error("Failed to cache:", url, err));
                })
            );
        }).then(() => self.skipWaiting())
    );
});

self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys().then((keyList) => {
            return Promise.all(
                keyList.map((key) => {
                    if (key !== CACHE_NAME) {
                        return caches.delete(key);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

self.addEventListener("fetch", (event) => {
    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            return cachedResponse || fetch(event.request);
        })
    );
});