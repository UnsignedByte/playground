(function() {
    let paths = [];
    let visited = [];
    function propogate(path=[], obj=window){
        let depth = -1;
        if (Object(obj) === obj && !visited.includes(obj)) {
            visited.push(obj)
            for (let x of Object.getOwnPropertyNames(obj)) {
                try {
                    depth = Math.max(depth, propogate([...path, x], obj[x])+1);
                } catch (e){
                }
            }
        }
        if (typeof(obj) === "function") {
            depth = Math.max(depth,0);
            paths.push({value:path, depth:depth});
        }
        return depth;
    }
    propogate();
    let shuffled = paths.map((a) => ({sort: Math.random()+a.depth, value: a.value}))
        .sort((a, b) => a.sort - b.sort)
        .map((a) => `["${a.value.join('"]["')}"]`);
    paths = paths.sort((a, b)=>(a.depth-b.depth) || (b.value.length-a.value.length))
         .map(x=>({depth:x.depth,value:`["${x.value.join('"]["')}"]`}));
    let functions = [];
    let evalstr = "";
    let cdepth = -1;
    let substr = "";
    for(let i = 0; i < paths.length; i++) {
        if (paths[i].depth > cdepth) {
            cdepth = paths[i].depth;
            evalstr+=substr;
            substr = "";
        }
        try {
            evalstr+=`try{functions[${i}] = window${shuffled[i]}}catch(e){}\n`;
            substr+=`try{window${paths[i].value} = functions[${i}]}catch(e){}\n;`
        } catch (e) {
            //console.log(paths[i], e)
        }
    }
    eval(evalstr+substr);
    //console.log(evalstr);
    //eval(evalstr);
})();