#eval 1 + 2
#eval 1 + 2 * 5
#eval String.append "it is " "a string"

def hello := "Hello"

def add1 (n: Nat) : Nat := n + 1
def max (n m : Nat) : Nat := if n > m then n else m

inductive Succ where
  | Zero : Succ
  | S (n : Succ) : Succ

def addSucc (n m : Succ) : Succ := match m with
  | Succ.Zero => n
  | Succ.S m' => Succ.S (addSucc n m')

def succToNat (n: Succ) : Nat := match n with
  | Succ.Zero => Nat.zero
  | Succ.S n' => Nat.succ (succToNat n')

#eval addSucc (Succ.S (Succ.Zero)) (Succ.S (Succ.S Succ.Zero))

def woodlandCritters: List String :=
  ["hedgehog", "deer", "snail"]

def hedgehog := woodlandCritters[0]
def deer := woodlandCritters[1]
def snail := woodlandCritters[2]

def one_plus_one_eq_two : Prop := 1 + 1 = 2
def one_plus_one_eq_three : Prop := 1 + 1 = 3

theorem one_plus_one_eq_two_proof : one_plus_one_eq_two := rfl

theorem two_or_three : one_plus_one_eq_two ∨ one_plus_one_eq_three :=
  @Or.inl one_plus_one_eq_two one_plus_one_eq_three
  rfl

theorem tactic_two_or_three: one_plus_one_eq_two ∨ one_plus_one_eq_three := by
  left
  rfl

-- @[simp] n + 0 = n
theorem add_zero_c (n : Succ) : (addSucc n Succ.Zero) = n := by
  rw [addSucc]

-- @[simp] 1 + (n + m) = (1 + n) + m
theorem add_one_c (n m: Succ) : (Succ.S (addSucc n m)) = addSucc (Succ.S n) m := by
  induction m with
  | Zero =>
    rw [addSucc, addSucc]
  | S m' ih =>
    rw [addSucc, addSucc, ih]

-- @[simp] n + m = m + n
theorem add_com_c (n m: Succ) : (addSucc n m) = (addSucc m n) := by
  induction m with
  | Zero =>
    rw [addSucc]
    induction n with
    | Zero =>
      rw [addSucc]
    | S n' ih =>
      exact congrArg Succ.S ih
  | S m' ih1 =>
    rw [addSucc, ih1]
    exact add_one_c m' n


theorem add_succ_c (n m : Succ): succToNat (addSucc n m) = succToNat n + succToNat m := by
  induction m with
  | Zero =>
    rw [succToNat, addSucc]
    rfl
  | S m' ih1 =>
    cases n with
    | Zero =>
      rw [addSucc, add_com_c, addSucc, succToNat]
      simp
    | S n' =>
      rw [addSucc]
      rw [succToNat]
      conv =>
        rhs
        rhs
        rw [succToNat]
      simp
      simp_arith
      exact ih1


inductive Suit: Prop where
  | Hearts : Suit
  | Diamonds : Suit
  | Clubs : Suit
  | Spades : Suit

inductive Rank where
  | Ace : Rank
  | Num (x: Nat) : Rank
  | Jack : Rank
  | Queen : Rank
  | King : Rank

inductive Card where
  | Basic (s: Suit) (r: Rank) : Card
  | BJoker: Card
  | WJoker: Card

def Wf_card (c: Card): Prop := match c with
  | Card.Basic _ r => match r with
    | Rank.Num x => x <= 10 ∧ x >= 2
    | _ => true
  | _ => true
