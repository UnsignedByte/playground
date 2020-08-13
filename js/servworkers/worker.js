/*
* @Author: UnsignedByte
* @Date:   21:06:16, 16-Jul-2020
* @Last Modified by:   UnsignedByte
* @Last Modified time: 15:40:23, 26-Jul-2020
*/

const CACHENAME = 'js13kPWA-v1';

const cachedFiles = [
  '/test.js',
  '/test.css',
  '/index.html'
  'https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@100&display=swap'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(cacheName).then((cache) => cache.addAll(contentToCache)));
});

self.addEventListener('fetch', e => {
  e.respondWith(caches.match(e.request).then(response => response || fetch(e.request)));
});

