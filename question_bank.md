# Cambridge-Style Maths Interview Question Bank

42 original problems for a strong Year 13 student (A-level Mathematics and Further Mathematics; no university content). Each problem has a short statement and three parts that get harder. Thinking aloud with hints, a problem should take **12–15 minutes in total**, roughly 3, 4–5 and 5–6 minutes for parts (a), (b) and (c).

**How to use the hints.** Each part has a three-rung hint ladder. Give one rung at a time, and only after the candidate has been stuck for a minute or so:

1. *Nudge*: a question that points at the right object without saying what to do with it.
2. *Direction*: names the method or the key idea.
3. *Step*: carries out the first concrete step and leaves the rest to the candidate.

The model answers are concise. They show the expected route and the result, not every line. The optional follow-up is for candidates who finish early, and comes with a short answer.

**Verification.** `verify_answers.py` checks every model answer that can be checked numerically (brute force on small cases, exact arithmetic, simulation, numerical integration, ODE solving and limits). Before checking a value, it confirms that the value appears in the text below. Run `python3 verify_answers.py`. The end of its report lists the answers that are proofs, which can only be spot-checked.

**Conventions.** ℕ = {1, 2, 3, …}; ln is the natural logarithm; C(n, k) is the binomial coefficient "n choose k"; angles are in radians unless degrees are shown; x_n and x_{n+1} denote subscripts.

## Contents

| ID | Title | Topic |
|----|-------|-------|
| Q01 | Sums of consecutive integers | Number theory |
| Q02 | A divisibility pattern | Number theory |
| Q03 | Last digits of large powers | Number theory |
| Q04 | Waiting for patterns in coin tosses | Probability |
| Q05 | Breaking a stick | Probability |
| Q06 | A frog between a snake and home | Probability |
| Q07 | Lattice paths | Counting |
| Q08 | Letters in the wrong envelopes | Counting |
| Q09 | Stars, bars and gaps | Counting |
| Q10 | Telescoping sums | Sequences and series |
| Q11 | An iterated square root | Sequences and series |
| Q12 | Comparison without the name | Sequences and series |
| Q13 | AM–GM and a trap | Inequalities |
| Q14 | Sums of squares and constrained minima | Inequalities |
| Q15 | How big is (1 + 1/n)^n? | Inequalities |
| Q16 | Additive functions | Functional equations |
| Q17 | Solving functional equations by substitution | Functional equations |
| Q18 | A function that triples when applied twice | Functional equations |
| Q19 | Tangents to a parabola | Coordinate geometry |
| Q20 | Apollonius circles and common tangents | Coordinate geometry |
| Q21 | The reachable region of a projectile | Mechanics |
| Q22 | A bouncing ball | Mechanics |
| Q23 | When does the ladder slip? | Mechanics |
| Q24 | Fifth roots of unity | Complex numbers |
| Q25 | Equilateral triangles in the complex plane | Complex numbers |
| Q26 | Binomial sums and roots of unity | Complex numbers |
| Q27 | Logistic growth with harvesting | Differential equations |
| Q28 | Curves defined by their tangents | Differential equations |
| Q29 | Symmetric functions of roots | Polynomials |
| Q30 | Remainders of a big power | Polynomials |
| Q31 | Integer polynomials | Polynomials |
| Q32 | Induction warm-ups and the stamp problem | Induction |
| Q33 | Fibonacci identities | Induction |
| Q34 | Sketching a rational function | Curve sketching |
| Q35 | Counting solutions with a sketch | Curve sketching |
| Q36 | A curve with a loop | Curve sketching |
| Q37 | Skew lines | Vectors |
| Q38 | Medians by vectors | Vectors |
| Q39 | Tilings and strings | Recurrences |
| Q40 | Solving recurrences | Recurrences |
| Q41 | Irrationality and parity | Proof by contradiction |
| Q42 | Primes and polynomials | Proof by contradiction |

---

## Q01 · Sums of consecutive integers

**Topic:** Number theory

**Statement.** Some positive integers can be written as a sum of two or more consecutive positive integers, for example 9 = 4 + 5 = 2 + 3 + 4. Which integers can be written like this, and in how many ways?

### Part (a)
Write 15 and 30 as sums of two or more consecutive positive integers in every possible way.

**Hints**
1. *Nudge:* Try two terms, then three, then four. When can you stop?
2. *Direction:* With k terms, the average of the terms is the middle term (k odd) or halfway between the two middle terms (k even).
3. *Step:* So N/k must be an integer when k is odd and an integer plus ½ when k is even, and the smallest term N/k − (k − 1)/2 must be at least 1.

**Model answer.** 15 = 7+8 = 4+5+6 = 1+2+3+4+5 (3 ways). 30 = 9+10+11 = 6+7+8+9 = 4+5+6+7+8 (3 ways). For 30, k = 2 fails because 15 is not a half-integer, and for k ≥ 8 the smallest term would be below 1.

### Part (b)
Show that the sum of k consecutive integers starting at a is k(2a + k − 1)/2. Deduce that no power of 2 can be written in this way.

**Hints**
1. *Nudge:* Pair the first term with the last.
2. *Direction:* If N = 2^m, then k(2a + k − 1) = 2^{m+1}. Look at the parities of the two factors.
3. *Step:* The factors k and 2a + k − 1 differ by 2a − 1, which is odd, so exactly one of them is odd. Both are at least 2.

**Model answer.** Sum = k × (first + last)/2 = k(2a + k − 1)/2. If this equals 2^m then k(2a + k − 1) = 2^{m+1}. One factor is odd, and the only odd divisor of 2^{m+1} is 1, but k ≥ 2 and 2a + k − 1 ≥ 3. This is a contradiction, so no power of 2 (including 1) can be written in this way.

### Part (c)
Show that every N that is not a power of 2 can be written in this way, and that the number of ways is (number of odd divisors of N) − 1.

**Hints**
1. *Nudge:* In (a), 15 and 30 both had 3 ways, and both have odd divisors 1, 3, 5, 15. Coincidence?
2. *Direction:* Write 2N = k × m with k < m. Each such factorisation with k, m of opposite parity gives one representation: k terms starting at a = (m − k + 1)/2.
3. *Step:* A factorisation of 2N into factors of opposite parity is fixed by choosing the odd factor d, which is an odd divisor of N. Take k = min(d, 2N/d). Which d gives k = 1?

**Model answer.** Representations correspond to pairs (k, m) with km = 2N, 2 ≤ k < m and k, m of opposite parity. Then a = (m − k + 1)/2 is a positive integer. Each odd divisor d of N gives the pair {d, 2N/d}, one odd and one even, so the two are never equal. Let k be the smaller of the two. This gives a valid representation unless k = 1, which happens only for d = 1, because 2N/d is even and so at least 2. The number of ways is therefore (number of odd divisors) − 1. This is positive exactly when N has an odd divisor greater than 1, i.e. when N is not a power of 2.

### Follow-up (optional)
Which N can be written in exactly one way?

**Answer.** Those with exactly two odd divisors: N = 2^a × p with p an odd prime and a ≥ 0.

---

## Q02 · A divisibility pattern

**Topic:** Number theory

**Statement.** For n = 2, 3, 4 the numbers n⁵ − n are 30, 240 and 1020. They seem to share a factor.

### Part (a)
Show that n³ − n is divisible by 6 for every integer n.

**Hints**
1. *Nudge:* Can you factorise n³ − n?
2. *Direction:* n³ − n = (n − 1)n(n + 1). What do you know about three consecutive integers?
3. *Step:* Among three consecutive integers, one is a multiple of 3 and at least one is even.

**Model answer.** n³ − n = (n − 1)n(n + 1) is a product of three consecutive integers. One of them is divisible by 3 and one by 2. Since 2 and 3 are coprime, 6 divides n³ − n.

### Part (b)
Show that n⁵ − n is divisible by 30 for every integer n.

**Hints**
1. *Nudge:* Does n⁵ − n contain n³ − n as a factor?
2. *Direction:* n⁵ − n = (n − 1)n(n + 1)(n² + 1), so it remains to show divisibility by 5.
3. *Step:* Check the five cases n ≡ 0, ±1, ±2 (mod 5). For n ≡ ±2, look at n² + 1.

**Model answer.** n⁵ − n = (n³ − n)(n² + 1), so 6 divides it by (a). Mod 5: if n ≡ 0 or ±1, one of n − 1, n, n + 1 is a multiple of 5. If n ≡ ±2, then n² + 1 ≡ 4 + 1 ≡ 0. So 5 divides n⁵ − n, and since gcd(5, 6) = 1, 30 divides n⁵ − n.

### Part (c)
What is the largest integer that divides n⁵ − n for every integer n? Justify your answer.

**Hints**
1. *Nudge:* Any such divisor must divide the value at one particular n. Which n gives the smallest positive value?
2. *Direction:* n = 2 gives 2⁵ − 2 = 30.
3. *Step:* So the answer divides 30, and (b) shows that 30 itself works.

**Model answer.** The largest such integer is 30: it must divide 2⁵ − 2 = 30, and (b) shows that 30 works.

### Follow-up (optional)
What is the largest integer dividing n⁷ − n for every integer n?

**Answer.** 42. It must divide 2⁷ − 2 = 126 = 2 × 3² × 7 and 3⁷ − 3 = 2184 = 2³ × 3 × 7 × 13, so it divides their gcd, 42. Conversely 2, 3 and 7 each divide n⁷ − n (check residues, or use Fermat's little theorem).

---

## Q03 · Last digits of large powers

**Topic:** Number theory

**Statement.** Without a calculator, find the final digits of some very large powers.

### Part (a)
Find the last digit of 7^2026.

**Hints**
1. *Nudge:* List the last digits of 7, 7², 7³, …
2. *Direction:* The last digits repeat with period 4.
3. *Step:* Find 2026 mod 4.

**Model answer.** The last digits cycle 7, 9, 3, 1 with period 4. Since 2026 ≡ 2 (mod 4), the last digit of 7^2026 is 9.

### Part (b)
Find the last two digits of 7^2026.

**Hints**
1. *Nudge:* Work mod 100. Is some small power of 7 congruent to 1?
2. *Direction:* 7² = 49 and 7⁴ = 2401.
3. *Step:* 7⁴ ≡ 1 (mod 100), and 7^2026 = (7⁴)^506 × 7².

**Model answer.** 7⁴ = 2401 ≡ 1 (mod 100), so 7^2026 = (7⁴)^506 × 49 ≡ 49. The last two digits are 49.

### Part (c)
Show that 3^20 ≡ 1 (mod 100), and hence find the last two digits of 3^2026 + 7^2026.

**Hints**
1. *Nudge:* Compute 3⁵ mod 100 and build up from there.
2. *Direction:* 3⁵ = 243 ≡ 43, so 3^10 ≡ 43² = 1849 ≡ 49.
3. *Step:* Then 3^20 ≡ 49² = 2401 ≡ 1, and 2026 = 20 × 101 + 6.

**Model answer.** 3^10 ≡ 43² ≡ 49 and 3^20 ≡ 49² ≡ 1 (mod 100). Since 2026 ≡ 6 (mod 20), 3^2026 ≡ 3⁶ = 729 ≡ 29. So 3^2026 + 7^2026 ≡ 29 + 49 = 78, and the last two digits are 78.

### Follow-up (optional)
Find the last two digits of 7^(7^7).

**Answer.** 43. Since 7⁴ ≡ 1 (mod 100), only the exponent mod 4 matters. 7^7 ≡ (−1)^7 ≡ 3 (mod 4), so 7^(7^7) ≡ 7³ = 343 ≡ 43 (mod 100).

---

## Q04 · Waiting for patterns in coin tosses

**Topic:** Probability

**Statement.** A fair coin is tossed repeatedly. How long, on average, do we wait until a given pattern appears?

### Part (a)
Find the expected number of tosses up to and including the first head.

**Hints**
1. *Nudge:* Let E be the answer. What can happen on the first toss?
2. *Direction:* With probability ½ you finish after one toss. Otherwise you have used one toss and are back where you started.
3. *Step:* E = 1 + ½ × 0 + ½ × E.

**Model answer.** E = 1 + E/2, so E = 2.

### Part (b)
Find the expected number of tosses until two consecutive heads (HH) first appear.

**Hints**
1. *Nudge:* Now you need to remember something about the previous toss.
2. *Direction:* Let E_0 be the expected number of tosses still needed from scratch, and E_1 the expected number still needed when the last toss was H.
3. *Step:* E_0 = 1 + ½E_1 + ½E_0 and E_1 = 1 + ½ × 0 + ½E_0.

**Model answer.** The first equation gives E_0 = 2 + E_1 and the second gives E_1 = 1 + E_0/2. Substituting, E_0 = 6.

### Part (c)
Find the expected number of tosses until HT first appears. Why is the answer different from HH?

**Hints**
1. *Nudge:* Set up states as in (b). If you are waiting for the T and you toss another H, how much progress have you lost?
2. *Direction:* For HT you never lose progress once you have an H, because an extra H still leaves you "one H ready".
3. *Step:* F_1 = 1 + ½ × 0 + ½F_1 and F_0 = 1 + ½F_1 + ½F_0.

**Model answer.** F_1 = 2 and F_0 = 2 + F_1 = 4. For HT, a failure after an H (another H) keeps you in the "H seen" state. For HH, a failure after an H (a T) sends you back to the start. So HT takes 4 tosses on average and HH takes 6.

### Follow-up (optional)
Players pick HH and TH, and the coin is tossed until one of the patterns appears. What is the probability that HH appears first?

**Answer.** 1/4. HH wins only if the first two tosses are HH. Once a T has appeared, the first HH must be preceded by a T, so TH occurs first.

---

## Q05 · Breaking a stick

**Topic:** Probability

**Statement.** A stick of length 1 is broken at a point chosen uniformly at random. In part (c) it is broken at two independent uniform points.

### Part (a)
With one break, find the expected length of the longer piece, and the probability that the longer piece is more than twice as long as the shorter.

**Hints**
1. *Nudge:* If the break is at U, the longer piece is max(U, 1 − U). By symmetry you may assume U ≤ ½.
2. *Direction:* Given U ≤ ½, U is uniform on [0, ½] and the longer piece is 1 − U.
3. *Step:* For U ≤ ½: longer > 2 × shorter ⇔ 1 − U > 2U ⇔ U < 1/3.

**Model answer.** E[longer] = E[1 − U | U ≤ ½] = 1 − ¼ = 3/4. For U ≤ ½ the condition is U < 1/3, which has probability (1/3)/(1/2) = 2/3. By symmetry the overall probability is also 2/3.

### Part (b)
Find the expected value of (shorter piece)/(longer piece).

**Hints**
1. *Nudge:* It is not (expected shorter)/(expected longer) = (1/4)/(3/4) = 1/3.
2. *Direction:* By symmetry the expectation is 2∫₀^{1/2} u/(1 − u) du.
3. *Step:* u/(1 − u) = −1 + 1/(1 − u).

**Model answer.** E = 2∫₀^{1/2} (−1 + 1/(1 − u)) du = 2[−u − ln(1 − u)] from 0 to ½ = 2(−½ + ln 2) = 2 ln 2 − 1 ≈ 0.386.

### Part (c)
Now break the stick at two independent uniform points. What is the probability that the three pieces form a triangle?

**Hints**
1. *Nudge:* When do three lengths with sum 1 form a triangle?
2. *Direction:* Exactly when every piece is shorter than ½. Represent the two break points (X, Y) as a point of the unit square.
3. *Step:* Take X < Y (half of the square). You need X < ½, Y − X < ½ and Y > ½. Sketch this region.

**Model answer.** A triangle forms ⇔ all pieces are shorter than ½. Inside the triangle 0 < X < Y < 1 (area ½), the conditions X < ½, Y > ½ and Y − X < ½ cut out a triangle of area 1/8. The probability is (1/8)/(1/2) = 1/4.

### Follow-up (optional)
With two breaks, what is the expected length of the shortest piece?

**Answer.** 1/9. For s ≤ 1/3, P(shortest > s) = (1 − 3s)², so E = ∫₀^{1/3} (1 − 3s)² ds = 1/9.

---

## Q06 · A frog between a snake and home

**Topic:** Probability

**Statement.** Lily pads are numbered 0 to 4. A snake waits on pad 0 and the frog's home is pad 4. The frog starts on pad 1. Each second it jumps one pad left or right, independently of the past, and it stops when it reaches pad 0 or pad 4.

### Part (a)
If left and right are equally likely, what is the probability that the frog gets home?

**Hints**
1. *Nudge:* Let p_k be the probability of getting home from pad k. What are p_0 and p_4?
2. *Direction:* p_k = ½p_{k−1} + ½p_{k+1} for k = 1, 2, 3.
3. *Step:* That says each p_k is the average of its neighbours, so the points (k, p_k) lie on a straight line.

**Model answer.** p_k is linear in k with p_0 = 0 and p_4 = 1, so p_k = k/4 and the answer is p_1 = 1/4.

### Part (b)
Still with fair jumps, find the expected number of jumps before the frog stops, starting from pad 1.

**Hints**
1. *Nudge:* Let T_k be the expected number of jumps from pad k, so T_0 = T_4 = 0.
2. *Direction:* T_k = 1 + ½T_{k−1} + ½T_{k+1}.
3. *Step:* By symmetry T_1 = T_3. Write down the equations for T_1 and T_2.

**Model answer.** T_1 = 1 + ½T_2 and T_2 = 1 + ½T_1 + ½T_3 = 1 + T_1. So T_1 = 1 + ½(1 + T_1), giving T_1 = 3. (In general T_k = k(4 − k).)

### Part (c)
Now the frog jumps right with probability 2/3 and left with probability 1/3. Find the probability that it gets home from pad 1.

**Hints**
1. *Nudge:* The idea is the same as in (a), but p_k is no longer the average of its neighbours.
2. *Direction:* p_k = (2/3)p_{k+1} + (1/3)p_{k−1}. Rearrange in terms of the differences d_k = p_{k+1} − p_k.
3. *Step:* 2(p_{k+1} − p_k) = p_k − p_{k−1}, so each difference is half the previous one.

**Model answer.** d_k = d_0/2^k, and d_0 + d_1 + d_2 + d_3 = p_4 − p_0 = 1. So d_0(1 + ½ + ¼ + ⅛) = 1, giving d_0 = 8/15. Since p_0 = 0, the frog gets home from pad 1 with probability p_1 = 8/15.

### Follow-up (optional)
With fair jumps on pads 0, 1, …, N, show that the expected number of jumps starting from pad k is k(N − k). What is it on pads 0 to 10, starting at pad 5?

**Answer.** T_k = k(N − k) satisfies T_k = 1 + ½T_{k−1} + ½T_{k+1} and T_0 = T_N = 0, and that system has only one solution. For N = 10, k = 5 the answer is 25.

---

## Q07 · Lattice paths

**Topic:** Counting

**Statement.** A path on the integer grid starts at (0, 0) and moves in unit steps, each Right (R) or Up (U).

### Part (a)
How many paths go from (0, 0) to (4, 3)?

**Hints**
1. *Nudge:* Describe a path as a word in R and U. How many letters does it have?
2. *Direction:* Every arrangement of 4 R's and 3 U's gives exactly one path.
3. *Step:* Choose which 3 of the 7 positions hold a U.

**Model answer.** C(7, 3) = 35.

### Part (b)
How many of these paths avoid the point (2, 1)?

**Hints**
1. *Nudge:* It is easier to count the paths that do pass through (2, 1).
2. *Direction:* A path through (2, 1) is a path (0, 0) → (2, 1) followed by a path (2, 1) → (4, 3).
3. *Step:* Count each piece as in (a), then multiply.

**Model answer.** Through (2, 1): C(3, 1) × C(4, 2) = 3 × 6 = 18. Avoiding it: 35 − 18 = 17.

### Part (c)
How many paths from (0, 0) to (4, 4) never go above the line y = x? Find a formula for paths to (n, n).

**Hints**
1. *Nudge:* Work out the small cases n = 1, 2, 3 by hand.
2. *Direction:* Count the bad paths instead: these are the paths that touch the line y = x + 1. Reflect the part of a bad path up to its first touch of y = x + 1 in that line.
3. *Step:* The reflection turns a bad path into an arbitrary path from (−1, 1) to (n, n), and this is a bijection.

**Model answer.** Bad paths correspond to all paths from (−1, 1) to (n, n), of which there are C(2n, n + 1). So the number of good paths is C(2n, n) − C(2n, n + 1) = C(2n, n)/(n + 1). For n = 4 this is 70 − 56 = 14. The small cases 1, 2, 5, 14 are the Catalan numbers.

### Follow-up (optional)
How many paths from (0, 0) to (n, n) touch the line y = x only at their two ends, staying strictly below it in between?

**Answer.** The first step must be R and the last must be U. In between, the path goes from (1, 0) to (n, n − 1) without going above y = x − 1, so there are C(2n − 2, n − 1)/n of them. For n = 4 that is 5.

---

## Q08 · Letters in the wrong envelopes

**Topic:** Counting

**Statement.** n letters are put at random into n addressed envelopes, one per envelope. A derangement is an arrangement with no letter in its own envelope. Let D_n be the number of derangements.

### Part (a)
Find D_2, D_3 and D_4.

**Hints**
1. *Nudge:* List them for n = 3.
2. *Direction:* For n = 4, letter 1 goes into envelope 2, 3 or 4. By symmetry, count the case "letter 1 in envelope 2" and multiply by 3.
3. *Step:* If letter 1 is in envelope 2, either letter 2 is in envelope 1 or it is not.

**Model answer.** D_2 = 1, D_3 = 2, D_4 = 9. With letter 1 in envelope 2, there is 1 way with letter 2 in envelope 1 and 2 ways otherwise, giving 3; multiply by 3.

### Part (b)
Show that D_n = (n − 1)(D_{n−1} + D_{n−2}), and compute D_5 and D_6.

**Hints**
1. *Nudge:* Generalise the case split you used for n = 4.
2. *Direction:* Letter 1 goes into envelope k (n − 1 choices). Split on whether letter k goes into envelope 1.
3. *Step:* If it does, the other n − 2 letters form a derangement. If it does not, treat envelope 1 as letter k's "own" envelope.

**Model answer.** Fix one of the n − 1 choices of k. If letter k is in envelope 1, the remaining letters give D_{n−2} ways. Otherwise letters 2, …, n must avoid their own envelopes, with envelope 1 playing the role of envelope k, which gives D_{n−1} ways. So D_n = (n − 1)(D_{n−1} + D_{n−2}). Then D_5 = 4(9 + 2) = 44 and D_6 = 5(44 + 9) = 265.

### Part (c)
Use inclusion–exclusion to show that D_n = n! Σ_{k=0}^{n} (−1)^k/k!. What happens to the probability that no letter is in its own envelope as n → ∞?

**Hints**
1. *Nudge:* Let A_i be the set of arrangements in which letter i is in its own envelope. How big is A_i ∩ A_j?
2. *Direction:* Any k of the sets have an intersection of size (n − k)!, and there are C(n, k) ways to choose the k letters.
3. *Step:* The number of arrangements with at least one correct letter is Σ_{k≥1} (−1)^{k+1} C(n, k)(n − k)!.

**Model answer.** D_n = Σ_{k=0}^{n} (−1)^k C(n, k)(n − k)! = n! Σ (−1)^k/k!. So P(no letter correct) = Σ_{k=0}^{n} (−1)^k/k!, which tends to e^{−1} ≈ 0.3679 (the Maclaurin series of e^x at x = −1). Already D_6/6! = 265/720 ≈ 0.3681.

### Follow-up (optional)
How many arrangements of 6 letters have exactly two letters in their own envelopes?

**Answer.** C(6, 2) × D_4 = 15 × 9 = 135.

---

## Q09 · Stars, bars and gaps

**Topic:** Counting

**Statement.** Count solutions of equations, and choices with gaps.

### Part (a)
How many solutions does a + b + c = 10 have in non-negative integers?

**Hints**
1. *Nudge:* Represent a solution as 10 stars split into three groups.
2. *Direction:* Place 2 bars among the stars: ★★|★★★★★|★★★ stands for (2, 5, 3).
3. *Step:* Choose the positions of the 2 bars among 12 symbols.

**Model answer.** C(12, 2) = 66.

### Part (b)
How many of these solutions have a, b, c ≤ 4?

**Hints**
1. *Nudge:* Count the solutions in which some variable is too big, and subtract.
2. *Direction:* If a ≥ 5, put a' = a − 5. Then a' + b + c = 5.
3. *Step:* By inclusion–exclusion the answer is 66 − 3 × (solutions with a ≥ 5) + 3 × (solutions with a, b ≥ 5).

**Model answer.** Solutions with a ≥ 5: C(7, 2) = 21. With a, b ≥ 5: 1. With all three ≥ 5: 0. So 66 − 63 + 3 = 6. Check: the permutations of (4, 4, 2) and (4, 3, 3).

### Part (c)
In how many ways can you choose 3 numbers from {1, 2, …, 20} with no two consecutive?

**Hints**
1. *Nudge:* Write the chosen numbers as x < y < z. What do you know about y − x?
2. *Direction:* Consider x, y − 1, z − 2.
3. *Step:* The map (x, y, z) ↦ (x, y − 1, z − 2) is a bijection onto all 3-element subsets of {1, …, 18}.

**Model answer.** The bijection gives C(18, 3) = 816. (In general the answer is C(n − k + 1, k).)

### Follow-up (optional)
Twenty people sit at a round table. In how many ways can 3 of them be chosen with no two sitting next to each other?

**Answer.** 800. If person 1 is chosen, persons 2 and 20 are excluded, and we choose 2 non-adjacent people from the line 3, …, 19 (17 people): C(16, 2) = 120. If person 1 is not chosen, we choose 3 non-adjacent people from the line 2, …, 20 (19 people): C(17, 3) = 680.

---

## Q10 · Telescoping sums

**Topic:** Sequences and series

**Statement.** Evaluate sums by making them collapse.

### Part (a)
Find Σ_{r=1}^{n} 1/(r(r + 1)).

**Hints**
1. *Nudge:* Work out the sum for n = 1, 2, 3 and guess.
2. *Direction:* Use partial fractions.
3. *Step:* 1/(r(r + 1)) = 1/r − 1/(r + 1).

**Model answer.** The sum telescopes to 1 − 1/(n + 1) = n/(n + 1).

### Part (b)
Find Σ_{r=1}^{n} 1/(r(r + 1)(r + 2)) and its limit as n → ∞.

**Hints**
1. *Nudge:* Can you write the term as a difference of two terms of a similar shape?
2. *Direction:* Work out 1/(r(r + 1)) − 1/((r + 1)(r + 2)).
3. *Step:* That difference equals 2/(r(r + 1)(r + 2)).

**Model answer.** The term is ½[1/(r(r + 1)) − 1/((r + 1)(r + 2))], so the sum is ½[½ − 1/((n + 1)(n + 2))] = 1/4 − 1/(2(n + 1)(n + 2)), which tends to 1/4.

### Part (c)
Find Σ_{r=1}^{∞} r/(r + 1)!.

**Hints**
1. *Nudge:* Write r = (r + 1) − 1.
2. *Direction:* Then r/(r + 1)! = (r + 1)/(r + 1)! − 1/(r + 1)!.
3. *Step:* (r + 1)/(r + 1)! = 1/r!.

**Model answer.** r/(r + 1)! = 1/r! − 1/(r + 1)!, so the partial sum up to n is 1 − 1/(n + 1)!, which tends to 1. The sum is 1.

### Follow-up (optional)
Find Σ_{r=1}^{∞} (2r + 1)/(r²(r + 1)²).

**Answer.** 1, because (2r + 1)/(r²(r + 1)²) = 1/r² − 1/(r + 1)², so the partial sum is 1 − 1/(n + 1)².

---

## Q11 · An iterated square root

**Topic:** Sequences and series

**Statement.** Define x_1 = √2 and x_{n+1} = √(2 + x_n), so that x_2 = √(2 + √2), and so on.

### Part (a)
Estimate x_2 and x_3. If the sequence converges, what must the limit be?

**Hints**
1. *Nudge:* What is √(2 + 1.414), roughly?
2. *Direction:* If x_n → L, then L = √(2 + L).
3. *Step:* Square: L² − L − 2 = 0. Which root is possible?

**Model answer.** x_2 ≈ 1.848 and x_3 ≈ 1.962. L² = L + 2 gives L = 2 or L = −1. Since x_n > 0, the limit must be L = 2.

### Part (b)
Prove by induction that √2 ≤ x_n < x_{n+1} < 2 for all n.

**Hints**
1. *Nudge:* What do you need to assume about x_n and x_{n+1} in order to say something about x_{n+1} and x_{n+2}?
2. *Direction:* The function t ↦ √(2 + t) is increasing.
3. *Step:* If x_n < x_{n+1} < 2, apply t ↦ √(2 + t) to all three parts.

**Model answer.** Base case: x_1 = √2 < x_2 = √(2 + √2) < 2. Step: if x_n < x_{n+1} < 2 then √(2 + x_n) < √(2 + x_{n+1}) < √4, i.e. x_{n+1} < x_{n+2} < 2. So the sequence is increasing, starts at √2 and is bounded above by 2.

### Part (c)
Show that 2 − x_{n+1} = (2 − x_n)/(2 + x_{n+1}). Deduce that 0 < 2 − x_n ≤ (2 − √2)/3^{n−1}, and conclude that x_n → 2.

**Hints**
1. *Nudge:* Use a difference of two squares: 4 − x_{n+1}² = (2 − x_{n+1})(2 + x_{n+1}).
2. *Direction:* 4 − x_{n+1}² = 2 − x_n.
3. *Step:* Since x_{n+1} ≥ √2 > 1, we have 2 + x_{n+1} > 3.

**Model answer.** (2 − x_{n+1})(2 + x_{n+1}) = 4 − (2 + x_n) = 2 − x_n, which gives the identity. As 2 + x_{n+1} > 3, the gap shrinks by more than a factor of 3 at each step, so 2 − x_n ≤ (2 − x_1)/3^{n−1} = (2 − √2)/3^{n−1}, with equality only for n = 1. The bound tends to 0, so x_n → 2.

### Follow-up (optional)
For a constant c > 0, let x_1 = √c and x_{n+1} = √(c + x_n). What is the limit?

**Answer.** (1 + √(1 + 4c))/2, by the same argument. For example, c = 6 gives 3.

---

## Q12 · Comparison without the name

**Topic:** Sequences and series

**Statement.** Decide whether some infinite sums are finite by comparing them with sums you understand.

### Part (a)
Show that 1 + 1/2 + 1/3 + … + 1/2^k ≥ 1 + k/2, and deduce that Σ 1/n diverges.

**Hints**
1. *Nudge:* Group the terms: 1/3 + 1/4, then 1/5 + … + 1/8, and so on.
2. *Direction:* The group 1/(2^{j−1} + 1) + … + 1/2^j has 2^{j−1} terms.
3. *Step:* Each term in that group is at least 1/2^j.

**Model answer.** Each of the k groups (j = 1, …, k) has 2^{j−1} terms, each at least 1/2^j, so each group contributes at least ½. Hence 1 + 1/2 + … + 1/2^k ≥ 1 + k/2. This is unbounded as k grows, so the series diverges.

### Part (b)
Show that Σ_{n=1}^{N} 1/n² < 2 for every N.

**Hints**
1. *Nudge:* Find a slightly bigger term that you can sum exactly.
2. *Direction:* For n ≥ 2, 1/n² < 1/(n(n − 1)).
3. *Step:* 1/(n(n − 1)) = 1/(n − 1) − 1/n, which telescopes.

**Model answer.** Σ_{n=1}^{N} 1/n² < 1 + Σ_{n=2}^{N} (1/(n − 1) − 1/n) = 1 + 1 − 1/N = 2 − 1/N < 2.

### Part (c)
Let S be the sum of 1/n over all positive integers n with no digit 9 in their decimal expansion. Show that S < 80.

**Hints**
1. *Nudge:* Group the numbers by how many digits they have.
2. *Direction:* How many k-digit numbers have no digit 9? What is the largest reciprocal among them?
3. *Step:* There are 8 × 9^{k−1} of them (8 choices for the first digit, 9 for each other digit), and each is at least 10^{k−1}.

**Model answer.** The k-digit numbers contribute at most 8 × 9^{k−1}/10^{k−1} = 8 × 0.9^{k−1}. Summing the geometric series, S < 8/(1 − 0.9) = 80. Removing this "thin" set of terms turns a divergent series into a convergent one.

### Follow-up (optional)
Improve (b) to show that Σ 1/n² ≤ 7/4.

**Answer.** Keep the first two terms exact and compare from n = 3 onwards: 1 + 1/4 + Σ_{n≥3} (1/(n − 1) − 1/n) = 1 + 1/4 + 1/2 = 7/4. (The true value is π²/6 ≈ 1.645.)

---

## Q13 · AM–GM and a trap

**Topic:** Inequalities

**Statement.** The AM–GM inequality, and how to use it carefully.

### Part (a)
Prove that (a + b)/2 ≥ √(ab) for positive a, b, with equality if and only if a = b.

**Hints**
1. *Nudge:* Squares are never negative.
2. *Direction:* Consider (√a − √b)².
3. *Step:* Expand (√a − √b)² ≥ 0.

**Model answer.** (√a − √b)² = a − 2√(ab) + b ≥ 0, so (a + b)/2 ≥ √(ab), with equality if and only if √a = √b.

### Part (b)
Find the minimum value of (x² + 3)/√(x² + 2) over all real x.

**Hints**
1. *Nudge:* Writing the expression as √(x² + 2) + 1/√(x² + 2) suggests that AM–GM gives ≥ 2. Is 2 actually achieved?
2. *Direction:* Let t = √(x² + 2). What values can t take?
3. *Step:* Minimise t + 1/t over t ≥ √2, not over all t > 0.

**Model answer.** With t = √(x² + 2) ≥ √2, the expression is t + 1/t. AM–GM gives ≥ 2, but equality would need t = 1, which is impossible. Since t + 1/t is increasing for t ≥ 1 (its derivative is 1 − 1/t² > 0), the minimum is at t = √2 (x = 0), with value √2 + 1/√2 = 3/√2 = 3√2/2 ≈ 2.121.

### Part (c)
Using the AM–GM inequality for three numbers, (p + q + r)/3 ≥ ∛(pqr), find the minimum of x + 4/x² for x > 0.

**Hints**
1. *Nudge:* AM–GM applied to x and 4/x² directly leaves an x in the product.
2. *Direction:* Split x into two equal parts so that the product is constant.
3. *Step:* x + 4/x² = x/2 + x/2 + 4/x².

**Model answer.** x/2 + x/2 + 4/x² ≥ 3∛((x/2)(x/2)(4/x²)) = 3∛1 = 3, with equality when x/2 = 4/x², i.e. x = 2. The minimum is 3.

### Follow-up (optional)
Show that (a + b)(b + c)(c + a) ≥ 8abc for positive a, b, c.

**Answer.** Multiply the three inequalities a + b ≥ 2√(ab), b + c ≥ 2√(bc) and c + a ≥ 2√(ca).

---

## Q14 · Sums of squares and constrained minima

**Topic:** Inequalities

**Statement.** Inequalities that come from writing expressions as sums of squares.

### Part (a)
Show that a² + b² + c² ≥ ab + bc + ca for all real a, b, c.

**Hints**
1. *Nudge:* Multiply by 2.
2. *Direction:* Try to write 2(a² + b² + c²) − 2(ab + bc + ca) as a sum of squares.
3. *Step:* Consider (a − b)² + (b − c)² + (c − a)².

**Model answer.** 2(a² + b² + c² − ab − bc − ca) = (a − b)² + (b − c)² + (c − a)² ≥ 0, with equality if and only if a = b = c.

### Part (b)
If a + b + c = 3, show that a² + b² + c² ≥ 3 and ab + bc + ca ≤ 3.

**Hints**
1. *Nudge:* Expand (a + b + c)².
2. *Direction:* 9 = (a² + b² + c²) + 2(ab + bc + ca). Combine this with (a).
3. *Step:* Let S = a² + b² + c² and P = ab + bc + ca. Then S + 2P = 9 and S ≥ P.

**Model answer.** From S + 2P = 9 and S ≥ P: 9 ≤ 3S, so S ≥ 3; and 9 ≥ 3P, so P ≤ 3. Equality holds at a = b = c = 1.

### Part (c)
For positive x, y, z with x + y + z = 1, find the minimum of 1/x + 4/y + 9/z.

**Hints**
1. *Nudge:* Multiply by x + y + z (which equals 1) and expand.
2. *Direction:* You get 14 + (y/x + 4x/y) + (z/x + 9x/z) + (4z/y + 9y/z).
3. *Step:* Apply u + v ≥ 2√(uv) to each bracket.

**Model answer.** (1/x + 4/y + 9/z)(x + y + z) ≥ 14 + 2×2 + 2×3 + 2×6 = 36. Equality needs y = 2x and z = 3x, so (x, y, z) = (1/6, 1/3, 1/2), where the value is 6 + 12 + 18 = 36. The minimum is 36.

### Follow-up (optional)
For positive x, y, z with x + y + z = 1, find the maximum of xy²z³.

**Answer.** 1/432, at (x, y, z) = (1/6, 1/3, 1/2). Apply AM–GM to the six numbers x, y/2, y/2, z/3, z/3, z/3, whose sum is 1: x(y/2)²(z/3)³ ≤ (1/6)⁶, so xy²z³ ≤ 4 × 27/6⁶ = 1/432.

---

## Q15 · How big is (1 + 1/n)^n?

**Topic:** Inequalities

**Statement.** Bound the sequence a_n = (1 + 1/n)^n using the binomial theorem and AM–GM.

### Part (a)
Prove Bernoulli's inequality: (1 + x)^n ≥ 1 + nx for x ≥ −1 and every integer n ≥ 1. Deduce that a_n ≥ 2.

**Hints**
1. *Nudge:* Use induction on n.
2. *Direction:* Multiply (1 + x)^n ≥ 1 + nx by (1 + x). Why does the inequality survive?
3. *Step:* (1 + x)^{n+1} ≥ (1 + nx)(1 + x) = 1 + (n + 1)x + nx².

**Model answer.** The case n = 1 is an equality. If (1 + x)^n ≥ 1 + nx, multiply by 1 + x ≥ 0 to get (1 + x)^{n+1} ≥ 1 + (n + 1)x + nx² ≥ 1 + (n + 1)x. Putting x = 1/n gives a_n ≥ 1 + 1 = 2.

### Part (b)
Show that a_n < 3 for all n.

**Hints**
1. *Nudge:* Expand using the binomial theorem.
2. *Direction:* The k-th term is C(n, k)/n^k = (1/k!) × (n/n) × ((n − 1)/n) × … × ((n − k + 1)/n).
3. *Step:* So the k-th term is at most 1/k!, which is at most 1/2^{k−1} for k ≥ 1.

**Model answer.** a_n = Σ_{k=0}^{n} C(n, k)/n^k ≤ 1 + Σ_{k=1}^{n} 1/2^{k−1} = 1 + 2 − 1/2^{n−1} < 3.

### Part (c)
Show that a_n is increasing in n.

**Hints**
1. *Nudge:* Find n + 1 numbers whose product is a_n.
2. *Direction:* Apply AM–GM to n copies of (1 + 1/n) and one copy of 1.
3. *Step:* The arithmetic mean of these n + 1 numbers is (n + 2)/(n + 1).

**Model answer.** By AM–GM, ((n(1 + 1/n) + 1)/(n + 1))^{n+1} ≥ (1 + 1/n)^n × 1, i.e. (1 + 1/(n + 1))^{n+1} ≥ a_n, strictly because the numbers are not all equal. So a_{n+1} > a_n. (The limit is e ≈ 2.718.)

### Follow-up (optional)
Without a calculator, show that 1.001^1000 > 2.7.

**Answer.** Every term of the binomial expansion is positive, and the first five terms already give 1 + 1 + 0.4995 + 0.166167 + 0.041417 ≈ 2.7071 > 2.7.

---

## Q16 · Additive functions

**Topic:** Functional equations

**Statement.** Find all functions f: ℚ → ℚ satisfying given equations for all rational x and y.

### Part (a)
If f(x + y) = f(x) + f(y) for all rationals x, y, show that f(0) = 0 and f(−x) = −f(x).

**Hints**
1. *Nudge:* Substitute special values.
2. *Direction:* Try x = y = 0, then y = −x.
3. *Step:* x = y = 0 gives f(0) = 2f(0).

**Model answer.** x = y = 0 gives f(0) = 2f(0), so f(0) = 0. Then y = −x gives 0 = f(0) = f(x) + f(−x).

### Part (b)
With the same equation, show that f(x) = cx for every rational x, where c = f(1).

**Hints**
1. *Nudge:* What are f(2) and f(3)?
2. *Direction:* Show f(nx) = nf(x) for positive integers n by induction, then deal with 1/q.
3. *Step:* q × f(p/q) = f(p) = p × f(1).

**Model answer.** Induction gives f(nx) = nf(x) for n ∈ ℕ, and with (a) this also holds for negative n. So f(n) = cn, and for q > 0, q f(p/q) = f(q × p/q) = f(p) = cp, so f(p/q) = c × p/q. Conversely, f(x) = cx satisfies the equation for every rational c.

### Part (c)
Find all f: ℚ → ℚ with f(x + y) = f(x) + f(y) + xy for all rationals x, y.

**Hints**
1. *Nudge:* Find one solution first. Try a quadratic.
2. *Direction:* f(x) = x²/2 works. Look at g(x) = f(x) − x²/2.
3. *Step:* Show that g satisfies the equation in (b).

**Model answer.** g(x + y) = f(x) + f(y) + xy − (x + y)²/2 = g(x) + g(y). So g(x) = cx by (b), and f(x) = x²/2 + cx for some rational c. All of these work.

### Follow-up (optional)
If f(x + y) = f(x) + f(y) + 2xy for all rationals and f(1) = 3, find f(10).

**Answer.** As in (c), f(x) = x² + cx, and f(1) = 3 gives c = 2. So f(x) = x² + 2x and f(10) = 120.

---

## Q17 · Solving functional equations by substitution

**Topic:** Functional equations

**Statement.** Each equation holds for all x in the stated domain. Find f.

### Part (a)
f(x) + 2f(1 − x) = x² for all real x.

**Hints**
1. *Nudge:* What equation do you get if you replace x by 1 − x?
2. *Direction:* You now have two linear equations in the two "unknowns" f(x) and f(1 − x).
3. *Step:* The new equation is 2f(x) + f(1 − x) = (1 − x)². Eliminate f(1 − x).

**Model answer.** Doubling the second equation and subtracting the first gives 3f(x) = 2(1 − x)² − x², so f(x) = (x² − 4x + 2)/3. This does satisfy the original equation.

### Part (b)
f(x) + 2f(1/x) = 3x for all x ≠ 0. Find f, and all x with f(x) = f(−x).

**Hints**
1. *Nudge:* Which substitution swaps x and 1/x?
2. *Direction:* Replacing x by 1/x gives f(1/x) + 2f(x) = 3/x.
3. *Step:* Eliminate f(1/x) as in (a).

**Model answer.** Doubling the new equation and subtracting the original gives 3f(x) = 6/x − 3x, so f(x) = 2/x − x. Then f(x) = f(−x) ⇔ 2/x − x = −2/x + x ⇔ x² = 2 ⇔ x = ±√2.

### Part (c)
f(x) + f((x − 1)/x) = 1 + x for all x ≠ 0, 1.

**Hints**
1. *Nudge:* Let g(x) = (x − 1)/x. Compute g(g(x)) and g(g(g(x))).
2. *Direction:* g(g(x)) = 1/(1 − x) and g(g(g(x))) = x. So also substitute g(x) and g(g(x)) for x.
3. *Step:* You get three equations in f(x), f(g(x)), f(g(g(x))). Add the first and third, and subtract the second.

**Model answer.** With A = f(x), B = f(g(x)) and C = f(g(g(x))): A + B = 1 + x, B + C = 1 + (x − 1)/x and C + A = 1 + 1/(1 − x). Then 2A = (1 + x) − (1 + (x − 1)/x) + (1 + 1/(1 − x)), which simplifies to f(x) = ½(x + 1/x + 1/(1 − x)).

### Follow-up (optional)
Find all f: ℝ → ℝ with f(x) + x f(−x) = x + 1 for all real x.

**Answer.** f(x) = 1 for all x. Replacing x by −x gives f(−x) − x f(x) = 1 − x. Multiply this by x and subtract it from the original equation: (1 + x²)f(x) = 1 + x².

---

## Q18 · A function that triples when applied twice

**Topic:** Functional equations

**Statement.** f: ℕ → ℕ is strictly increasing, and f(f(n)) = 3n for every positive integer n.

### Part (a)
Show that f(1) = 2, and find f(2).

**Hints**
1. *Nudge:* Could f(1) = 1?
2. *Direction:* If f(1) = 1 then f(f(1)) = 1 ≠ 3. If f(1) = k ≥ 3, look at f(k) and use the fact that f is strictly increasing.
3. *Step:* f(1) = k gives f(k) = 3. But f(k) ≥ f(1) = k ≥ 3, with equality only if k = 1.

**Model answer.** f(1) ≠ 1 because f(f(1)) = 3. If f(1) = k ≥ 3 then f(k) = 3, but k > 1 forces f(k) > f(1) = k ≥ 3, a contradiction. So f(1) = 2, and f(2) = f(f(1)) = 3.

### Part (b)
Show that f(3n) = 3f(n), and find f(n) for n = 3, …, 9.

**Hints**
1. *Nudge:* Apply f to both sides of f(f(n)) = 3n.
2. *Direction:* f(f(f(n))) = f(3n), but also f(f(f(n))) = 3f(n), by applying the equation to f(n).
3. *Step:* f(3) = 3f(1) = 6 and f(6) = 3f(2) = 9. What does strict increase force for f(4) and f(5)?

**Model answer.** f(3n) = f(f(f(n))) = 3f(n). So f(3) = 6, f(6) = 9 and f(9) = 18. f(4) and f(5) are integers strictly between 6 and 9, so f(4) = 7 and f(5) = 8. Then f(7) = f(f(4)) = 12 and f(8) = f(f(5)) = 15. For n = 3, …, 9 the values are 6, 7, 8, 9, 12, 15, 18.

### Part (c)
Find f(100).

**Hints**
1. *Nudge:* Find f(3^k) and f(2 × 3^k).
2. *Direction:* f(3^k) = 2 × 3^k and f(2 × 3^k) = 3^{k+1}. Between 3^k and 2 × 3^k the arguments go up by 3^k. By how much do the values go up?
3. *Step:* The values also go up by exactly 3^k, and a strictly increasing function on the integers goes up by at least 1 each step, so it must go up by exactly 1 each step.

**Model answer.** By (b) and induction, f(3^k) = 2 × 3^k and f(2 × 3^k) = 3^{k+1}. Strict increase over an interval of 3^k steps whose values also rise by 3^k forces f(3^k + j) = 2 × 3^k + j for 0 ≤ j ≤ 3^k. With k = 4, f(100) = f(81 + 19) = 162 + 19 = 181. (Similarly f(2 × 3^k + j) = 3^{k+1} + 3j.)

### Follow-up (optional)
For which n is f(n) = 2n?

**Answer.** Exactly when n is a power of 3. On [3^k, 2 × 3^k], f(3^k + j) = 2 × 3^k + j equals 2(3^k + j) only when j = 0. On [2 × 3^k, 3^{k+1}], f(n) = 3n − 3^{k+1} equals 2n only when n = 3^{k+1}.

---

## Q19 · Tangents to a parabola

**Topic:** Coordinate geometry

**Statement.** Points P(p, p²) and Q(q, q²) lie on the parabola y = x², with p ≠ q.

### Part (a)
Find the equation of the tangent at P, and show that the tangents at P and Q meet at R((p + q)/2, pq).

**Hints**
1. *Nudge:* What is the gradient of y = x² at x = p?
2. *Direction:* The tangent at P is y = 2px − p², and similarly at Q.
3. *Step:* Subtract the two tangent equations to find x.

**Model answer.** Tangent at P: y − p² = 2p(x − p), i.e. y = 2px − p². Setting this equal to y = 2qx − q² gives 2(p − q)x = p² − q², so x = (p + q)/2 and y = p(p + q) − p² = pq.

### Part (b)
Show that the tangents at P and Q are perpendicular if and only if pq = −1/4, and that in this case R lies on the line y = −1/4.

**Hints**
1. *Nudge:* The gradients are 2p and 2q.
2. *Direction:* Two lines are perpendicular when the product of their gradients is −1.
3. *Step:* 4pq = −1, and the y-coordinate of R is pq.

**Model answer.** Perpendicular ⇔ (2p)(2q) = −1 ⇔ pq = −1/4, and then R = ((p + q)/2, −1/4). So perpendicular tangents always meet on the directrix y = −1/4. (The focus is (0, 1/4).)

### Part (c)
Show that triangle PQR has area |p − q|³/4, and that the region between the chord PQ and the parabola has area |p − q|³/6.

**Hints**
1. *Nudge:* For the triangle, use the vectors PQ and PR (half the absolute value of the 2 × 2 determinant), or the shoelace formula.
2. *Direction:* For the region, integrate (chord − parabola) from p to q. The chord is y = (p + q)x − pq.
3. *Step:* (p + q)x − pq − x² = −(x − p)(x − q).

**Model answer.** PQ = (q − p)(1, p + q) and PR = (q − p)(½, p). Area = ½|q − p|² × |p − (p + q)/2| = |q − p|³/4. For the region (taking p < q), ∫_p^q −(x − p)(x − q) dx = (q − p)³/6. So the parabolic segment is exactly 2/3 of triangle PQR.

### Follow-up (optional)
If the chord PQ passes through the focus (0, 1/4), show that R lies on y = −1/4.

**Answer.** The chord y = (p + q)x − pq passes through (0, 1/4) if and only if pq = −1/4, and R has y-coordinate pq. So focal chords correspond exactly to pairs of perpendicular tangents.

---

## Q20 · Apollonius circles and common tangents

**Topic:** Coordinate geometry

**Statement.** Let O = (0, 0) and B = (3, 0).

### Part (a)
Find the locus of points P with OP = 2 × PB.

**Hints**
1. *Nudge:* Square both sides to get rid of square roots.
2. *Direction:* x² + y² = 4((x − 3)² + y²).
3. *Step:* Collect terms and complete the square.

**Model answer.** 3x² − 24x + 3y² + 36 = 0, i.e. x² − 8x + y² + 12 = 0, i.e. (x − 4)² + y² = 4. This is the circle with centre (4, 0) and radius 2.

### Part (b)
Find the equations of the two tangents from O to this circle, and the angle between them.

**Hints**
1. *Nudge:* Draw the radius to a point of tangency. What angle does it make with the tangent?
2. *Direction:* You get a right-angled triangle with hypotenuse 4 (O to the centre) and the radius 2 opposite the angle at O.
3. *Step:* Half the angle between the tangents is arcsin(2/4).

**Model answer.** The half-angle is arcsin(½) = 30°, so the tangents are y = ±x/√3 and the angle between them is 60°. (Check: the distance from (4, 0) to x − √3y = 0 is 4/2 = 2.)

### Part (c)
Find the equations of all the common tangents to the circles x² + y² = 1 and (x − 4)² + y² = 4.

**Hints**
1. *Nudge:* How many common tangents should there be? Compare the distance between the centres with the radii.
2. *Direction:* The line y = mx + c is tangent to a circle if and only if its distance from the centre equals the radius: |c|/√(1 + m²) = 1 and |4m + c|/√(1 + m²) = 2.
3. *Step:* Dividing, |4m + c| = 2|c|. Treat 4m + c = 2c and 4m + c = −2c separately.

**Model answer.** The centres are 4 apart and 4 > 1 + 2, so there are four common tangents. If 4m + c = 2c, then c = 4m and 16m² = 1 + m², so m = ±1/√15, giving y = ±(x + 4)/√15 (the external tangents, which meet at (−4, 0)). If 4m + c = −2c, then c = −4m/3 and 16m²/9 = 1 + m², so m = ±3/√7, giving y = ±(3x − 4)/√7 (the internal tangents, which cross at (4/3, 0)). No vertical line is tangent to both circles.

### Follow-up (optional)
For k > 0 with k ≠ 1, show that the locus OP = k × PB is a circle, and find its centre and radius.

**Answer.** Centre (3k²/(k² − 1), 0) and radius 3k/|k² − 1|. When k = 1 the locus is the line x = 3/2.

---

## Q21 · The reachable region of a projectile

**Topic:** Mechanics

**Statement.** A particle is projected from the origin with speed u at angle θ above the horizontal. Gravity g is constant and there is no air resistance.

### Part (a)
Find the range on horizontal ground, and the angle that maximises it.

**Hints**
1. *Nudge:* Find the time of flight from the vertical motion.
2. *Direction:* y = ut sin θ − ½gt² = 0 at t = 2u sin θ/g.
3. *Step:* Range = u cos θ × t. Then use 2 sin θ cos θ = sin 2θ.

**Model answer.** The range is u² sin 2θ/g, which is greatest at θ = 45°, with value u²/g.

### Part (b)
Show that the point (X, Y) with X > 0 can be hit, for some θ, if and only if Y ≤ u²/(2g) − gX²/(2u²).

**Hints**
1. *Nudge:* Write the trajectory as y in terms of x.
2. *Direction:* y = x tan θ − gx²(1 + tan²θ)/(2u²), a quadratic in T = tan θ.
3. *Step:* (X, Y) can be hit if and only if this quadratic in T has a real root, i.e. its discriminant is ≥ 0.

**Model answer.** The quadratic gX²T²/(2u²) − XT + (Y + gX²/(2u²)) = 0 has a real root if and only if X² ≥ 4 × (gX²/(2u²)) × (Y + gX²/(2u²)), which rearranges to Y ≤ u²/(2g) − gX²/(2u²). The boundary parabola is the envelope of all the trajectories.

### Part (c)
Hence find the maximum range up a plane inclined at angle α to the horizontal, projecting from a point on the plane.

**Hints**
1. *Nudge:* A point at distance R up the slope is (R cos α, R sin α).
2. *Direction:* The maximum R is where the slope meets the boundary parabola from (b).
3. *Step:* Solve R sin α = u²/(2g) − gR² cos²α/(2u²) for R > 0.

**Model answer.** Multiplying by 2u²/g gives cos²α R² + (2u²/g) sin α R − u⁴/g² = 0. Using 1 − sin²α = cos²α, the positive root is R = (u²/g)(1 − sin α)/cos²α = u²/(g(1 + sin α)). For α = 0 this gives u²/g, as in (a).

### Follow-up (optional)
What is the maximum range down the same slope, and at what angle should you aim?

**Answer.** u²/(g(1 − sin α)), by replacing α with −α. The best direction bisects the angle between the upward vertical and the slope: θ = 45° − α/2 above the horizontal when firing down the slope, and θ = 45° + α/2 when firing up it.

---

## Q22 · A bouncing ball

**Topic:** Mechanics

**Statement.** A ball is dropped from rest at height h onto a horizontal floor. The coefficient of restitution is e (0 < e < 1), so each bounce multiplies the speed by e. Ignore air resistance.

### Part (a)
Show that the ball rises to height e²h after the first bounce.

**Hints**
1. *Nudge:* How fast is the ball moving when it hits the floor? Use v² = u² + 2as.
2. *Direction:* It hits the floor at √(2gh) and leaves at e√(2gh).
3. *Step:* A ball launched upwards at speed V rises to V²/(2g).

**Model answer.** The impact speed is √(2gh), the rebound speed is e√(2gh), and the height reached is e² × 2gh/(2g) = e²h.

### Part (b)
Find the total distance travelled before the ball comes to rest. Evaluate it for h = 1.25 m and e = ½.

**Hints**
1. *Nudge:* After the first drop, each bounce goes up and comes down the same height.
2. *Direction:* Distance = h + 2(e²h + e⁴h + …).
3. *Step:* Sum the geometric series with ratio e².

**Model answer.** Distance = h + 2e²h/(1 − e²) = h(1 + e²)/(1 − e²). For h = 1.25 and e = ½ this is 1.25 × (5/4)/(3/4) = 25/12 ≈ 2.08 m.

### Part (c)
Show that the ball comes to rest after a finite time, and find that time. Evaluate it for h = 1.25 m, e = ½ and g = 10 m s⁻².

**Hints**
1. *Nudge:* There are infinitely many bounces, but how long does each one take?
2. *Direction:* The first drop takes t_0 = √(2h/g). A bounce with launch speed V lasts 2V/g.
3. *Step:* The k-th bounce has launch speed e^k √(2gh), so it lasts 2e^k t_0.

**Model answer.** Total time = t_0 + 2t_0(e + e² + …) = t_0(1 + 2e/(1 − e)) = √(2h/g) × (1 + e)/(1 − e). This is finite. For the given numbers it is 0.5 × 3 = 1.5 s.

### Follow-up (optional)
For these numbers, what is the average speed over the whole motion?

**Answer.** (25/12)/1.5 = 25/18 ≈ 1.39 m s⁻¹.

---

## Q23 · When does the ladder slip?

**Topic:** Mechanics

**Statement.** A uniform ladder of length L and weight W stands with its foot on rough horizontal ground (coefficient of friction μ) and its top against a vertical wall. It makes angle θ with the horizontal.

### Part (a)
If the wall is smooth, show that the ladder can rest in equilibrium if and only if tan θ ≥ 1/(2μ).

**Hints**
1. *Nudge:* List the forces: the weight, the normal reaction R and friction F at the foot, and the normal reaction S at the wall.
2. *Direction:* Resolve vertically and horizontally, then take moments about the foot.
3. *Step:* Moments about the foot: S × L sin θ = W × (L/2) cos θ.

**Model answer.** R = W and F = S = W/(2 tan θ). There is no slipping if and only if F ≤ μR, i.e. W/(2 tan θ) ≤ μW, i.e. tan θ ≥ 1/(2μ).

### Part (b)
With a smooth wall, μ = ½ and tan θ = 4/3, a person of weight W climbs the ladder. How far up can they go?

**Hints**
1. *Nudge:* Which forces change when the person is at distance d up the ladder?
2. *Direction:* Now R = 2W. Take moments about the foot again, including the person's weight.
3. *Step:* S × L sin θ = W(L/2) cos θ + Wd cos θ, and we need S ≤ μR = W.

**Model answer.** S = W(L/2 + d)/(L tan θ) = 3W(L/2 + d)/(4L). S ≤ W gives L/2 + d ≤ 4L/3, i.e. d ≤ 5L/6. They can climb five-sixths of the way up.

### Part (c)
Now suppose the wall is also rough, with coefficient of friction μ'. Show that the least angle for equilibrium satisfies tan θ = (1 − μμ')/(2μ).

**Hints**
1. *Nudge:* At the point of slipping, which way does each friction force act, and how big is it?
2. *Direction:* In limiting equilibrium, F = μR at the floor (towards the wall) and G = μ'S at the wall (upwards).
3. *Step:* R + μ'S = W, μR = S, and moments about the foot give S L sin θ + μ'S L cos θ = W(L/2) cos θ.

**Model answer.** The first two equations give S = μW/(1 + μμ'). The moment equation is S(tan θ + μ') = W/2, so μ(tan θ + μ') = (1 + μμ')/2, giving tan θ = (1 − μμ')/(2μ). For example, μ = ½ and μ' = ⅓ give tan θ = 5/6, θ ≈ 39.8°.

### Follow-up (optional)
What happens if μμ' ≥ 1?

**Answer.** The formula gives tan θ ≤ 0, so the ladder can rest at any angle, however shallow: friction alone can hold it up.

---

## Q24 · Fifth roots of unity

**Topic:** Complex numbers

**Statement.** Let ω = e^{2πi/5} = cos(2π/5) + i sin(2π/5).

### Part (a)
Show that 1 + ω + ω² + ω³ + ω⁴ = 0.

**Hints**
1. *Nudge:* What is ω⁵?
2. *Direction:* It is a geometric series. Alternatively, factorise z⁵ − 1.
3. *Step:* z⁵ − 1 = (z − 1)(z⁴ + z³ + z² + z + 1), and ω ≠ 1.

**Model answer.** ω⁵ = 1 and ω ≠ 1, so 0 = ω⁵ − 1 = (ω − 1)(1 + ω + ω² + ω³ + ω⁴), and the second factor must be 0.

### Part (b)
Deduce that cos(2π/5) = (√5 − 1)/4.

**Hints**
1. *Nudge:* Take real parts in (a).
2. *Direction:* ω⁴ is the conjugate of ω and ω³ is the conjugate of ω², so 1 + 2cos(2π/5) + 2cos(4π/5) = 0.
3. *Step:* Put c = cos(2π/5). Then cos(4π/5) = 2c² − 1.

**Model answer.** 1 + 2c + 2(2c² − 1) = 0 gives 4c² + 2c − 1 = 0, so c = (−1 ± √5)/4. Since 0 < 2π/5 < π/2, c > 0, so cos(2π/5) = (√5 − 1)/4 ≈ 0.309.

### Part (c)
Show that (1 − ω)(1 − ω²)(1 − ω³)(1 − ω⁴) = 5, and deduce that sin(π/5) sin(2π/5) sin(3π/5) sin(4π/5) = 5/16.

**Hints**
1. *Nudge:* ω, ω², ω³ and ω⁴ are the roots of z⁴ + z³ + z² + z + 1.
2. *Direction:* So z⁴ + z³ + z² + z + 1 = (z − ω)(z − ω²)(z − ω³)(z − ω⁴). Put z = 1.
3. *Step:* |1 − e^{iφ}| = 2 sin(φ/2) for 0 < φ < 2π.

**Model answer.** Setting z = 1 shows that the product is 1 + 1 + 1 + 1 + 1 = 5. Taking moduli, and using |1 − e^{iφ}| = |e^{−iφ/2} − e^{iφ/2}| = 2 sin(φ/2), gives 2⁴ × sin(π/5) sin(2π/5) sin(3π/5) sin(4π/5) = 5. So the product of the sines is 5/16.

### Follow-up (optional)
Generalise (c) to n-th roots of unity.

**Answer.** Π_{k=1}^{n−1} sin(kπ/n) = n/2^{n−1}, because Π_{k=1}^{n−1} (1 − ω^k) = 1 + 1 + … + 1 = n.

---

## Q25 · Equilateral triangles in the complex plane

**Topic:** Complex numbers

**Statement.** Points in the plane are represented by complex numbers.

### Part (a)
Explain why z_1, z_2, z_3 form an equilateral triangle, labelled anticlockwise, if and only if z_3 − z_1 = e^{iπ/3}(z_2 − z_1).

**Hints**
1. *Nudge:* What does multiplying by e^{iπ/3} do geometrically?
2. *Direction:* It rotates by 60° about the origin and keeps lengths.
3. *Step:* z_2 − z_1 represents the vector from z_1 to z_2.

**Model answer.** The triangle is equilateral and anticlockwise if and only if the vector from z_1 to z_3 is the vector from z_1 to z_2 rotated by +60°, with the same length. That says exactly z_3 − z_1 = e^{iπ/3}(z_2 − z_1).

### Part (b)
Find all z such that 0, 1 + i and z are the vertices of an equilateral triangle.

**Hints**
1. *Nudge:* There are two such triangles, one on each side of the segment.
2. *Direction:* z = e^{±iπ/3}(1 + i).
3. *Step:* e^{iπ/3} = ½ + (√3/2)i.

**Model answer.** z = (1 + i)(½ ± (√3/2)i), i.e. z = (1 − √3)/2 + i(1 + √3)/2 or z = (1 + √3)/2 + i(1 − √3)/2.

### Part (c)
Show that z_1, z_2, z_3 form an equilateral triangle, in either orientation, if and only if z_1² + z_2² + z_3² = z_1z_2 + z_2z_3 + z_3z_1.

**Hints**
1. *Nudge:* Rewrite (a) using ω = e^{2πi/3}, which satisfies 1 + ω + ω² = 0 (note e^{iπ/3} = −ω²).
2. *Direction:* Anticlockwise equilateral ⇔ z_1 + ωz_2 + ω²z_3 = 0. Clockwise equilateral ⇔ z_1 + ω²z_2 + ωz_3 = 0.
3. *Step:* Multiply out (z_1 + ωz_2 + ω²z_3)(z_1 + ω²z_2 + ωz_3) using ω³ = 1 and ω + ω² = −1.

**Model answer.** The product equals z_1² + z_2² + z_3² − z_1z_2 − z_2z_3 − z_3z_1. It is zero if and only if one of the factors is zero, i.e. if and only if the triangle is equilateral in one of the two orientations.

### Follow-up (optional)
The roots of z³ − 3z² + 3z − 9 = 0 form a triangle. Show that it is equilateral and find its area.

**Answer.** The equation is (z − 1)³ = 8, so z = 1 + 2, 1 + 2ω, 1 + 2ω². These form an equilateral triangle with circumradius 2 and side 2√3, so its area is 3√3.

---

## Q26 · Binomial sums and roots of unity

**Topic:** Complex numbers

**Statement.** Use complex numbers to evaluate trigonometric and binomial sums.

### Part (a)
For θ not a multiple of 2π, show that Σ_{k=1}^{n} cos(kθ) = sin(nθ/2) cos((n + 1)θ/2)/sin(θ/2).

**Hints**
1. *Nudge:* cos kθ = Re(e^{ikθ}).
2. *Direction:* Sum the geometric series Σ e^{ikθ}.
3. *Step:* Factor e^{ix/2} out of e^{ix} − 1 to get e^{ix/2} × 2i sin(x/2).

**Model answer.** Σ_{k=1}^{n} e^{ikθ} = e^{iθ}(e^{inθ} − 1)/(e^{iθ} − 1) = e^{i(n+1)θ/2} sin(nθ/2)/sin(θ/2). Taking real parts gives the result.

### Part (b)
Show that Σ_{k=0}^{n} C(n, k) cos(kθ) = 2^n cos^n(θ/2) cos(nθ/2).

**Hints**
1. *Nudge:* Again write cos kθ as a real part. What is Σ C(n, k) z^k?
2. *Direction:* The sum is Re (1 + e^{iθ})^n.
3. *Step:* 1 + e^{iθ} = e^{iθ/2}(e^{−iθ/2} + e^{iθ/2}) = 2cos(θ/2) e^{iθ/2}.

**Model answer.** Re (1 + e^{iθ})^n = Re(2^n cos^n(θ/2) e^{inθ/2}) = 2^n cos^n(θ/2) cos(nθ/2).

### Part (c)
Let ω = e^{2πi/3}. By considering (1 + 1)^n + (1 + ω)^n + (1 + ω²)^n, show that C(n, 0) + C(n, 3) + C(n, 6) + … = (2^n + 2cos(nπ/3))/3. Evaluate this for n = 10.

**Hints**
1. *Nudge:* What is 1 + ω^k + ω^{2k} when 3 divides k, and when it does not?
2. *Direction:* Expanding, the sum is Σ_k C(n, k)(1 + ω^k + ω^{2k}) = 3 Σ_{3|k} C(n, k).
3. *Step:* 1 + ω = −ω² = e^{iπ/3} and 1 + ω² = e^{−iπ/3}.

**Model answer.** 1 + ω^k + ω^{2k} is 3 if 3 divides k and 0 otherwise. So 3 Σ_{3|k} C(n, k) = 2^n + e^{inπ/3} + e^{−inπ/3} = 2^n + 2cos(nπ/3). For n = 10: (1024 + 2cos(10π/3))/3 = (1024 − 1)/3 = 341 (= 1 + 120 + 210 + 10).

### Follow-up (optional)
Find C(10, 0) + C(10, 4) + C(10, 8) using fourth roots of unity.

**Answer.** ¼(2^10 + (1 + i)^10 + 0^10 + (1 − i)^10) = ¼(1024 + 32i − 32i) = 256.

---

## Q27 · Logistic growth with harvesting

**Topic:** Differential equations

**Statement.** A population, in suitable units, satisfies dP/dt = P(1 − P) − h, where h ≥ 0 is a constant harvesting rate.

### Part (a)
With h = 0 and P(0) = 1/4, solve for P(t), and find when P = 1/2.

**Hints**
1. *Nudge:* Separate the variables.
2. *Direction:* Use partial fractions: 1/(P(1 − P)) = 1/P + 1/(1 − P).
3. *Step:* ln(P/(1 − P)) = t + C.

**Model answer.** P/(1 − P) = (1/3)e^t, so P = 1/(1 + 3e^{−t}). P = ½ when e^t = 3, i.e. at t = ln 3 ≈ 1.10.

### Part (b)
For which h does the equation have an equilibrium (constant) solution? For h = 3/16, find the equilibria and decide which is stable.

**Hints**
1. *Nudge:* Equilibria are the values of P where dP/dt = 0.
2. *Direction:* P² − P + h = 0 needs a non-negative discriminant.
3. *Step:* Sketch dP/dt against P (a downward parabola) to see which way P moves.

**Model answer.** The discriminant is 1 − 4h, so there is an equilibrium if and only if h ≤ 1/4. For h = 3/16 the equilibria are P = 1/4 and P = 3/4. dP/dt = −(P − ¼)(P − ¾) is positive between them and negative outside, so 3/4 is stable and 1/4 is unstable.

### Part (c)
With h = 3/16 and P(0) = 1/8, show that the population dies out, and find the time at which P = 0.

**Hints**
1. *Nudge:* P(0) is below the unstable equilibrium. Which way does P move?
2. *Direction:* Separate: ∫ dP/((P − ¼)(P − ¾)) = −∫ dt.
3. *Step:* 1/((P − ¼)(P − ¾)) = 2/(P − ¾) − 2/(P − ¼).

**Model answer.** For 0 ≤ P ≤ 1/8, dP/dt ≤ (1/8)(7/8) − 3/16 = −5/64 < 0, so P falls at a rate of at least 5/64 and reaches 0 in finite time. Integrating, 2 ln|(P − ¾)/(P − ¼)| = −t + C. At t = 0, (P − ¾)/(P − ¼) = 5, so C = 2 ln 5. At P = 0 the ratio is 3, so 2 ln 3 = −t + 2 ln 5, giving t = 2 ln(5/3) ≈ 1.02.

### Follow-up (optional)
With h = 3/16 and P(0) = 1/2, find P(t) and its limit.

**Answer.** Here C = 0 and (¾ − P)/(P − ¼) = e^{−t/2}, so P = (3 + e^{−t/2})/(4(1 + e^{−t/2})), which tends to 3/4.

---

## Q28 · Curves defined by their tangents

**Topic:** Differential equations

**Statement.** Find all curves y = f(x), with x > 0, that have the given geometric property, by turning the property into a differential equation.

### Part (a)
The tangent at every point P(x, y) meets the x-axis at the point with x-coordinate x/2.

**Hints**
1. *Nudge:* Write down the tangent at P and find where y = 0.
2. *Direction:* The tangent meets the x-axis at x − y/y'.
3. *Step:* x − y/y' = x/2 gives dy/dx = 2y/x.

**Model answer.** Separating, ∫ dy/y = ∫ 2 dx/x, so ln|y| = 2 ln x + c, so y = Ax²: parabolas with vertex at the origin.

### Part (b)
The normal at every point passes through the origin.

**Hints**
1. *Nudge:* If the normal at P passes through O, then the line OP is the normal.
2. *Direction:* The gradient of OP is y/x, and the gradient of the tangent is y'.
3. *Step:* (y/x) × y' = −1.

**Model answer.** y dy/dx = −x, so y² = −x² + C, i.e. x² + y² = C: circles centred at O. (Geometrically clear: a radius is perpendicular to the tangent.)

### Part (c)
The tangent at P meets the y-axis at height equal to OP, i.e. at the point (0, √(x² + y²)).

**Hints**
1. *Nudge:* Where does the tangent at P meet the y-axis?
2. *Direction:* The intercept is y − x y'. Set it equal to √(x² + y²) and substitute y = vx.
3. *Step:* You get −x dv/dx = √(1 + v²). You may use d/dv [ln(v + √(1 + v²))] = 1/√(1 + v²).

**Model answer.** ln(v + √(1 + v²)) = −ln x + c, so v + √(1 + v²) = A/x with A > 0. Isolate the square root and square: 1 + v² = A²/x² − 2Av/x + v², so v = (A² − x²)/(2Ax), i.e. y = A/2 − x²/(2A). These are parabolas with focus at the origin: the reflective property in disguise.

### Follow-up (optional)
Find the curve through (1, 1) for which the area under the curve from 0 to x is one third of the rectangle with opposite corners O and P, i.e. ∫₀^x f(t) dt = x f(x)/3.

**Answer.** Differentiating gives f = (f + x f')/3, i.e. x f' = 2f, so f = Cx². Through (1, 1), the curve is y = x².

---

## Q29 · Symmetric functions of roots

**Topic:** Polynomials

**Statement.** α, β, γ are the roots of x³ − 2x² + 3x − 4 = 0.

### Part (a)
Find α + β + γ, αβ + βγ + γα, αβγ and α² + β² + γ². What can you deduce about the roots?

**Hints**
1. *Nudge:* Expand (x − α)(x − β)(x − γ) and compare coefficients.
2. *Direction:* α² + β² + γ² = (α + β + γ)² − 2(αβ + βγ + γα).
3. *Step:* Can real numbers have a negative sum of squares?

**Model answer.** α + β + γ = 2, αβ + βγ + γα = 3 and αβγ = 4. Then α² + β² + γ² = 4 − 6 = −2 < 0, so the roots are not all real. A real cubic has at least one real root, so there is one real root and a pair of complex conjugate roots.

### Part (b)
Find α³ + β³ + γ³.

**Hints**
1. *Nudge:* Each root satisfies the equation.
2. *Direction:* α³ = 2α² − 3α + 4. Add the three such equations.
3. *Step:* Use the values from (a).

**Model answer.** α³ + β³ + γ³ = 2(α² + β² + γ²) − 3(α + β + γ) + 12 = −4 − 6 + 12 = 2.

### Part (c)
Find a cubic equation with roots αβ, βγ and γα.

**Hints**
1. *Nudge:* You need the sum, the sum of pairwise products and the product of the new roots.
2. *Direction:* αβ × βγ + βγ × γα + γα × αβ = αβγ(α + β + γ).
3. *Step:* (αβ)(βγ)(γα) = (αβγ)².

**Model answer.** The new roots have sum 3, pairwise-product sum 4 × 2 = 8 and product 16, so they are the roots of x³ − 3x² + 8x − 16 = 0.

### Follow-up (optional)
Find α⁴ + β⁴ + γ⁴.

**Answer.** Multiply the equation by α: α⁴ = 2α³ − 3α² + 4α. Summing over the roots gives 2 × 2 − 3 × (−2) + 4 × 2 = 18.

---

## Q30 · Remainders of a big power

**Topic:** Polynomials

**Statement.** Find the remainder when x^100 is divided by various quadratics, without doing long division.

### Part (a)
The remainder when x^100 is divided by x² − 1.

**Hints**
1. *Nudge:* What degree can the remainder have?
2. *Direction:* Write x^100 = (x² − 1)Q(x) + ax + b.
3. *Step:* Substitute x = 1 and x = −1.

**Model answer.** 1 = a + b and 1 = −a + b, so a = 0 and b = 1. The remainder is 1.

### Part (b)
The remainder when x^100 is divided by (x − 1)².

**Hints**
1. *Nudge:* Substituting x = 1 gives only one equation. Where can a second one come from?
2. *Direction:* Differentiate x^100 = (x − 1)²Q(x) + ax + b.
3. *Step:* The derivative of (x − 1)²Q(x) is also zero at x = 1.

**Model answer.** x = 1 gives a + b = 1. Differentiating and setting x = 1 gives 100 = a. So b = −99 and the remainder is 100x − 99.

### Part (c)
The remainder when x^100 is divided by x² + x + 1.

**Hints**
1. *Nudge:* What are the roots of x² + x + 1?
2. *Direction:* The roots are ω and ω², where ω = e^{2πi/3} and ω³ = 1.
3. *Step:* ω^100 = ω^99 × ω = ω.

**Model answer.** aω + b = ω and aω² + b = ω². Subtracting, a(ω − ω²) = ω − ω², so a = 1 and then b = 0. The remainder is x.

### Follow-up (optional)
Find the remainder when x^2026 is divided by x³ − x.

**Answer.** x². Write the remainder as ax² + bx + c and substitute x = 0, 1, −1: c = 0, a + b = 1 and a − b = 1.

---

## Q31 · Integer polynomials

**Topic:** Polynomials

**Statement.** P(x) is a polynomial with integer coefficients.

### Part (a)
Show that a − b divides P(a) − P(b) for all integers a ≠ b.

**Hints**
1. *Nudge:* Start with P(x) = x^n.
2. *Direction:* a^n − b^n = (a − b)(a^{n−1} + a^{n−2}b + … + b^{n−1}).
3. *Step:* If P(x) = Σ c_k x^k, then P(a) − P(b) = Σ c_k(a^k − b^k).

**Model answer.** Each a^k − b^k is divisible by a − b, by the factorisation above. So the integer combination Σ c_k(a^k − b^k) = P(a) − P(b) is divisible by a − b too.

### Part (b)
Is there such a P with P(2) = 5 and P(7) = 13?

**Hints**
1. *Nudge:* Apply (a).
2. *Direction:* 7 − 2 must divide 13 − 5.
3. *Step:* Does 5 divide 8?

**Model answer.** No. By (a), 7 − 2 = 5 would have to divide 13 − 5 = 8, and it does not.

### Part (c)
Suppose P(0) and P(1) are both odd. Show that P has no integer roots.

**Hints**
1. *Nudge:* Consider P(n) for even n and for odd n separately.
2. *Direction:* By (a), n − 0 divides P(n) − P(0), and n − 1 divides P(n) − P(1).
3. *Step:* If n is even, 2 divides n, so P(n) ≡ P(0) (mod 2). If n is odd, 2 divides n − 1.

**Model answer.** For even n, P(n) ≡ P(0) ≡ 1 (mod 2). For odd n, P(n) ≡ P(1) ≡ 1 (mod 2). So P(n) is always odd, and in particular never 0.

### Follow-up (optional)
Suppose P(a) = P(b) = P(c) = P(d) = 5 for four distinct integers a, b, c, d. Show that P(k) ≠ 8 for every integer k.

**Answer.** P(x) − 5 = (x − a)(x − b)(x − c)(x − d)Q(x), where Q has integer coefficients because we divided by monic integer polynomials. If P(k) = 8, then 3 is the product of the four distinct integers k − a, …, k − d and the integer Q(k). Each of the four divides 3, so they must be 1, −1, 3, −3, whose product is 9, and 9 does not divide 3.

---

## Q32 · Induction warm-ups and the stamp problem

**Topic:** Induction

**Statement.** Practise three styles of induction.

### Part (a)
Prove that 9^n + 7 is divisible by 8 for all n ≥ 0.

**Hints**
1. *Nudge:* Check n = 0 and n = 1.
2. *Direction:* Express 9^{n+1} + 7 in terms of 9^n + 7.
3. *Step:* 9^{n+1} + 7 = 9(9^n + 7) − 56.

**Model answer.** For n = 0 the value is 8. If 8 divides 9^n + 7, then 9^{n+1} + 7 = 9(9^n + 7) − 56 is divisible by 8, since 56 = 7 × 8.

### Part (b)
Prove that 2^n > n² for all n ≥ 5.

**Hints**
1. *Nudge:* Check n = 2, 3, 4 and 5. Why does the statement start at 5?
2. *Direction:* Assume 2^n > n². Then 2^{n+1} > 2n², so you need 2n² ≥ (n + 1)².
3. *Step:* 2n² − (n + 1)² = n² − 2n − 1 = (n − 1)² − 2, which is positive for n ≥ 3.

**Model answer.** Base case n = 5: 32 > 25. Step: 2^{n+1} > 2n² ≥ (n + 1)², because (n − 1)² ≥ 2 for n ≥ 3. The statement fails at n = 2, 3, 4 (4 = 4, 8 < 9, 16 = 16).

### Part (c)
Stamps cost 4p and 5p. Prove that every amount of n pence with n ≥ 12 can be made exactly, and that 11p cannot.

**Hints**
1. *Nudge:* Check 12, 13, 14 and 15 by hand.
2. *Direction:* If you can make n, you can make n + 4.
3. *Step:* So the four base cases 12 to 15 cover everything (strong induction with steps of 4).

**Model answer.** 12 = 4+4+4, 13 = 4+4+5, 14 = 4+5+5 and 15 = 5+5+5. Every n ≥ 16 follows from n − 4 by adding a 4p stamp. For 11p, using zero, one or two 5p stamps leaves 11, 6 or 1, none of which is a multiple of 4.

### Follow-up (optional)
Which amounts cannot be made?

**Answer.** 1, 2, 3, 6, 7 and 11. That is six amounts. In general, for coprime a and b there are (a − 1)(b − 1)/2 such amounts, and the largest is ab − a − b.

---

## Q33 · Fibonacci identities

**Topic:** Induction

**Statement.** F_0 = 0, F_1 = 1 and F_{n+1} = F_n + F_{n−1}.

### Part (a)
Prove that F_1 + F_2 + … + F_n = F_{n+2} − 1.

**Hints**
1. *Nudge:* Check n = 1, 2, 3.
2. *Direction:* Add F_{n+1} to both sides of the case n.
3. *Step:* F_{n+2} − 1 + F_{n+1} = F_{n+3} − 1.

**Model answer.** For n = 1: F_1 = 1 = F_3 − 1. Step: F_1 + … + F_{n+1} = F_{n+2} − 1 + F_{n+1} = F_{n+3} − 1.

### Part (b)
Prove Cassini's identity, F_{n+1}F_{n−1} − F_n² = (−1)^n for n ≥ 1.

**Hints**
1. *Nudge:* Check n = 1, 2, 3.
2. *Direction:* In F_{n+2}F_n − F_{n+1}², replace F_{n+2} by F_{n+1} + F_n.
3. *Step:* F_{n+2}F_n − F_{n+1}² = F_{n+1}F_n + F_n² − F_{n+1}² = F_n² − F_{n+1}(F_{n+1} − F_n) = F_n² − F_{n+1}F_{n−1}.

**Model answer.** Base case n = 1: F_2F_0 − F_1² = 0 − 1 = −1. Step: F_{n+2}F_n − F_{n+1}² = −(F_{n+1}F_{n−1} − F_n²) = −(−1)^n = (−1)^{n+1}.

### Part (c)
Let φ = (1 + √5)/2. Prove that F_n ≤ φ^{n−1} for all n ≥ 1.

**Hints**
1. *Nudge:* What equation does φ satisfy?
2. *Direction:* φ² = φ + 1. Use strong induction, assuming the result for n and n − 1.
3. *Step:* F_{n+1} = F_n + F_{n−1} ≤ φ^{n−1} + φ^{n−2} = φ^{n−2}(φ + 1).

**Model answer.** Base cases: F_1 = 1 = φ⁰ and F_2 = 1 ≤ φ. Step: F_{n+1} ≤ φ^{n−2}(φ + 1) = φ^{n−2}φ² = φ^n. So the Fibonacci numbers grow at most geometrically, with ratio φ ≈ 1.618.

### Follow-up (optional)
Prove that F_{2n} = F_n(F_{n−1} + F_{n+1}).

**Answer.** First prove F_{m+n} = F_m F_{n+1} + F_{m−1} F_n by induction on n, then put m = n.

---

## Q34 · Sketching a rational function

**Topic:** Curve sketching

**Statement.** Let f(x) = (x² + 3)/(x − 1).

### Part (a)
Find the asymptotes of y = f(x).

**Hints**
1. *Nudge:* Where is f undefined?
2. *Direction:* Divide x² + 3 by x − 1.
3. *Step:* x² + 3 = (x − 1)(x + 1) + 4.

**Model answer.** f(x) = x + 1 + 4/(x − 1). So x = 1 is a vertical asymptote and y = x + 1 is an oblique asymptote. The curve lies above the oblique asymptote for x > 1 and below it for x < 1.

### Part (b)
Find the stationary points and their nature, and sketch the curve.

**Hints**
1. *Nudge:* Differentiating the form from (a) is easier.
2. *Direction:* f'(x) = 1 − 4/(x − 1)².
3. *Step:* f'(x) = 0 ⇔ (x − 1)² = 4.

**Model answer.** At x = 3, f = 6 (local minimum). At x = −1, f = −2 (local maximum). The left branch climbs from −∞ (below the asymptote) to the maximum (−1, −2), then falls to −∞ as x → 1 from below. The right branch comes down from +∞ to the minimum (3, 6), then rises alongside y = x + 1. The y-intercept is −3, and there are no x-intercepts.

### Part (c)
For which k does f(x) = k have two distinct real solutions? Confirm your answer algebraically.

**Hints**
1. *Nudge:* Use the sketch: draw horizontal lines y = k.
2. *Direction:* There are two solutions when the line is above the minimum or below the maximum.
3. *Step:* Algebraically, x² + 3 = k(x − 1) ⇔ x² − kx + (k + 3) = 0. Look at the discriminant.

**Model answer.** k < −2 or k > 6. The discriminant is k² − 4k − 12 = (k − 6)(k + 2), which is positive exactly when k < −2 or k > 6, and x = 1 is never a root because 1 + 3 ≠ 0. The range of f is (−∞, −2] ∪ [6, ∞).

### Follow-up (optional)
Sketch y² = f(x).

**Answer.** The curve exists only for x > 1, and it is symmetric in the x-axis. |y| = √f(x) ≥ √6, with closest approach to the axis at (3, ±√6). The line x = 1 is an asymptote, and y behaves like ±√x for large x.

---

## Q35 · Counting solutions with a sketch

**Topic:** Curve sketching

**Statement.** Let f(x) = x² e^{−x}.

### Part (a)
Find the stationary points and their nature.

**Hints**
1. *Nudge:* Use the product rule.
2. *Direction:* f'(x) = (2x − x²)e^{−x} = x(2 − x)e^{−x}.
3. *Step:* Look at the sign of x(2 − x).

**Model answer.** At x = 0 there is a minimum with f = 0. At x = 2 there is a maximum with f = 4/e² ≈ 0.541.

### Part (b)
Find the points of inflection, and describe the behaviour as x → ±∞. Sketch the curve.

**Hints**
1. *Nudge:* Differentiate again.
2. *Direction:* f''(x) = (x² − 4x + 2)e^{−x}.
3. *Step:* Which grows faster as x → ∞, x² or e^x?

**Model answer.** f'' = 0 at x = 2 ± √2 (≈ 0.59 and 3.41). f'' changes sign at both, so both are points of inflection. As x → ∞, f → 0 from above (the exponential beats the polynomial), and f → ∞ as x → −∞. The curve comes down from +∞, touches 0 at the origin, rises to (2, 4/e²), then decays towards the x-axis.

### Part (c)
For each real k, how many solutions does x² e^{−x} = k have?

**Hints**
1. *Nudge:* Draw horizontal lines on your sketch.
2. *Direction:* The critical values are k = 0 and k = 4/e².
3. *Step:* For 0 < k < 4/e², count the intersections in x < 0, in 0 < x < 2 and in x > 2.

**Model answer.** k < 0: 0 solutions; k = 0: 1; 0 < k < 4/e²: 3; k = 4/e²: 2; k > 4/e²: 1.

### Follow-up (optional)
Show that ∫₀^∞ x² e^{−x} dx = 2.

**Answer.** Integrating by parts twice, ∫₀^N x² e^{−x} dx = 2 − (N² + 2N + 2)e^{−N}, which tends to 2.

---

## Q36 · A curve with a loop

**Topic:** Curve sketching

**Statement.** Consider the curve C: x³ + y³ = 3xy.

### Part (a)
The line y = tx meets C at the origin and at one other point. Find that point, and hence parametrise C.

**Hints**
1. *Nudge:* Substitute y = tx.
2. *Direction:* x³(1 + t³) = 3tx².
3. *Step:* Divide by x², since x ≠ 0 at the other point.

**Model answer.** x = 3t/(1 + t³), y = 3t²/(1 + t³), for t ≠ −1. The values t ≥ 0 trace the loop in the first quadrant, leaving O at t = 0 and returning to O as t → ∞.

### Part (b)
Show that x + y + 1 = 0 is an asymptote, and find the point on the loop, other than O, where the tangent is horizontal.

**Hints**
1. *Nudge:* Which value of t sends the point off to infinity?
2. *Direction:* As t → −1, look at x + y = 3t(1 + t)/(1 + t³) and cancel the factor 1 + t.
3. *Step:* A horizontal tangent needs dy/dt = 0 with dx/dt ≠ 0.

**Model answer.** x + y = 3t/(1 − t + t²), which tends to −1 as t → −1 while x and y become infinite, so x + y + 1 = 0 is an asymptote. dy/dt = 3t(2 − t³)/(1 + t³)², which is zero at t = ∛2 (and dx/dt ≠ 0 there). The tangent is horizontal at (∛2, ∛4).

### Part (c)
Using the polar area formula A = ½∫ r² dθ with tan θ = t, show that the area enclosed by the loop is 3/2.

**Hints**
1. *Nudge:* Express r² = x² + y² in terms of t, and convert dθ into dt.
2. *Direction:* θ = arctan t, so dθ = dt/(1 + t²), and r² = 9t²(1 + t²)/(1 + t³)².
3. *Step:* A = ½∫₀^∞ 9t²/(1 + t³)² dt. Substitute u = 1 + t³.

**Model answer.** A = (9/2)∫₀^∞ t²/(1 + t³)² dt = (9/2)[−1/(3(1 + t³))] from 0 to ∞ = (9/2)(1/3) = 3/2.

### Follow-up (optional)
Find the point of the loop furthest from O.

**Answer.** The curve is symmetric under swapping x and y (t ↔ 1/t), and r² = 9t²(1 + t²)/(1 + t³)² is greatest at t = 1. The furthest point is (3/2, 3/2), at distance 3/√2.

---

## Q37 · Skew lines

**Topic:** Vectors

**Statement.** L_1: r = (1, 2, 0) + s(1, 0, 1) and L_2: r = (0, 0, 3) + t(1, 1, 0).

### Part (a)
Show that L_1 and L_2 are skew, i.e. not parallel and not meeting.

**Hints**
1. *Nudge:* Is one direction vector a multiple of the other?
2. *Direction:* If the lines meet, the coordinates agree for some s and t.
3. *Step:* 1 + s = t, 2 = t and s = 3.

**Model answer.** The directions are not parallel. Meeting would need 1 + s = t, 2 = t and s = 3, which give both t = 2 and t = 4. This is inconsistent, so the lines are skew.

### Part (b)
Find the points P on L_1 and Q on L_2 such that PQ is perpendicular to both lines.

**Hints**
1. *Nudge:* Write the vector PQ in terms of s and t.
2. *Direction:* PQ = (−1 + t − s, −2 + t, 3 − s). Impose PQ · (1, 0, 1) = 0 and PQ · (1, 1, 0) = 0.
3. *Step:* 2 + t − 2s = 0 and −3 + 2t − s = 0.

**Model answer.** s = 7/3 and t = 8/3, so P = (10/3, 2, 7/3) and Q = (8/3, 8/3, 3), with PQ = (2/3)(−1, 1, 1).

### Part (c)
Find the shortest distance between L_1 and L_2, and explain why PQ gives it.

**Hints**
1. *Nudge:* Compute |PQ|.
2. *Direction:* For other points P' on L_1 and Q' on L_2, write the vector P'Q' as PQ plus a combination of the two direction vectors.
3. *Step:* PQ is perpendicular to that combination, so Pythagoras applies.

**Model answer.** |PQ| = (2/3)√3 = 2/√3 ≈ 1.155. For any P' = P + a(1, 0, 1) and Q' = Q + b(1, 1, 0), P'Q' = PQ + w with w perpendicular to PQ, so |P'Q'|² = |PQ|² + |w|² ≥ |PQ|². Alternatively, n = (1, 0, 1) × (1, 1, 0) = (−1, 1, 1) and the distance is |(−1, −2, 3) · n|/|n| = 2/√3.

### Follow-up (optional)
Find the equation of the plane that contains L_1 and is parallel to L_2.

**Answer.** It has normal (−1, 1, 1) and passes through (1, 2, 0): −x + y + z = 1. L_2 lies at distance 2/√3 from it.

---

## Q38 · Medians by vectors

**Topic:** Vectors

**Statement.** Triangle ABC has vertices with position vectors a, b, c, and M is the midpoint of BC.

### Part (a)
Show that the three medians meet at G = (a + b + c)/3, which divides each median in the ratio 2 : 1.

**Hints**
1. *Nudge:* Write down the position vector m of M.
2. *Direction:* Points on AM are a + λ(m − a), with m = (b + c)/2.
3. *Step:* Try λ = 2/3 and look at the symmetry of the result.

**Model answer.** m = (b + c)/2, and a + (2/3)(m − a) = (a + b + c)/3. This expression is symmetric in a, b, c, so G lies on all three medians, with AG : GM = 2 : 1.

### Part (b)
Prove Apollonius' theorem: AB² + AC² = 2AM² + 2BM².

**Hints**
1. *Nudge:* Put the origin at M to simplify.
2. *Direction:* Then c = −b, so AB² = |b − a|² and AC² = |−b − a|².
3. *Step:* |a − b|² + |a + b|² = 2|a|² + 2|b|².

**Model answer.** With the origin at M, c = −b. Then AB² + AC² = |b − a|² + |−b − a|² = 2|a|² + 2|b|² = 2AM² + 2BM², because the cross terms ±2a · b cancel.

### Part (c)
A triangle has sides 7, 8 and 9. Find the lengths of its three medians, and check that the sum of their squares is ¾ of the sum of the squares of the sides.

**Hints**
1. *Nudge:* Use (b), with BM equal to half of the side.
2. *Direction:* The median to side a satisfies m_a² = (2b² + 2c² − a²)/4.
3. *Step:* Start with the median to the side of length 8.

**Model answer.** The median to side 8 is √((2 × 49 + 2 × 81 − 64)/4) = √49 = 7. The median to side 7 is √241/2 ≈ 7.76, and the median to side 9 is √145/2 ≈ 6.02. The sum of the squares is (196 + 241 + 145)/4 = 145.5 = ¾(49 + 64 + 81).

### Follow-up (optional)
Show that GA² + GB² + GC² = (AB² + BC² + CA²)/3.

**Answer.** With the origin at G, a + b + c = 0. Squaring, −2(a · b + b · c + c · a) = |a|² + |b|² + |c|². So AB² + BC² + CA² = 2(|a|² + |b|² + |c|²) − 2(a · b + b · c + c · a) = 3(GA² + GB² + GC²). For the 7–8–9 triangle, the value is 194/3.

---

## Q39 · Tilings and strings

**Topic:** Recurrences

**Statement.** Count arrangements by finding a recurrence.

### Part (a)
Let T_n be the number of ways to tile a 2 × n strip with 1 × 2 dominoes, in either orientation. Find a recurrence, and T_10.

**Hints**
1. *Nudge:* Find T_1, T_2, T_3 and T_4 by drawing.
2. *Direction:* Look at the left end: either one vertical domino, or two horizontal dominoes stacked.
3. *Step:* T_n = T_{n−1} + T_{n−2}.

**Model answer.** T_1 = 1, T_2 = 2 and T_n = T_{n−1} + T_{n−2}, giving 1, 2, 3, 5, 8, 13, 21, 34, 55, 89. So T_10 = 89.

### Part (b)
A 1 × n strip is tiled with 1 × 1 squares, each coloured red or blue, and 1 × 2 dominoes of a single colour. Let a_n be the number of tilings. Find a recurrence and a closed form.

**Hints**
1. *Nudge:* What can the first tile be?
2. *Direction:* a_n = 2a_{n−1} + a_{n−2}, with a_0 = 1 and a_1 = 2.
3. *Step:* Try a_n = r^n: r² = 2r + 1.

**Model answer.** r = 1 ± √2, so a_n = A(1 + √2)^n + B(1 − √2)^n. Fitting a_0 = 1 and a_1 = 2 gives a_n = [(1 + √2)^{n+1} − (1 − √2)^{n+1}]/(2√2). The first values are 2, 5, 12, 29, 70.

### Part (c)
How many binary strings of length 10 contain no three consecutive 1s?

**Hints**
1. *Nudge:* Classify the valid strings by how they end.
2. *Direction:* For n ≥ 3, a valid string ends in 0, 01 or 011, preceded by any valid string.
3. *Step:* b_n = b_{n−1} + b_{n−2} + b_{n−3}, with b_0 = 1, b_1 = 2, b_2 = 4.

**Model answer.** The sequence is 1, 2, 4, 7, 13, 24, 44, 81, 149, 274, 504, so b_10 = 504.

### Follow-up (optional)
How many ways are there to tile a 3 × 8 rectangle with dominoes?

**Answer.** 153. The counts u_n for a 3 × n rectangle satisfy u_n = 4u_{n−2} − u_{n−4}, giving 1, 3, 11, 41, 153 for n = 0, 2, 4, 6, 8. (For odd n there are no tilings.)

---

## Q40 · Solving recurrences

**Topic:** Recurrences

**Statement.** Find closed forms for the sequences defined below.

### Part (a)
u_0 = 5 and u_{n+1} = 3u_n − 2.

**Hints**
1. *Nudge:* Is there a constant sequence satisfying u_{n+1} = 3u_n − 2?
2. *Direction:* The fixed point is 1. Consider v_n = u_n − 1.
3. *Step:* v_{n+1} = 3v_n.

**Model answer.** v_n = 4 × 3^n, so u_n = 4 × 3^n + 1.

### Part (b)
u_0 = 0, u_1 = 1 and u_{n+2} = 5u_{n+1} − 6u_n.

**Hints**
1. *Nudge:* Try u_n = r^n.
2. *Direction:* r² = 5r − 6 has roots 2 and 3, so u_n = A × 2^n + B × 3^n.
3. *Step:* Use u_0 and u_1 to find A and B.

**Model answer.** A + B = 0 and 2A + 3B = 1, so B = 1 and A = −1: u_n = 3^n − 2^n.

### Part (c)
x_0 = 5/2 and x_{n+1} = x_n² − 2.

**Hints**
1. *Nudge:* Write 5/2 as 2 + 1/2.
2. *Direction:* If x = t + 1/t, what is x² − 2?
3. *Step:* (t + 1/t)² − 2 = t² + 1/t².

**Model answer.** Each step squares t, starting from t = 2, so by induction x_n = 2^{2^n} + 2^{−2^n}. For example, x_3 = 256 + 1/256.

### Follow-up (optional)
Find the product x_0 x_1 ⋯ x_{n−1} in closed form.

**Answer.** Multiply by t − 1/t = 3/2 and telescope, using (t^m − t^{−m})(t^m + t^{−m}) = t^{2m} − t^{−2m}. The product is (2/3)(2^{2^n} − 2^{−2^n}).

---

## Q41 · Irrationality and parity

**Topic:** Proof by contradiction

**Statement.** Prove that certain things are impossible by assuming that they are possible.

### Part (a)
Prove that √2 is irrational.

**Hints**
1. *Nudge:* Suppose √2 = p/q in lowest terms.
2. *Direction:* Then p² = 2q². What does that tell you about p?
3. *Step:* If p is even, p = 2r, so q² = 2r², so q is even.

**Model answer.** If √2 = p/q in lowest terms, then p² = 2q². So p² is even, hence p is even. Writing p = 2r gives q² = 2r², so q is even too, contradicting lowest terms.

### Part (b)
Prove that log_2 3 is irrational.

**Hints**
1. *Nudge:* Suppose log_2 3 = p/q with positive integers p and q.
2. *Direction:* Rewrite the equation without logarithms.
3. *Step:* 2^p = 3^q. Look at parity.

**Model answer.** log_2 3 > 0, so if it equals p/q with p, q ≥ 1, then 2^{p/q} = 3 and so 2^p = 3^q. The left side is even and the right side is odd, a contradiction.

### Part (c)
Prove that if a, b, c are odd integers, then ax² + bx + c = 0 has no rational root.

**Hints**
1. *Nudge:* Suppose x = p/q in lowest terms is a root, and clear denominators.
2. *Direction:* ap² + bpq + cq² = 0. Consider the parities of p and q.
3. *Step:* p and q cannot both be even. Check the cases (odd, odd), (odd, even) and (even, odd).

**Model answer.** ap² + bpq + cq² = 0. If p and q are both odd, all three terms are odd, so the sum is odd and cannot be 0. If p is odd and q even, ap² is odd and the other terms are even, so the sum is odd. If p is even and q odd, cq² is odd and the others are even. Every case is a contradiction, so there is no rational root.

### Follow-up (optional)
Show that, for odd a, b, c, the discriminant b² − 4ac is ≡ 5 (mod 8), and use this for a second proof.

**Answer.** Odd squares are ≡ 1 (mod 8) and 4ac ≡ 4 (mod 8), so b² − 4ac ≡ 5. But every square is ≡ 0, 1 or 4 (mod 8), so the discriminant is not a perfect square, and the roots are not rational.

---

## Q42 · Primes and polynomials

**Topic:** Proof by contradiction

**Statement.** Classic contradiction arguments about primes.

### Part (a)
Prove that there are infinitely many primes. Is p_1 p_2 ⋯ p_k + 1 always prime, when p_1, …, p_k are the first k primes?

**Hints**
1. *Nudge:* Suppose p_1, …, p_k are all the primes.
2. *Direction:* Consider N = p_1 p_2 ⋯ p_k + 1. Which primes can divide it?
3. *Step:* N leaves remainder 1 on division by each p_i. For the second question, try k = 6.

**Model answer.** Every prime factor of N is missing from the list p_1, …, p_k, because each p_i leaves remainder 1. This contradicts the list being complete. N need not be prime: 2 × 3 × 5 × 7 × 11 × 13 + 1 = 30031 = 59 × 509.

### Part (b)
Prove that there are infinitely many primes of the form 4k + 3.

**Hints**
1. *Nudge:* Copy the argument of (a), but with a different N.
2. *Direction:* If p_1, …, p_k are all the primes ≡ 3 (mod 4), take N = 4p_1 ⋯ p_k − 1.
3. *Step:* N is odd and N ≡ 3 (mod 4). A product of numbers that are ≡ 1 (mod 4) is ≡ 1 (mod 4).

**Model answer.** N is odd, so all its prime factors are odd, i.e. ≡ 1 or 3 (mod 4). They cannot all be ≡ 1 (mod 4), because then N would be ≡ 1. So some prime factor q of N is ≡ 3 (mod 4). But q is not any p_i, since N ≡ −1 (mod p_i). This is a contradiction.

### Part (c)
Show that no non-constant polynomial P with integer coefficients has P(n) prime for every positive integer n. Use your argument to find an n for which n² + n + 41 is composite.

**Hints**
1. *Nudge:* Let p = P(1), assumed prime. What can you say about P(1 + p) mod p?
2. *Direction:* a − b always divides P(a) − P(b), so (1 + kp) − 1 divides P(1 + kp) − P(1). Hence p divides P(1 + kp).
3. *Step:* If all the numbers P(1 + kp) are prime and divisible by p, they all equal p.

**Model answer.** Each P(1 + kp) is a prime divisible by p, so it equals p, for infinitely many k. Then P(x) − p has infinitely many roots, so P is constant, a contradiction. For n² + n + 41: P(1) = 43, so try n = 1 + 43 = 44, giving 44² + 44 + 41 = 2021 = 43 × 47.

### Follow-up (optional)
Why does the argument of (b) fail for primes ≡ 1 (mod 4), using N = 4p_1 ⋯ p_k + 1?

**Answer.** N ≡ 1 (mod 4) could be a product of primes that are ≡ 3 (mod 4). For example, 21 = 3 × 7 ≡ 1 (mod 4). So we cannot guarantee a new prime ≡ 1 (mod 4).
