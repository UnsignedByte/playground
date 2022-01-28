(*
* @Author: UnsignedByte
* @Date:   2022-01-26 18:34:14
* @Last Modified by:   UnsignedByte
* @Last Modified time: 2022-01-28 11:31:58
*)

let () = print_endline "Hello World!"

let sus v = v ^ " among us"

let () = print_endline (sus "mmm")

open String
let () = print_endline (let y, x = "\" in x ^ (String.escaped y) ^ \"\\\", \\\"\" ^ String.escaped x ^ y)", "open String\nlet () = print_endline (let y, x = \"" in x ^ (String.escaped y) ^ "\", \"" ^ String.escaped x ^ y)