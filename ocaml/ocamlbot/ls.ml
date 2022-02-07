(*
* @Author: UnsignedByte
* @Date:   2022-02-07 11:12:01
* @Last Modified by:   UnsignedByte
* @Last Modified time: 2022-02-07 13:46:57
*)

(** List all files in the directory
		recursively. *)
let _ =
(let rec ls p i bl = 
 	let lsnr v = List.map (fun x -> 
 		try Sys.readdir x |> Array.to_list |> List.filter_map (fun s -> if List.exists ((=) s) bl then None else Some (x ^ "/" ^ s))
 		with _ -> [x]) v |> List.flatten
 	in match i with
 	| 0 -> p
 	| _ -> (i-1 |> ls @@ lsnr p) bl in (let rec ts l = match l with
 			| [] -> ()
 			| a :: b -> print_endline a;(ts b) in ts) @@ ls ["/"] 10 ["opam-repository"; ".git"])

let () = 
let rf fn =
	Printf.sprintf "===FILE: %s===\n\n%s" fn (let ic = open_in fn in let icl = in_channel_length ic in
	 	let buf = Bytes.create icl in
	 	input ic buf 0 icl |> Bytes.sub_string buf 0) in
let rec prf l = match l with
	| [] -> ""
	| a :: b -> Printf.sprintf "%s\n\n===EOF===\n\n%s" (rf a) (prf b)
in print_endline @@ prf ["/home/opam/.gitconfig"; "/home/opam/.opamrc-sandbox"; "/home/opam/.bashrc"]