/*
* @Author: UnsignedByte
* @Date:   18:12:54, 23-Aug-2020
* @Last Modified by:   UnsignedByte
* @Last Modified time: 20:21:18, 23-Aug-2020
*/

const fetch = require('node-fetch')
const path = require('path');
const fs = require('fs');

let uuid = 298225;
const delay = ms => new Promise(res => setTimeout(res, ms));
const filter = "!.K6KdqgnytCtwZ1xc1FjWPlJ4oXc("

async function continuousFetch(link, parseF){
	let page = 0;
	let data = [];
	let response;
	do {
		response = await fetch(`${link}?order=desc&sort=creation&site=stackoverflow&pagesize=100&page=${++page}&filter=${filter}`).then(x=>x.json())
		if (response.error_id) {
			throw new Error(`Server responded with status ${response.error_id} and message ${response.error_message}.`);
		}
		if (response.backoff) {
			console.log(`Backoff recieved, waiting ${response.backoff} seconds.`);
			await delay(response.backoff*1000);
		}

		data = data.concat(response.items.map(parseF));
		console.log(`${data.length} fetched.`);
	} while (response.has_more)
	
	return data;
}

async function getComments(uuid){
	return await continuousFetch(
		`https://api.stackexchange.com/2.2/users/${uuid}/comments`,
		x=>({body:x.body, markdown:x.body_markdown, link:x.link, date:new Date(x.creation_date*1000), score:x.score, id:x.comment_id})
	)
}

async function getPosts(uuid){
	return await continuousFetch(
		`https://api.stackexchange.com/2.2/users/${uuid}/posts`,
		x=>({body:x.body, markdown:x.body_markdown, type:x.post_type, link:x.link, date:new Date(x.creation_date*1000), score:x.score, id:x.post_id})
	)
}

(async () => {
	let data = {};
	data.posts = await getPosts(uuid, "post");
	data.comments = await getComments(uuid, "comment");

	fs.promises.writeFile(path.resolve(__dirname, `./data.json`), JSON.stringify(data, null, 2))
})();

