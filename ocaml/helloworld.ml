(*
* @Author: UnsignedByte
* @Date:   2022-01-26 18:34:14
* @Last Modified by:   UnsignedByte
* @Last Modified time: 2022-01-28 11:47:49
*)

let () = print_endline "Hello World!"

let sus v = v ^ " among us"

let () = print_endline (sus "mmm")

(* open String *)
let () = print_endline (let y, x = "\" in x ^ (String.escaped y) ^ \"\\\", \\\"\" ^ String.escaped x ^ y)", "let () = print_endline (let y, x = \"" in x ^ (String.escaped y) ^ "\", \"" ^ String.escaped x ^ y)

let () = Printf.printf "%S" "let () = print_endline \"Hello World!\""

let () = (fun s -> Printf.printf "%s %S" s s) "let () = (fun s -> Printf.printf \"%s %S\" s s)"