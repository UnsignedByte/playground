/*
* @Author: UnsignedByte
* @Date:   2022-03-04 07:41:54
* @Last Modified by:   UnsignedByte
* @Last Modified time: 2022-03-04 08:07:31
*/

let _cookie = `${document.cookie};`.match(/reportsAuthenticatedUser=(.+?);/)[1]

let rooms = await fetch("https://reports.scl.cornell.edu/api/bedavailability/beds", {
  "headers": {
    "authorization": `Bearer ${_cookie}`,
  },
  "referrer": "https://reports.scl.cornell.edu/bedavailability",
  "method": "GET",
  "mode": "cors",
  "credentials": "include"
}).then(x=>x.json()).then(x=>x.data.map(x=>x.Building));

for (let r of rooms) {
	let roomdata = await fetch("https://reports.scl.cornell.edu/api/bedavailability/availableBedsByBuilding", {
	  "headers": {
	    "authorization": `Bearer ${_cookie}`,
    	"content-type": "application/json",
	  },
	  "referrer": "https://reports.scl.cornell.edu/bedavailabilitybyroom",
	  "body": JSON.stringify({building: r}),
	  "method": "POST",
	  "mode": "cors",
	  "credentials": "include"
	}).then(x=>x.json()).then(x=>x.data);

	let suites = {};

	for (let s of roomdata) {
		if (s.IsSuite === "True") {
			suites = Object.assign(Object.fromEntries([[s.SuiteDescription, 0]]), suites);

			suites[s.SuiteDescription] += s.BedCount;
		}
	}

	let counts = {};

	for (let v of Object.values(suites)) {
		counts = Object.assign(Object.fromEntries([[v, 0]]), counts);
		counts[v]++;
	}
	console.log(r);
	console.log(counts);
}