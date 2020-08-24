/*
* @Author: UnsignedByte
* @Date:   20:36:23, 23-Aug-2020
* @Last Modified by:   UnsignedByte
* @Last Modified time: 23:42:45, 23-Aug-2020
*/

const fetch = require('node-fetch')
const path = require('path');
const fs = require('fs');

let uuid = 298225;
const delay = ms => new Promise(res => setTimeout(res, ms));
const filter = "!E-Pkenc-_Bu8MBBJVydaOc2zIg**a_WOQbooV-"
function onlyUnique(value, index, self) { 
    return self.indexOf(value) === index;
}

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
	let page = 0
	let data = [];
	do {
		response = await fetch(`https://api.stackexchange.com/2.2/users/${uuid}/comments?page=${++page}&pagesize=100&order=desc&sort=creation&site=stackoverflow&filter=${filter}`).then(x=>x.json())

		if (response.error_id) {
			throw new Error(`Server responded with status ${response.error_id} and message ${response.error_message}.`);
		}
		if (response.backoff) {
			console.log(`Backoff recieved, waiting ${response.backoff} seconds.`);
			await delay(response.backoff*1000);
		}

		let ps = await fetch(`https://api.stackexchange.com/2.2/posts/${response.items.map(x=>x.post_id).filter(onlyUnique).join(';')}?pagesize=100&order=desc&sort=creation&site=stackoverflow&filter=${filter}`)
			.then(v=>v.json()).then(v=>Object.fromEntries(v.items.map(x=>[x.post_id,x.body_markdown])))
		// console.log(ps);

		data = data.concat(response.items.map(
			x=>({body:x.body_markdown, post:ps[x.post_id]}))
		);
		// console.log(data);
		console.log(`${data.length} comments fetched.`);
	} while (response.has_more)
	return data;
}

async function getQs(uuid){
	return await continuousFetch(
		`https://api.stackexchange.com/2.2/users/${uuid}/questions`,
		x=>({body:x.body_markdown})
	)
}

(async () => {
	let data = await fs.promises.readFile(path.resolve(__dirname, `./data.json`)).then(JSON.parse);
	// let data = {};
	// data.comments = await getComments(uuid);
	data.answers = [];
	let page = 0;
	do {
		response = await fetch(`https://api.stackexchange.com/2.2/users/${uuid}/answers?page=${++page}&pagesize=100&order=desc&sort=creation&site=stackoverflow&filter=${filter}`).then(x=>x.json())

		if (response.error_id) {
			throw new Error(`Server responded with status ${response.error_id} and message ${response.error_message}.`);
		}
		if (response.backoff) {
			console.log(`Backoff recieved, waiting ${response.backoff} seconds.`);
			await delay(response.backoff*1000);
		}

		let ps = await fetch(`https://api.stackexchange.com/2.2/questions/${response.items.map(x=>x.question_id).filter(onlyUnique).join(';')}?pagesize=100&order=desc&sort=creation&site=stackoverflow&filter=${filter}`)
			.then(v=>v.json()).then(v=>Object.fromEntries(v.items.map(x=>[x.question_id,x.body_markdown])))
		// console.log(ps);

		data.answers = data.answers.concat(response.items.map(
			x=>({body:x.body_markdown, post:ps[x.question_id]}))
		);
		// console.log(data.answers);
		console.log(`${data.answers.length} answers fetched.`);
	} while (response.has_more)

	// data.questions = await getQs(uuid);



	fs.promises.writeFile(path.resolve(__dirname, `./data.json`), JSON.stringify(data, null, 2))
})();

