/*
* @Author: UnsignedByte
* @Date:   16:10:21, 24-May-2020
* @Last Modified by:   UnsignedByte
* @Last Modified time: 12:18:48, 06-Sep-2020
*/

// import resolve from '@rollup/plugin-node-resolve';
// import ignore from 'rollup-plugin-ignore';
// import commonjs from '@rollup/plugin-commonjs';

export default {
  input: 'bot.js',
  inlineDynamicImports: true,
  output: {
    file: 'main.js',
    format: 'iife',
    name: 'Bot',
		sourcemap: true
  },
	// plugins: [
	// 	resolve({
	// 		browser: true
	// 	}),
 //    commonjs(),
	// 	ignore([
	// 		'fs',
	// 		'buffer',
	// 		'mcproto'
	// 	])
	// ]
};
