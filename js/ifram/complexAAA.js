/*
* @Author: UnsignedByte
* @Date:   23:41:04, 12-Aug-2020
* @Last Modified by:   UnsignedByte
* @Last Modified time: 02:21:27, 13-Aug-2020
*/

// document.head.appendChild(document.createElement('script')).src = 'https://unsignedbyte.github.io/playground/js/ifram/complexAAA.js'

let posts;
const delay = ms => new Promise(res => setTimeout(res, ms));

function htmlToElement(html) {
    var template = document.createElement('template');
    html = html.trim(); // Never return a text node of whitespace as the result
    template.innerHTML = html;
    return template.content.firstChild;
}

function load(){
	console.log("loading new posts...");
	posts = Array.prototype.slice.call(document.querySelectorAll("#main-inner ul.s-edge-feed > li"));
	if (posts.length === 0) return;
	// rerun load when new posts loaded
	posts[posts.length-1].children[0].addEventListener('click', async ()=>{
		for(let i = 0; i < 10; i++){
			await delay(1000);
			load();
		}
	});
	posts = posts.slice(0, posts.length-1);
	for (x of posts){
		let c1 = x.querySelector(`.feed-comments .s-comments-post-form > form > div > span.submit-span-wrapper`);
		if (c1 === null || x.querySelector('span[name="spamComment"]') !== null) continue;
		let c = htmlToElement(`<span name="spamComment" style="display: none; border: 1px solid rgb(2, 61, 90);background: url(&quot;/sites/all/themes/schoology_theme/images/btn-bg-dark.gif?5f3434ac7da37785&quot;) repeat-x rgb(51, 125, 188);float: none !important;vertical-align: top;white-space: nowrap;margin-top: 5px;margin-left: 10px;padding: 0;outline: none;"><input type="button" value="Spam Comment" class="" onclick="spam(&quot;${x.id}&quot;)" style="padding: 4px 8px;font-size: 13px;height: 24px;"></span>`);
		c = c1.parentNode.insertBefore(c, c1.nextSibling);
		let f = (event) => {
			const targetElement = event.target || event.srcElement;
			c.style.display = "inline-block";
			if (targetElement.value.length === 0) {
				c.style.opacity= .5;
				c.style.zoom= 1;
				c.style.cursor= "default";
			}else {
				c.style.opacity= null;
				c.style.zoom= null;
				c.style.cursor= null;
			}
		}
		x.querySelector('textarea[name="comment"]').addEventListener('click', f)
		x.querySelector('textarea[name="comment"]').addEventListener('input', f)
		x.querySelector('textarea[name="comment"]').addEventListener('blur', (event)=>{
			const targetElement = event.target || event.srcElement;
			if (targetElement.value === "Write a comment"){
				c.style.display = "none";
			}
		})
	}
}

spamming = {};
// add-comment-resize
async function spam(id){
	if (spamming[id]){
		spamming[id] = false;
		document.querySelector(`#${id} span[name="spamComment"] > input`).value = "Spam Post";
		return;
	}
	const content = document.querySelector(`#${id} textarea[name="comment"]`).value;
	const dat = Object.assign(...Array.prototype.slice.call(document.querySelectorAll(`#${id} .feed-comments .s-comments-post-form > form > div > input`)).map(x=>({[x.name]: x.value})));
	spamming[id] = true;

	document.querySelector(`#${id} span[name="spamComment"] > input`).value = "Stop Spamming";

	while(spamming[id]){
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
		}).then(resp=>{
			if (resp.status === 200){
				console.log(`Message sent successfully to ${dat.nid}.`);
			}
		});
		await delay(3000);
	}
}

async function continuousload(){
	for(;;){
		load();
		await delay(5000);
	}
}
continuousload();