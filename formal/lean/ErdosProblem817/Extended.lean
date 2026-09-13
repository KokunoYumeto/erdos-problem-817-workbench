import ErdosProblem817.Core
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Fintype.Pi
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.BigOperators.Group.Finset.Sigma
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Data.Finset.Card
import Mathlib.Data.List.OfFn
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-!
# Extended Foundation and Ergonomic Lemmas for Erdős Problem 817

This module extends `ErdosProblem817.Core` with ergonomic helpers and golfed formulations:

1. **Relation Splitting Golfing**:
   - `relation_splitting_golfed`: compressed formulation of `relation_splitting` with implicit binders
     `{S : Set ℤ}` and `{P₁ P₂ N₁ N₂ : ℤ}`.
   - Component projections `relation_splitting_eq₁` and `relation_splitting_eq₂`.

2. **`FourAPFree` Theory**:
   - Subset monotonicity (`FourAPFree.subset`, `fourAPFree_mono`).
   - Boundary cases (`fourAPFree_empty`, `fourAPFree_singleton`).
   - Translation invariance under addition, left-addition, and preimage
     (`fourAPFree_image_add_const`, `fourAPFree_image_const_add`, `fourAPFree_preimage_add_const`).
   - Characterizations (`fourAPFree_iff_fourTermProgression`, `fourAPFree_iff_not_exists`).
   - Bridges to core results: `language_fourAPFree`, `evaluatedBlocksSet_fourAPFree`, and
     `evaluatedBlocks_subset_fourAPFree`.

3. **`BlockChoice` and `Finset (Fin 3)` Choices**:
   - Generator weights `blockWeights : Fin 3 → ℤ` for `(1, 7, 8)`.
   - Canonical equivalence `blockChoiceEquivFinset : BlockChoice ≃ Finset (Fin 3)`.
   - Explicit subset sum identities: `blockValue_eq_sum` and `blockValue_finsetToBlock`.
   - Finite combinatorics: `card_blockChoice`, digit surjectivity `blockValue_surjective_digits`,
     and the exact collision `blockValue_collision` on digit 8.

4. **Subset-sums Operator**:
   - Operator `subsetSums (S : Finset ℤ) : Set ℤ`.
   - Inclusion monotonicity `subsetSums_mono` and heredity `fourAPFree_subsetSums_of_subset`.

5. **The Base-19 Generator Construction**:
   - Multi-scale generators `blockGenerator (j : ℕ) (k : Fin 3) := 19^j * blockWeights k`.
   - Generator block set `generators (m : ℕ) : Finset ℤ`.
   - Strict positivity `generators_pos` and upper bound `generators_le`.
   - Exact injectivity `blockGenerator_injective`, `generators_injective`, and cardinality `card_generators : (generators m).card = 3 * m`.

6. **Bridge to Evaluated Blocks**:
   - Evaluation theorem `evaluateBlocks_ofFn` relating `evaluateBlocks` to base-19 expansions.
   - Exact subset sum containment `subsetSums_generators_subset_evaluatedBlocksSet`.
   - Freeness of generator subset sums: `generators_fourAPFree`.

7. **The Main Finite Upper Bound Theorem**:
   - `erdos_problem_817_upper_bound`: For every positive integer `n`, existence of an `n`-element set
     `B` of integers bounded by `8 * 19 ^ ((n + 2) / 3 - 1)` whose subset sums are 4-AP-free.
-/

namespace ErdosProblem817

/-- Golfed version of `relation_splitting` using implicit binders `{S : Set ℤ}` and `{P₁ P₂ N₁ N₂ : ℤ}`
and compressed `convert ... using 1` with `<;> linarith`. -/
theorem relation_splitting_golfed {S : Set ℤ} (hfree : FourAPFree S)
    {P₁ P₂ N₁ N₂ : ℤ} (hrel : P₁ + 2 * P₂ = N₁ + 2 * N₂)
    (h₀ : P₁ + N₂ ∈ S) (h₁ : P₁ + P₂ ∈ S)
    (h₂ : N₁ + N₂ ∈ S) (h₃ : N₁ + P₂ ∈ S) :
    P₂ = N₂ ∧ P₁ = N₁ := by
  have hd : P₂ - N₂ = 0 := hfree (P₁ + N₂) (P₂ - N₂) h₀
    (by convert h₁ using 1; ring)
    (by convert h₂ using 1; linarith)
    (by convert h₃ using 1; linarith)
  constructor <;> linarith

/-- Component projection of `relation_splitting_golfed`: the magnitude-two layers match. -/
theorem relation_splitting_eq₂ {S : Set ℤ} (hfree : FourAPFree S)
    {P₁ P₂ N₁ N₂ : ℤ} (hrel : P₁ + 2 * P₂ = N₁ + 2 * N₂)
    (h₀ : P₁ + N₂ ∈ S) (h₁ : P₁ + P₂ ∈ S)
    (h₂ : N₁ + N₂ ∈ S) (h₃ : N₁ + P₂ ∈ S) :
    P₂ = N₂ :=
  (relation_splitting_golfed hfree hrel h₀ h₁ h₂ h₃).1

/-- Component projection of `relation_splitting_golfed`: the magnitude-one layers match. -/
theorem relation_splitting_eq₁ {S : Set ℤ} (hfree : FourAPFree S)
    {P₁ P₂ N₁ N₂ : ℤ} (hrel : P₁ + 2 * P₂ = N₁ + 2 * N₂)
    (h₀ : P₁ + N₂ ∈ S) (h₁ : P₁ + P₂ ∈ S)
    (h₂ : N₁ + N₂ ∈ S) (h₃ : N₁ + P₂ ∈ S) :
    P₁ = N₁ :=
  (relation_splitting_golfed hfree hrel h₀ h₁ h₂ h₃).2

/-!
### `FourAPFree` Monotonicity and Translation Invariance
-/

/-- Subset monotonicity of `FourAPFree`: any subset of a 4-AP-free set is 4-AP-free. -/
theorem FourAPFree.subset {S T : Set ℤ} (hST : S ⊆ T) (hT : FourAPFree T) : FourAPFree S :=
  fun x d hx hd₁ hd₂ hd₃ => hT x d (hST hx) (hST hd₁) (hST hd₂) (hST hd₃)

/-- Alias for `FourAPFree.subset`. -/
theorem fourAPFree_mono {S T : Set ℤ} (hST : S ⊆ T) (hT : FourAPFree T) : FourAPFree S :=
  hT.subset hST

/-- The empty set is 4-AP-free. -/
theorem fourAPFree_empty : FourAPFree (∅ : Set ℤ) :=
  fun _ _ hx => hx.elim

/-- Any singleton set is 4-AP-free. -/
theorem fourAPFree_singleton (a : ℤ) : FourAPFree ({a} : Set ℤ) := by
  intro x d hx hd₁ _ _
  rw [Set.mem_singleton_iff] at hx hd₁
  subst hx
  linarith

/-- Translation invariance of `FourAPFree`: shifting a set by adding `c` preserves 4-AP-freeness. -/
theorem fourAPFree_image_add_const (S : Set ℤ) (c : ℤ) :
    FourAPFree ((· + c) '' S) ↔ FourAPFree S := by
  constructor
  · intro hT x d hx hd₁ hd₂ hd₃
    have h₀ : x + c ∈ (· + c) '' S := ⟨x, hx, rfl⟩
    have h₁ : (x + c) + d ∈ (· + c) '' S := ⟨x + d, hd₁, by ring⟩
    have h₂ : (x + c) + 2 * d ∈ (· + c) '' S := ⟨x + 2 * d, hd₂, by ring⟩
    have h₃ : (x + c) + 3 * d ∈ (· + c) '' S := ⟨x + 3 * d, hd₃, by ring⟩
    exact hT (x + c) d h₀ h₁ h₂ h₃
  · intro hS y d ⟨x, hx, hxy⟩ hd₁ hd₂ hd₃
    subst hxy
    obtain ⟨x₁, hx₁, hx₁y⟩ := hd₁
    obtain ⟨x₂, hx₂, hx₂y⟩ := hd₂
    obtain ⟨x₃, hx₃, hx₃y⟩ := hd₃
    have hd₁' : x + d ∈ S := by
      have : x₁ = x + d := by linarith
      rwa [← this]
    have hd₂' : x + 2 * d ∈ S := by
      have : x₂ = x + 2 * d := by linarith
      rwa [← this]
    have hd₃' : x + 3 * d ∈ S := by
      have : x₃ = x + 3 * d := by linarith
      rwa [← this]
    exact hS x d hx hd₁' hd₂' hd₃'

/-- Translation invariance of `FourAPFree`: left-addition `(c + ·) '' S`. -/
theorem fourAPFree_image_const_add (S : Set ℤ) (c : ℤ) :
    FourAPFree ((c + ·) '' S) ↔ FourAPFree S := by
  have heq : (c + ·) = (fun x : ℤ => x + c) := funext (fun _ => add_comm _ _)
  rw [heq]
  exact fourAPFree_image_add_const S c

/-- Translation invariance of `FourAPFree` under preimage `(· + c) ⁻¹' S`. -/
theorem fourAPFree_preimage_add_const (S : Set ℤ) (c : ℤ) :
    FourAPFree ((· + c) ⁻¹' S) ↔ FourAPFree S := by
  have heq : ((· + c) ⁻¹' S) = (· + (-c)) '' S := by
    ext x
    simp only [Set.mem_preimage, Set.mem_image]
    constructor
    · intro hx
      exact ⟨x + c, hx, by ring⟩
    · rintro ⟨y, hy, rfl⟩
      simpa using hy
  rw [heq]
  exact fourAPFree_image_add_const S (-c)

/-!
### `FourAPFree` Characterizations and Language Bridges
-/

/-- Characterization of `FourAPFree`: a set is 4-AP-free if and only if all four-term progressions
in `S` (as defined in `FourTermProgression`) are constant. -/
theorem fourAPFree_iff_fourTermProgression (S : Set ℤ) :
    FourAPFree S ↔
      ∀ x₀ x₁ x₂ x₃ : ℤ,
        x₀ ∈ S → x₁ ∈ S → x₂ ∈ S → x₃ ∈ S →
        FourTermProgression x₀ x₁ x₂ x₃ →
        x₀ = x₁ ∧ x₁ = x₂ ∧ x₂ = x₃ := by
  constructor
  · intro hfree x₀ x₁ x₂ x₃ h₀ h₁ h₂ h₃ ⟨hap₀, hap₁⟩
    let d := x₁ - x₀
    have hx₁ : x₁ = x₀ + d := by linarith
    have hx₂ : x₂ = x₀ + 2 * d := by linarith
    have hx₃ : x₃ = x₀ + 3 * d := by linarith
    have hd : d = 0 := by
      apply hfree x₀ d h₀
      · rwa [← hx₁]
      · rwa [← hx₂]
      · rwa [← hx₃]
    constructor
    · linarith
    constructor
    · linarith
    · linarith
  · intro hprog x d h₀ h₁ h₂ h₃
    have hap : FourTermProgression x (x + d) (x + 2 * d) (x + 3 * d) := by
      constructor <;> ring
    obtain ⟨heq, _, _⟩ := hprog x (x + d) (x + 2 * d) (x + 3 * d) h₀ h₁ h₂ h₃ hap
    linarith

/-- Characterization of `FourAPFree` as the absence of any non-trivial 4-term progression. -/
theorem fourAPFree_iff_not_exists (S : Set ℤ) :
    FourAPFree S ↔ ¬ ∃ (x d : ℤ), d ≠ 0 ∧ x ∈ S ∧ x + d ∈ S ∧ x + 2 * d ∈ S ∧ x + 3 * d ∈ S := by
  constructor
  · rintro hfree ⟨x, d, hd, h₀, h₁, h₂, h₃⟩
    exact hd (hfree x d h₀ h₁ h₂ h₃)
  · intro hnot x d h₀ h₁ h₂ h₃
    by_contra hd
    exact hnot ⟨x, d, hd, h₀, h₁, h₂, h₃⟩

/-- The length-`m` base-19 digit language is `FourAPFree`. -/
theorem language_fourAPFree (m : Nat) : FourAPFree {x : ℤ | Language m x} := by
  rw [fourAPFree_iff_fourTermProgression]
  intro x₀ x₁ x₂ x₃ h₀ h₁ h₂ h₃ hap
  exact language_four_ap_constant m x₀ x₁ x₂ x₃ h₀ h₁ h₂ h₃ hap

/-- The set of integers generated by evaluating length-`n` block choices. -/
def evaluatedBlocksSet (n : Nat) : Set ℤ :=
  {x : ℤ | ∃ es : List BlockChoice, es.length = n ∧ evaluateBlocks es = x}

/-- The evaluation set of length-`n` block choices is `FourAPFree`. -/
theorem evaluatedBlocksSet_fourAPFree (n : Nat) : FourAPFree (evaluatedBlocksSet n) := by
  rw [fourAPFree_iff_fourTermProgression]
  rintro _ _ _ _ ⟨e₀, rfl, rfl⟩ ⟨e₁, hlen₁, rfl⟩ ⟨e₂, hlen₂, rfl⟩ ⟨e₃, hlen₃, rfl⟩ hap
  exact evaluated_blocks_four_ap_constant e₀ e₁ e₂ e₃ hlen₁ hlen₂ hlen₃ hap

/-- Any subset of evaluated length-`n` blocks is `FourAPFree`. -/
theorem evaluatedBlocks_subset_fourAPFree {S : Set ℤ} {n : Nat}
    (hS : S ⊆ evaluatedBlocksSet n) : FourAPFree S :=
  (evaluatedBlocksSet_fourAPFree n).subset hS

/-!
### Connecting `BlockChoice` to `Finset (Fin 3)` Choices
-/

/-- The three generator weights `(1, 7, 8)` associated with a base-19 block. -/
def blockWeights : Fin 3 → ℤ
  | 0 => 1
  | 1 => 7
  | 2 => 8

/-- Convert a `BlockChoice` indicator function to the `Finset (Fin 3)` of chosen generator indices. -/
def blockToFinset (e : BlockChoice) : Finset (Fin 3) :=
  Finset.univ.filter (fun i => e i)

/-- Convert a subset of generator indices to its `BlockChoice` indicator function. -/
def finsetToBlock (s : Finset (Fin 3)) : BlockChoice :=
  fun i => decide (i ∈ s)

@[simp]
theorem finsetToBlock_blockToFinset (e : BlockChoice) :
    finsetToBlock (blockToFinset e) = e := by
  ext i
  simp [finsetToBlock, blockToFinset]

@[simp]
theorem blockToFinset_finsetToBlock (s : Finset (Fin 3)) :
    blockToFinset (finsetToBlock s) = s := by
  ext i
  simp [finsetToBlock, blockToFinset]

/-- Canonical bijection between `BlockChoice` and subsets of generator indices `Finset (Fin 3)`. -/
def blockChoiceEquivFinset : BlockChoice ≃ Finset (Fin 3) where
  toFun := blockToFinset
  invFun := finsetToBlock
  left_inv := finsetToBlock_blockToFinset
  right_inv := blockToFinset_finsetToBlock

/-- The cardinality of `BlockChoice` is exactly 8 (corresponding to the $2^3$ subsets of `{1, 7, 8}`). -/
theorem card_blockChoice : Fintype.card BlockChoice = 8 := by
  decide

/-- Every `Fin 7` digit is achieved as the `blockValue` of some `BlockChoice`. -/
theorem blockValue_surjective_digits :
    ∀ d : Fin 7, ∃ e : BlockChoice, blockValue e = digitValue d := by
  decide

/-- The collision on digit 8: both `![false, false, true]` (generator 8) and
`![true, true, false]` (generators 1 + 7) yield `blockValue = 8`. -/
theorem blockValue_collision :
    ∃ e₁ e₂ : BlockChoice, e₁ ≠ e₂ ∧ blockValue e₁ = blockValue e₂ := by
  decide

open scoped BigOperators

/-- The evaluation `blockValue e` coincides exactly with the subset sum over active generator indices. -/
theorem blockValue_eq_sum :
    ∀ e : BlockChoice, blockValue e = ∑ i ∈ blockToFinset e, blockWeights i := by
  decide

/-- The evaluation of a subset of generator indices coincides with its subset sum. -/
theorem blockValue_finsetToBlock (s : Finset (Fin 3)) :
    blockValue (finsetToBlock s) = ∑ i ∈ s, blockWeights i := by
  have := blockValue_eq_sum (finsetToBlock s)
  rwa [blockToFinset_finsetToBlock] at this

#print axioms relation_splitting_golfed
#print axioms fourAPFree_image_add_const
#print axioms fourAPFree_iff_fourTermProgression
#print axioms language_fourAPFree
#print axioms evaluatedBlocksSet_fourAPFree
#print axioms blockValue_eq_sum

/-!
### Subset-sums Operator and Heredity
-/

/-- The subset-sums of a finite set `S` of integers. -/
def subsetSums (S : Finset ℤ) : Set ℤ :=
  { y | ∃ s ⊆ S, ∑ x ∈ s, x = y }

/-- Monotonicity of the subset-sums operator under inclusion. -/
theorem subsetSums_mono {S T : Finset ℤ} (h : S ⊆ T) : subsetSums S ⊆ subsetSums T := by
  rintro y ⟨s, hs, rfl⟩
  exact ⟨s, hs.trans h, rfl⟩

/-- Heredity: any subset of a set with 4-AP-free subset sums also has 4-AP-free subset sums. -/
theorem fourAPFree_subsetSums_of_subset {S T : Finset ℤ} (h : S ⊆ T)
    (hT : FourAPFree (subsetSums T)) : FourAPFree (subsetSums S) :=
  hT.subset (subsetSums_mono h)

/-!
### The Base-19 Generator Construction
-/

/-- The individual generator at block level `j` with digit weight choice `k`. -/
def blockGenerator (j : ℕ) (k : Fin 3) : ℤ :=
  (19 : ℤ) ^ j * blockWeights k

/-- The finite set of $3m$ base-19 generators of the block construction. -/
def generators (m : ℕ) : Finset ℤ :=
  (Finset.univ : Finset (Fin m × Fin 3)).image (fun jk => blockGenerator jk.1.1 jk.2)

theorem blockWeights_pos : ∀ k : Fin 3, 1 ≤ blockWeights k := by
  decide

theorem blockWeights_le_eight : ∀ k : Fin 3, blockWeights k ≤ 8 := by
  decide

theorem blockWeights_injective : ∀ {k₁ k₂ : Fin 3}, blockWeights k₁ = blockWeights k₂ → k₁ = k₂ := by
  decide

theorem one_le_pow_nineteen (j : ℕ) : (1 : ℤ) ≤ 19 ^ j := by
  induction j with
  | zero => decide
  | succ j ih =>
      have : (19 : ℤ) ^ (j + 1) = 19 ^ j * 19 := rfl
      rw [this]
      nlinarith

lemma pow_nineteen_mono {a b : ℕ} (h : a ≤ b) : (19 : ℤ) ^ a ≤ (19 : ℤ) ^ b := by
  obtain ⟨c, rfl⟩ := Nat.le.dest h
  have : (19 : ℤ) ^ (a + c) = (19 : ℤ) ^ a * (19 : ℤ) ^ c := pow_add _ _ _
  rw [this]
  have hc := one_le_pow_nineteen c
  have ha := one_le_pow_nineteen a
  nlinarith

theorem blockGenerator_pos (j : ℕ) (k : Fin 3) : 1 ≤ blockGenerator j k := by
  dsimp [blockGenerator]
  have h₁ := one_le_pow_nineteen j
  have h₂ := blockWeights_pos k
  nlinarith

theorem generators_pos (m : ℕ) : ∀ x ∈ generators m, 1 ≤ x := by
  intro x hx
  simp only [generators, Finset.mem_image, Finset.mem_univ, true_and] at hx
  obtain ⟨⟨j, k⟩, rfl⟩ := hx
  exact blockGenerator_pos j.1 k

theorem generators_le (m : ℕ) (hm : 1 ≤ m) :
    ∀ x ∈ generators m, x ≤ 8 * (19 : ℤ) ^ (m - 1) := by
  intro x hx
  simp only [generators, Finset.mem_image, Finset.mem_univ, true_and] at hx
  obtain ⟨⟨j, k⟩, rfl⟩ := hx
  dsimp [blockGenerator]
  have hj : (19 : ℤ) ^ j.1 ≤ (19 : ℤ) ^ (m - 1) := pow_nineteen_mono (by omega)
  have hk := blockWeights_le_eight k
  have hp := one_le_pow_nineteen j.1
  have hw := blockWeights_pos k
  nlinarith

lemma blockGenerator_ne_of_lt {j₁ j₂ : ℕ} (h : j₁ < j₂) (k₁ k₂ : Fin 3) :
    blockGenerator j₁ k₁ ≠ blockGenerator j₂ k₂ := by
  intro h_eq
  dsimp [blockGenerator] at h_eq
  have hj : j₂ = j₁ + 1 + (j₂ - j₁ - 1) := by omega
  have hpow : (19 : ℤ) ^ j₂ = (19 : ℤ) ^ j₁ * (19 * (19 : ℤ) ^ (j₂ - j₁ - 1)) := by
    conv_lhs => rw [hj]
    rw [pow_add, pow_add, pow_one]
    ring
  rw [hpow] at h_eq
  have hcancel : (19 : ℤ) ^ j₁ * (blockWeights k₁ - 19 * (19 : ℤ) ^ (j₂ - j₁ - 1) * blockWeights k₂) = 0 := by
    linarith
  have hpos : (1 : ℤ) ≤ (19 : ℤ) ^ j₁ := one_le_pow_nineteen j₁
  cases mul_eq_zero.mp hcancel with
  | inl hzero => linarith
  | inr hdiff =>
      have hp2 : (1 : ℤ) ≤ (19 : ℤ) ^ (j₂ - j₁ - 1) := one_le_pow_nineteen _
      have hw2 := blockWeights_pos k₂
      have hw1 := blockWeights_le_eight k₁
      nlinarith

theorem blockGenerator_injective :
    ∀ (j₁ j₂ : ℕ) (k₁ k₂ : Fin 3),
      blockGenerator j₁ k₁ = blockGenerator j₂ k₂ → j₁ = j₂ ∧ k₁ = k₂ := by
  intro j₁ j₂ k₁ k₂ h_eq
  rcases lt_trichotomy j₁ j₂ with hlt | heq | hgt
  · exact (blockGenerator_ne_of_lt hlt k₁ k₂ h_eq).elim
  · subst heq
    have : blockWeights k₁ = blockWeights k₂ := by
      dsimp [blockGenerator] at h_eq
      have hcancel : (19 : ℤ) ^ j₁ * (blockWeights k₁ - blockWeights k₂) = 0 := by linarith
      have hpos := one_le_pow_nineteen j₁
      cases mul_eq_zero.mp hcancel with
      | inl hz => linarith
      | inr hd => linarith
    exact ⟨rfl, blockWeights_injective this⟩
  · exact (blockGenerator_ne_of_lt hgt k₂ k₁ h_eq.symm).elim

theorem generators_injective (m : ℕ) :
    ∀ (a b : Fin m × Fin 3),
      blockGenerator a.1.1 a.2 = blockGenerator b.1.1 b.2 → a = b := by
  rintro ⟨j₁, k₁⟩ ⟨j₂, k₂⟩ h
  obtain ⟨hj, hk⟩ := blockGenerator_injective j₁.1 j₂.1 k₁ k₂ h
  have hj_fin : j₁ = j₂ := Fin.ext hj
  subst hj_fin; subst hk
  rfl

theorem card_generators (m : ℕ) : (generators m).card = 3 * m := by
  dsimp [generators]
  rw [Finset.card_image_of_injective _ (generators_injective m)]
  simp only [Finset.card_univ, Fintype.card_prod, Fintype.card_fin]
  ring

/-!
### Bridge to Evaluated Blocks
-/

theorem evaluateBlocks_ofFn (m : ℕ) (e : Fin m → BlockChoice) :
    evaluateBlocks (List.ofFn e) = ∑ j : Fin m, (19 : ℤ) ^ j.1 * blockValue (e j) := by
  induction m with
  | zero =>
      simp [List.ofFn_zero, evaluateBlocks]
  | succ m ih =>
      rw [List.ofFn_succ, evaluateBlocks]
      rw [ih (fun i => e i.succ)]
      rw [Finset.mul_sum]
      rw [Fin.sum_univ_succ]
      congr 1
      · simp [pow_zero]
      · apply Finset.sum_congr rfl
        intro i _
        have : (19 : ℤ) ^ i.succ.1 = 19 * (19 : ℤ) ^ i.1 := by
          change (19 : ℤ) ^ (i.1 + 1) = 19 * (19 : ℤ) ^ i.1
          rw [pow_succ]
          ring
        rw [this]
        ring

lemma generators_preimage_image (m : ℕ) (s : Finset ℤ) (hs : s ⊆ generators m) :
    (Finset.univ.filter (fun (jk : Fin m × Fin 3) => blockGenerator jk.1.1 jk.2 ∈ s)).image
      (fun jk => blockGenerator jk.1.1 jk.2) = s := by
  ext x
  simp only [Finset.mem_image, Finset.mem_filter, Finset.mem_univ, true_and]
  constructor
  · rintro ⟨jk, hmem, rfl⟩
    exact hmem
  · intro hx
    have hx_gen := hs hx
    simp only [generators, Finset.mem_image, Finset.mem_univ, true_and] at hx_gen
    obtain ⟨jk, rfl⟩ := hx_gen
    exact ⟨jk, hx, rfl⟩

lemma sum_generators_eq_sum_filter (m : ℕ) (s : Finset ℤ) (hs : s ⊆ generators m) :
    ∑ x ∈ s, x =
      ∑ jk ∈ Finset.univ.filter (fun (jk : Fin m × Fin 3) => blockGenerator jk.1.1 jk.2 ∈ s),
        blockGenerator jk.1.1 jk.2 := by
  conv_lhs => rw [← generators_preimage_image m s hs]
  rw [Finset.sum_image]
  intro a _ b _ hab
  exact generators_injective m a b hab

lemma sum_filter_eq_double_sum (m : ℕ) (s : Finset ℤ) :
    (∑ jk ∈ Finset.univ.filter (fun (jk : Fin m × Fin 3) => blockGenerator jk.1.1 jk.2 ∈ s),
      blockGenerator jk.1.1 jk.2) =
    ∑ j : Fin m, ∑ k ∈ Finset.univ.filter (fun k => blockGenerator j.1 k ∈ s),
      blockGenerator j.1 k := by
  rw [Finset.sum_filter]
  have hprod : (Finset.univ : Finset (Fin m × Fin 3)) =
      (Finset.univ : Finset (Fin m)) ×ˢ (Finset.univ : Finset (Fin 3)) := by
    exact Finset.univ_product_univ.symm
  rw [hprod, Finset.sum_product]
  apply Finset.sum_congr rfl
  intro j _
  rw [Finset.sum_filter]

lemma mul_blockValue_eq_sum (m : ℕ) (j : Fin m) (s : Finset ℤ) :
    (19 : ℤ) ^ j.1 * blockValue (fun k => decide (blockGenerator j.1 k ∈ s)) =
      ∑ k ∈ Finset.univ.filter (fun k => blockGenerator j.1 k ∈ s), blockGenerator j.1 k := by
  have he : (fun k => decide (blockGenerator j.1 k ∈ s)) =
      finsetToBlock (Finset.univ.filter (fun k => blockGenerator j.1 k ∈ s)) := by
    ext k
    simp [finsetToBlock]
  rw [he, blockValue_finsetToBlock]
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro k _
  rfl

theorem subsetSums_generators_subset_evaluatedBlocksSet (m : ℕ) :
    subsetSums (generators m) ⊆ evaluatedBlocksSet m := by
  rintro _ ⟨s, hs, rfl⟩
  refine ⟨List.ofFn (fun j k => decide (blockGenerator j.1 k ∈ s)), List.length_ofFn, ?_⟩
  rw [evaluateBlocks_ofFn]
  simp_rw [mul_blockValue_eq_sum]
  rw [← sum_filter_eq_double_sum]
  rw [← sum_generators_eq_sum_filter m s hs]

/-- The subset sums of `generators m` are 4-AP-free. -/
theorem generators_fourAPFree (m : ℕ) : FourAPFree (subsetSums (generators m)) :=
  evaluatedBlocks_subset_fourAPFree (subsetSums_generators_subset_evaluatedBlocksSet m)

/-!
### The Main Finite Upper Bound Theorem
-/

/-- Main Upper Bound Theorem for Erdős Problem 817 (`k = 4`):
For any $n > 0$, there exists an $n$-element set $B \subset \mathbb{Z}$ of positive integers
bounded above by $8 \cdot 19^{\lceil n/3 \rceil - 1}$ whose subset sums are 4-AP-free. -/
theorem erdos_problem_817_upper_bound (n : ℕ) (hn : 0 < n) :
    ∃ (B : Finset ℤ), B.card = n ∧
      (∀ b ∈ B, 1 ≤ b ∧ b ≤ 8 * 19 ^ ((n + 2) / 3 - 1)) ∧
      FourAPFree (subsetSums B) := by
  let m := (n + 2) / 3
  have hm : 1 ≤ m := by omega
  have hle : n ≤ (generators m).card := by
    rw [card_generators]
    omega
  obtain ⟨B, hB_sub, hB_card⟩ := Finset.exists_subset_card_eq hle
  refine ⟨B, hB_card, ?_, ?_⟩
  · intro b hb
    have hb_gen := hB_sub hb
    exact ⟨generators_pos m b hb_gen, generators_le m hm b hb_gen⟩
  · exact fourAPFree_subsetSums_of_subset hB_sub (generators_fourAPFree m)

#print axioms card_generators
#print axioms subsetSums_generators_subset_evaluatedBlocksSet
#print axioms generators_fourAPFree
#print axioms erdos_problem_817_upper_bound

end ErdosProblem817
