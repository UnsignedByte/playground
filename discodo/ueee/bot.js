/*
* @Author: UnsignedByte
* @Date:   11:57:15, 06-Sep-2020
* @Last Modified by:   UnsignedByte
* @Last Modified time: 13:18:00, 06-Sep-2020
*/


// https://en.wikipedia.org/w/api.php?format=json&action=query&generator=random

import '../../js/utils/_dom2.js'
import Discord from "../discord/discord.js"
// import * as storage from './utils/storage.js'

const TOKEN_KEY = '[playground/discodo/ueee] token'
const NO_STORE = 'please do not store token in localStorage thank'

let token = localStorage.getItem(TOKEN_KEY)
const tokenInput = Elem('input', {
	type: 'text',
	value: token === NO_STORE ? '' : token,
	onchange: () => {
    	if (!storeInput.checked) {
    		localStorage.setItem(TOKEN_KEY, tokenInput.value)
    	}
    }
})
const storeInput = Elem('input', {
	type: 'checkbox',
	checked: token === NO_STORE,
	onchange: () => {
			if (storeInput.checked) {
				localStorage.setItem(TOKEN_KEY, NO_STORE)
			} else {
				localStorage.setItem(TOKEN_KEY, tokenInput.value)
			}
		}
	})
	document.body.appendChild(Fragment([
	Elem('p', {}, [
		Elem('label', {}, [
			'Token: ',
			tokenInput
		])
	]),
	Elem('p', {}, [
		Elem('label', {}, [
			storeInput,
			'Do not store token in localStorage',
		])
	]),
	Elem('button', {
		autofocus: true,
		onclick: () => {
			empty(document.body)
			main(tokenInput.value, Discord).catch(err => {
				console.error(err)
				document.body.appendChild(Elem('p', {}, ['There was a problem. Check the console?']))
			})
		}
	}, ['Start'])
]))

async function main (token, Discord) {
	const { Client } = Discord

	// Create an instance of a Discord client
	const client = new Client()

	const commands = [
		[/^echo (.+?)( \d+)?$/s, async (x, msg)=>{
			console.log("run");
			for (let i = 0; i < (x[2] || 1); i++){
				await msg.channel.send(x[1])
			}
		}],
		[/^wiki$/, async (x, msg)=>{
			let title = await fetch('https://en.wikipedia.org/w/api.php?format=json&action=query&generator=random&origin=*').then(x=>x.json()).then(x=>Object.values(x.query.pages)[0].title);
			await msg.channel.send(`lwiki ${title}`);
		}]
	];

	client.on('ready', () => {
		console.log('ready');
	})

	client.on('message', async msg => {
		if (msg.content.startsWith('u')) {
			msg.content = msg.content.substring(1);
			for(let r of commands){
				let v = msg.content.match(r[0]);
				console.log(msg.content);
				console.log(r);
				console.log(v);
				if (v !== null){
					await r[1](v, msg)
				}
			}
		}
	})

	await client.login(token)
}