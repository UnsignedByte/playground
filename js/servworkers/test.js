/*
* @Author: UnsignedByte
* @Date:   18:12:52, 16-Jul-2020
* @Last Modified by:   UnsignedByte
* @Last Modified time: 13:18:57, 17-Jul-2020
*/

document.getElementById('test').innerHTML = 'haha'

// register the sevice worker
if('serviceWorker' in navigator) {
    navigator.serviceWorker.register('./worker.js');
};