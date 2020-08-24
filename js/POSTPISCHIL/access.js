/*
* @Author: UnsignedByte
* @Date:   18:12:54, 23-Aug-2020
* @Last Modified by:   UnsignedByte
* @Last Modified time: 19:43:41, 23-Aug-2020
*/

const fetch = require('node-fetch')
const path = require('path');
const fs = require('fs');

let uuid = 298225;
const delay = ms => new Promise(res => setTimeout(res, ms));

async function getCommentIDs(uuid){
	let page = 0;
	let comments = [];
	let response;
	do {
		response = await fetch(`https://api.stackexchange.com/2.2/users/${uuid}/comments?order=desc&sort=creation&site=stackoverflow&pagesize=100&page=${++page}&filter=!babFNN1pR4yfqo`).then(x=>x.json())
		if (response.error_id) {
			throw new Error(`Server responded with status ${response.error_id} and message ${response.error_message}.`);
		}

		comments = comments.concat(response.items.map(x=>({body:x.body, date:new Date(x.creation_date*1000), score:x.score, id:x.comment_id})));
		console.log(`${comments.length} comments fetched.`);
	} while (response.has_more)
	
	return comments;
}

getCommentIDs(uuid)
	.then(x=>fs.promises.writeFile(path.resolve(__dirname, `./data.json`), JSON.stringify(x)))