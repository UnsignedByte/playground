/*
* @Author: UnsignedByte
* @Date:   23:02:47, 14-Aug-2020
* @Last Modified by:   UnsignedByte
* @Last Modified time: 10:41:35, 15-Aug-2020
*/
const a = 19; // "I don't understand "
const maxlen = 10000000;
function getst(tosend, pref){
	let wantedL = maxlen-tosend.length;
	return '0'.repeat(wantedL%a+18)+' '+'wtf '.repeat(Math.floor(wantedL/a)-1)+tosend+pref;
}

const body = getst('<div class="</div><script>console.log(\'runnnnnnn\')</script>', '"/>');