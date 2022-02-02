(*
* @Author: UnsignedByte
* @Date:   2022-02-02 08:14:01
* @Last Modified by:   UnsignedByte
* @Last Modified time: 2022-02-02 09:15:26
*)

let tri h m = 
	let rec rtri r h m = 
		let rec grow r = 
			match r with
			| [] -> []
			| e :: rx -> (
				match rx with
				| [] -> e
				| e2 :: rx2 -> (e + e2) mod m
			) :: grow rx
		in match h with
		| 0 -> r
		| _ -> rtri ((1 :: grow (match r with | [] -> [] | rl :: rex -> rl)) :: r) (h - 1) m
	in rtri [] h m

let rec rep_str s n =
	match n with
	| _ when n < 0 -> ""
	| _ -> s ^ (rep_str s (n-1))

let triangle_str h m =
	let rec pllr l i =
		match l with
		| [] -> ""
		| e :: lx ->
			let rec plr l =
				match l with
				| [] -> rep_str " " (h - i)
				| e :: lx -> ((plr lx) ^ " " ^ (string_of_int e))
			in ((pllr lx (i-1)) ^ "\n" ^ (plr e))
	in pllr (tri h m) h

let () = print_endline (triangle_str 32 2)