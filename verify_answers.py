#!/usr/bin/env python3
"""Numerically verify the model answers in question_bank.md.

Every part of every problem (keys like Q07b, and Q07f for the follow-up) gets one of:

* a numerical check: brute force on small cases, exact rational arithmetic,
  Monte Carlo simulation, numerical integration, ODE solving, optimisation or limits.
  Before checking anything, the script confirms that the value it is about to test
  appears in that part's model answer, so the document and the checks cannot drift apart;
* a "spot-check": the model answer is a proof, so the script tests the statement being
  proved on many cases. The argument itself cannot be checked numerically;
* an entry in NOT_CHECKABLE, with the reason.

The script also confirms that every part in the bank is accounted for.
Standard library only.

    python3 verify_answers.py            # summary and failures
    python3 verify_answers.py -v         # one line per part
    python3 verify_answers.py --only Q18  # a subset (prefix match)
    python3 verify_answers.py --bank other.md

The exit status is 1 if any check fails or any part is unaccounted for.
"""
from __future__ import annotations

import argparse
import cmath
import itertools
import math
import random
import re
import sys
import time
from dataclasses import dataclass
from fractions import Fraction as Fr
from functools import lru_cache
from pathlib import Path
from typing import Callable

BANK = Path(__file__).resolve().with_name("question_bank.md")

# ======================================================================================
# Parsing the bank
# ======================================================================================

HEAD_RE = re.compile(r"^### (?:Part \((?P<part>[abc])\)|Follow-up \(optional\))\s*$", re.M)
PROB_RE = re.compile(r"^## (Q\d\d)\b.*$", re.M)


def normalise(s: str) -> str:
    return " ".join(s.split())


def parse_bank(text: str) -> dict[str, str]:
    """Map 'Q01a' etc. to the normalised text of that part's model answer."""
    answers: dict[str, str] = {}
    probs = list(PROB_RE.finditer(text))
    for i, m in enumerate(probs):
        qid = m.group(1)
        body = text[m.end(): probs[i + 1].start() if i + 1 < len(probs) else len(text)]
        heads = list(HEAD_RE.finditer(body))
        for j, h in enumerate(heads):
            sec = body[h.end(): heads[j + 1].start() if j + 1 < len(heads) else len(body)]
            key = qid + (h.group("part") or "f")
            marker = "**Model answer.**" if h.group("part") else "**Answer.**"
            k = sec.find(marker)
            if k < 0:
                answers[key] = ""
                continue
            ans = sec[k + len(marker):]
            ans = re.split(r"^---\s*$", ans, flags=re.M)[0]
            answers[key] = normalise(ans)
    return answers


# ======================================================================================
# Registry
# ======================================================================================

@dataclass
class Check:
    fn: Callable[[], None]
    snippets: tuple[str, ...]
    kind: str  # exact | numeric | simulation | spot-check
    note: str


CHECKS: dict[str, Check] = {}
NOT_CHECKABLE: dict[str, str] = {}
KINDS = ("exact", "numeric", "simulation", "spot-check")


def check(key: str, *snippets: str, kind: str = "exact", note: str = ""):
    assert kind in KINDS, kind

    def deco(fn):
        assert key not in CHECKS, f"duplicate check {key}"
        CHECKS[key] = Check(fn, snippets, kind, note)
        return fn

    return deco


class CheckFailed(AssertionError):
    pass


def ensure(cond: bool, msg: str) -> None:
    if not cond:
        raise CheckFailed(msg)


def close(got: float, want: float, tol: float = 1e-9, what: str = "value") -> None:
    if not (abs(got - want) <= tol * max(1.0, abs(want))):
        raise CheckFailed(f"{what}: got {got!r}, expected {want!r} (tol {tol})")


def cclose(got: complex, want: complex, tol: float = 1e-9, what: str = "value") -> None:
    if not (abs(got - want) <= tol * max(1.0, abs(want))):
        raise CheckFailed(f"{what}: got {got!r}, expected {want!r}")


# ======================================================================================
# Numerical toolkit
# ======================================================================================

def mc_mean(sample: Callable[[], float], n: int, expected: float, what: str) -> None:
    """Monte Carlo: sample mean must lie within 5 standard errors of `expected`."""
    s = s2 = 0.0
    for _ in range(n):
        x = sample()
        s += x
        s2 += x * x
    mean = s / n
    var = max(s2 / n - mean * mean, 0.0)
    se = math.sqrt(var / n)
    if abs(mean - expected) > 5 * se + 1e-12:
        raise CheckFailed(f"{what}: simulated {mean:.5f} ± {se:.5f} (n={n}), expected {expected:.5f}")


def simpson(f: Callable[[float], float], a: float, b: float, n: int = 4000) -> float:
    n += n % 2
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4 if i % 2 else 2) * f(a + i * h)
    return s * h / 3


def rk4_step(f, t, y, h):
    k1 = f(t, y)
    k2 = f(t + h / 2, y + h * k1 / 2)
    k3 = f(t + h / 2, y + h * k2 / 2)
    k4 = f(t + h, y + h * k3)
    return y + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6


def rk4(f, t0: float, y0: float, t1: float, n: int = 4000) -> float:
    h = (t1 - t0) / n
    t, y = t0, y0
    for _ in range(n):
        y = rk4_step(f, t, y, h)
        t += h
    return y


def rk4_hit(f, t0: float, y0: float, target: float, h: float = 1e-3, tmax: float = 100.0) -> float:
    """Integrate y' = f(t, y) until y crosses `target`; return the crossing time."""
    t, y = t0, y0
    side = y - target
    while t < tmax:
        y1 = rk4_step(f, t, y, h)
        if (y1 - target) * side <= 0:
            lo, hi = 0.0, h
            for _ in range(60):
                mid = (lo + hi) / 2
                if (rk4_step(f, t, y, mid) - target) * side > 0:
                    lo = mid
                else:
                    hi = mid
            return t + (lo + hi) / 2
        t, y = t + h, y1
    raise CheckFailed("rk4_hit: target never reached")


def golden(f: Callable[[float], float], a: float, b: float, maximise: bool = False,
           iters: int = 200) -> tuple[float, float]:
    """Golden-section search for the minimum (or maximum) of a unimodal f on [a, b]."""
    sgn = -1.0 if maximise else 1.0
    g = (math.sqrt(5) - 1) / 2
    c, d = b - g * (b - a), a + g * (b - a)
    fc, fd = sgn * f(c), sgn * f(d)
    for _ in range(iters):
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - g * (b - a)
            fc = sgn * f(c)
        else:
            a, c, fc = c, d, fd
            d = a + g * (b - a)
            fd = sgn * f(d)
    x = (a + b) / 2
    return x, f(x)


def grid_then_golden(f, a, b, n=4000, maximise=False):
    """Coarse grid search to bracket the global optimum, then golden-section refinement."""
    xs = [a + (b - a) * i / n for i in range(n + 1)]
    vals = [f(x) for x in xs]
    best = (max if maximise else min)(range(n + 1), key=lambda i: vals[i])
    lo, hi = xs[max(best - 1, 0)], xs[min(best + 1, n)]
    return golden(f, lo, hi, maximise)


def bisect_root(f, a, b, iters=200):
    fa = f(a)
    for _ in range(iters):
        m = (a + b) / 2
        fm = f(m)
        if (fm > 0) == (fa > 0):
            a, fa = m, fm
        else:
            b = m
    return (a + b) / 2


def poly_roots(coeffs: list[complex]) -> list[complex]:
    """All complex roots of a polynomial (coefficients highest degree first), Durand-Kerner."""
    a = [complex(c) / coeffs[0] for c in coeffs]
    n = len(a) - 1
    roots = [(0.4 + 0.9j) ** k for k in range(n)]
    for _ in range(2000):
        new = []
        for i, r in enumerate(roots):
            num = 0j
            for c in a:
                num = num * r + c
            den = 1 + 0j
            for j, s in enumerate(roots):
                if j != i:
                    den *= r - s
            new.append(r - num / den)
        done = max(abs(x - y) for x, y in zip(new, roots)) < 1e-15
        roots = new
        if done:
            break
    return roots


def poly_rem(num: list, den: list) -> list:
    """Remainder of polynomial division (coefficient lists, highest degree first), exact."""
    num = [Fr(c) for c in num]
    den = [Fr(c) for c in den]
    while len(num) >= len(den):
        q = num[0] / den[0]
        for i in range(len(den)):
            num[i] -= q * den[i]
        num.pop(0)
    while num and num[0] == 0:
        num.pop(0)
    return num


def solve_linear(A: list[list], b: list) -> list:
    """Exact Gaussian elimination over the rationals."""
    n = len(A)
    M = [[Fr(x) for x in row] + [Fr(bi)] for row, bi in zip(A, b)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                fac = M[r][c] / M[c][c]
                M[r] = [x - fac * y for x, y in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def factorise(n: int) -> list[int]:
    out, d = [], 2
    while d * d <= n:
        while n % d == 0:
            out.append(d)
            n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


@lru_cache(maxsize=None)
def fib(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def rand_frac(rng: random.Random, lim: int = 50) -> Fr:
    return Fr(rng.randint(-lim, lim), rng.randint(1, lim))


def count_solutions(g: Callable[[float], float], a: float, b: float, n: int = 20000) -> int:
    """Count the zeros of g on [a, b]: strict sign changes on a fine grid, plus touching
    zeros (local minima of |g| without a sign change, refined and required to be ~0)."""
    xs = [a + (b - a) * i / n for i in range(n + 1)]
    vs = [g(x) for x in xs]
    count = sum(1 for v in vs if v == 0)  # zeros that land exactly on a grid point
    count += sum(1 for i in range(n) if vs[i] * vs[i + 1] < 0)
    for i in range(1, n):
        # strict on the left so that flat runs of identical floats are not "minima"
        if vs[i - 1] * vs[i] > 0 and vs[i] * vs[i + 1] > 0 and abs(vs[i]) < abs(vs[i - 1]) \
                and abs(vs[i]) <= abs(vs[i + 1]):
            _, v = golden(lambda x: abs(g(x)), xs[i - 1], xs[i + 1])
            if abs(v) < 1e-9:
                count += 1
    return count


# ======================================================================================
# Q01  Sums of consecutive integers
# ======================================================================================

def consecutive_reps_upto(L: int) -> list[list[tuple[int, ...]]]:
    """Brute force: every run a, a+1, ..., b (b > a) with sum <= L."""
    reps: list[list[tuple[int, ...]]] = [[] for _ in range(L + 1)]
    for a in range(1, L + 1):
        s = a
        for b in range(a + 1, L + 1):
            s += b
            if s > L:
                break
            reps[s].append(tuple(range(a, b + 1)))
    return reps


@lru_cache(maxsize=None)
def _reps5000():
    return consecutive_reps_upto(5000)


def odd_divisor_counts(L: int) -> list[int]:
    c = [0] * (L + 1)
    for d in range(1, L + 1, 2):
        for m in range(d, L + 1, d):
            c[m] += 1
    return c


@check("Q01a", "15 = 7+8 = 4+5+6 = 1+2+3+4+5 (3 ways)", "30 = 9+10+11 = 6+7+8+9 = 4+5+6+7+8 (3 ways)")
def _():
    reps = _reps5000()
    ensure(set(reps[15]) == {(7, 8), (4, 5, 6), (1, 2, 3, 4, 5)}, f"15: {reps[15]}")
    ensure(set(reps[30]) == {(9, 10, 11), (6, 7, 8, 9), (4, 5, 6, 7, 8)}, f"30: {reps[30]}")


@check("Q01b", "k(2a + k − 1)/2", kind="spot-check",
       note="formula checked for a, k ≤ 60; no power of 2 up to 2^30 has a representation")
def _():
    for a in range(1, 61):
        for k in range(1, 61):
            ensure(sum(range(a, a + k)) * 2 == k * (2 * a + k - 1), f"formula a={a} k={k}")
    reps = _reps5000()
    for m in range(13):
        ensure(reps[2 ** m] == [], f"2^{m} has representation {reps[2 ** m]}")
    for m in range(13, 31):  # beyond the brute-force table: test each run length k
        N = 2 ** m
        k = 2
        while k * (k + 1) // 2 <= N:
            ensure((N - k * (k - 1) // 2) % k != 0, f"2^{m} with k={k}")
            k += 1


@check("Q01c", "(number of odd divisors) − 1", kind="spot-check",
       note="number of representations = odd divisors − 1 for every N ≤ 5000")
def _():
    reps, od = _reps5000(), odd_divisor_counts(5000)
    for N in range(1, 5001):
        ensure(len(reps[N]) == od[N] - 1, f"N={N}: {len(reps[N])} reps, {od[N]} odd divisors")


@check("Q01f", "N = 2^a × p with p an odd prime")
def _():
    reps = _reps5000()
    for N in range(1, 5001):
        m = N
        while m % 2 == 0:
            m //= 2
        ensure((len(reps[N]) == 1) == (m > 1 and is_prime(m)), f"N={N}")


# ======================================================================================
# Q02  A divisibility pattern
# ======================================================================================

@check("Q02a", "6 divides n³ − n", kind="spot-check", note="checked for |n| ≤ 2000")
def _():
    ensure(all((n ** 3 - n) % 6 == 0 for n in range(-2000, 2001)), "n³ − n")


@check("Q02b", "30 divides n⁵ − n", "n² + 1 ≡ 4 + 1 ≡ 0", kind="spot-check",
       note="checked for |n| ≤ 2000, and the mod 5 case analysis on all residues")
def _():
    ensure(all((n ** 5 - n) % 30 == 0 for n in range(-2000, 2001)), "n⁵ − n")
    for r in (2, 3):
        ensure((r * r + 1) % 5 == 0, f"n ≡ {r}")


@check("Q02c", "The largest such integer is 30")
def _():
    g = 0
    for n in range(2, 500):
        g = math.gcd(g, n ** 5 - n)
    ensure(g == 30, f"gcd = {g}")


@check("Q02f", "42", "2⁷ − 2 = 126", "3⁷ − 3 = 2184")
def _():
    ensure(2 ** 7 - 2 == 126 and 3 ** 7 - 3 == 2184, "values")
    g = 0
    for n in range(2, 500):
        g = math.gcd(g, n ** 7 - n)
    ensure(g == 42, f"gcd = {g}")


# ======================================================================================
# Q03  Last digits
# ======================================================================================

@check("Q03a", "the last digit of 7^2026 is 9", "7, 9, 3, 1")
def _():
    ensure([pow(7, k, 10) for k in range(1, 9)] == [7, 9, 3, 1] * 2, "cycle")
    ensure(pow(7, 2026, 10) == 9, "last digit")


@check("Q03b", "7⁴ = 2401", "The last two digits are 49")
def _():
    ensure(7 ** 4 == 2401 and pow(7, 2026, 100) == 49, str(pow(7, 2026, 100)))


@check("Q03c", "3^20 ≡ 49² ≡ 1", "3⁶ = 729 ≡ 29", "the last two digits are 78")
def _():
    ensure(pow(3, 10, 100) == 49 and pow(3, 20, 100) == 1, "3^20")
    ensure(pow(3, 2026, 100) == 29, "3^2026")
    ensure((3 ** 2026 + 7 ** 2026) % 100 == 78, "sum")


@check("Q03f", "343 ≡ 43")
def _():
    ensure(pow(7, 7 ** 7, 100) == 43, str(pow(7, 7 ** 7, 100)))


# ======================================================================================
# Q04  Coin patterns (simulation)
# ======================================================================================

def tosses_until(pattern: str, rng: random.Random) -> int:
    last, n = "", 0
    L = len(pattern)
    while True:
        last = (last + ("H" if rng.getrandbits(1) else "T"))[-L:]
        n += 1
        if last == pattern:
            return n


@check("Q04a", "E = 2", kind="simulation")
def _():
    rng = random.Random(41)
    mc_mean(lambda: tosses_until("H", rng), 100_000, 2.0, "tosses to first H")


@check("Q04b", "E_0 = 6", kind="simulation")
def _():
    rng = random.Random(42)
    mc_mean(lambda: tosses_until("HH", rng), 100_000, 6.0, "tosses to HH")


@check("Q04c", "HT takes 4 tosses on average and HH takes 6", kind="simulation")
def _():
    rng = random.Random(43)
    mc_mean(lambda: tosses_until("HT", rng), 100_000, 4.0, "tosses to HT")


@check("Q04f", "1/4", kind="simulation")
def _():
    rng = random.Random(44)

    def trial():
        last = ""
        while True:
            last = (last + ("H" if rng.getrandbits(1) else "T"))[-2:]
            if last == "HH":
                return 1.0
            if last == "TH":
                return 0.0

    mc_mean(trial, 200_000, 0.25, "P(HH before TH)")


# ======================================================================================
# Q05  Breaking a stick
# ======================================================================================

@check("Q05a", "1 − ¼ = 3/4", "overall probability is also 2/3", kind="simulation")
def _():
    rng = random.Random(51)
    mc_mean(lambda: max(u := rng.random(), 1 - u), 200_000, 0.75, "E[longer]")
    mc_mean(lambda: float(max(u := rng.random(), 1 - u) > 2 * min(u, 1 - u)), 200_000, 2 / 3,
            "P(longer > 2 shorter)")


@check("Q05b", "2 ln 2 − 1 ≈ 0.386", kind="numeric",
       note="numerical integration of E[shorter/longer] and simulation")
def _():
    exact = 2 * math.log(2) - 1
    close(2 * simpson(lambda u: u / (1 - u), 0, 0.5), exact, 1e-10, "integral")
    close(round(exact, 3), 0.386, 1e-12, "rounding")
    rng = random.Random(52)
    mc_mean(lambda: min(u := rng.random(), 1 - u) / max(u, 1 - u), 200_000, exact, "E[ratio]")


@check("Q05c", "(1/8)/(1/2) = 1/4", kind="simulation")
def _():
    rng = random.Random(53)

    def trial():
        x, y = sorted((rng.random(), rng.random()))
        return float(max(x, y - x, 1 - y) < 0.5)

    mc_mean(trial, 300_000, 0.25, "P(triangle)")


@check("Q05f", "1/9", kind="simulation", note="simulation and numerical integration")
def _():
    rng = random.Random(54)

    def trial():
        x, y = sorted((rng.random(), rng.random()))
        return min(x, y - x, 1 - y)

    mc_mean(trial, 300_000, 1 / 9, "E[shortest]")
    close(simpson(lambda s: (1 - 3 * s) ** 2, 0, 1 / 3), 1 / 9, 1e-12, "integral")


# ======================================================================================
# Q06  Frog (gambler's ruin)
# ======================================================================================

def frog_exact(N: int, start: int, pr: Fr) -> tuple[Fr, Fr]:
    """Exact P(reach N before 0) and expected number of jumps, by solving linear systems."""
    pl = 1 - pr
    n = N - 1  # unknowns for pads 1..N-1
    A = [[Fr(0)] * n for _ in range(n)]
    bp, bt = [Fr(0)] * n, [Fr(1)] * n
    for k in range(1, N):
        i = k - 1
        A[i][i] = Fr(1)
        if k + 1 < N:
            A[i][i + 1] -= pr
        else:
            bp[i] += pr  # p_N = 1
        if k - 1 > 0:
            A[i][i - 1] -= pl
    p = solve_linear(A, bp)
    t = solve_linear(A, bt)
    return p[start - 1], t[start - 1]


def frog_sim(N, start, pr, rng):
    k, steps = start, 0
    while 0 < k < N:
        k += 1 if rng.random() < pr else -1
        steps += 1
    return k == N, steps


@check("Q06a", "p_1 = 1/4", kind="simulation", note="simulation and exact linear solve")
def _():
    ensure(frog_exact(4, 1, Fr(1, 2))[0] == Fr(1, 4), "exact")
    rng = random.Random(61)
    mc_mean(lambda: float(frog_sim(4, 1, 0.5, rng)[0]), 200_000, 0.25, "P(home)")


@check("Q06b", "T_1 = 3", "T_k = k(4 − k)", kind="simulation", note="simulation and exact linear solve")
def _():
    for k in range(1, 4):
        ensure(frog_exact(4, k, Fr(1, 2))[1] == k * (4 - k), f"T_{k}")
    rng = random.Random(62)
    mc_mean(lambda: frog_sim(4, 1, 0.5, rng)[1], 200_000, 3.0, "E[jumps]")


@check("Q06c", "p_1 = 8/15", kind="simulation", note="simulation and exact linear solve")
def _():
    ensure(frog_exact(4, 1, Fr(2, 3))[0] == Fr(8, 15), "exact")
    rng = random.Random(63)
    mc_mean(lambda: float(frog_sim(4, 1, 2 / 3, rng)[0]), 200_000, 8 / 15, "P(home)")


@check("Q06f", "the answer is 25")
def _():
    for N in range(2, 13):
        for k in range(1, N):
            ensure(frog_exact(N, k, Fr(1, 2))[1] == k * (N - k), f"N={N} k={k}")
    ensure(frog_exact(10, 5, Fr(1, 2))[1] == 25, "N=10")


# ======================================================================================
# Q07  Lattice paths
# ======================================================================================

def lattice_paths(m: int, n: int):
    """All R/U words from (0,0) to (m,n), as lists of visited points."""
    for word in itertools.product("RU", repeat=m + n):
        if word.count("R") != m:
            continue
        x = y = 0
        pts = [(0, 0)]
        for c in word:
            if c == "R":
                x += 1
            else:
                y += 1
            pts.append((x, y))
        yield pts


@check("Q07a", "C(7, 3) = 35")
def _():
    ensure(sum(1 for _ in lattice_paths(4, 3)) == 35, "count")


@check("Q07b", "C(3, 1) × C(4, 2) = 3 × 6 = 18", "35 − 18 = 17")
def _():
    paths = list(lattice_paths(4, 3))
    through = sum(1 for p in paths if (2, 1) in p)
    ensure(through == 18 and len(paths) - through == 17, f"through={through}")


@check("Q07c", "70 − 56 = 14", "C(2n, n)/(n + 1)")
def _():
    for n in range(1, 9):
        good = sum(1 for p in lattice_paths(n, n) if all(y <= x for x, y in p))
        ensure(good == math.comb(2 * n, n) // (n + 1), f"n={n}: {good}")
        ensure(math.comb(2 * n, n) - math.comb(2 * n, n + 1) == good, f"reflection n={n}")
        if n == 4:
            ensure(good == 14, "n=4")


@check("Q07f", "C(2n − 2, n − 1)/n", "For n = 4 that is 5")
def _():
    for n in range(1, 9):
        cnt = sum(1 for p in lattice_paths(n, n) if all(y < x for x, y in p[1:-1]))
        ensure(cnt == math.comb(2 * n - 2, n - 1) // n, f"n={n}: {cnt}")
        if n == 4:
            ensure(cnt == 5, "n=4")


# ======================================================================================
# Q08  Derangements
# ======================================================================================

@lru_cache(maxsize=None)
def derangements(n: int) -> int:
    return sum(1 for p in itertools.permutations(range(n)) if all(p[i] != i for i in range(n)))


@check("Q08a", "D_2 = 1, D_3 = 2, D_4 = 9")
def _():
    ensure([derangements(n) for n in (2, 3, 4)] == [1, 2, 9], "values")


@check("Q08b", "D_5 = 4(9 + 2) = 44", "D_6 = 5(44 + 9) = 265")
def _():
    ensure(derangements(5) == 44 and derangements(6) == 265, "values")
    for n in range(3, 9):
        ensure(derangements(n) == (n - 1) * (derangements(n - 1) + derangements(n - 2)), f"n={n}")


@check("Q08c", "e^{−1} ≈ 0.3679", "265/720 ≈ 0.3681", kind="numeric",
       note="inclusion–exclusion formula checked exactly for n ≤ 8; the limit numerically")
def _():
    for n in range(1, 9):
        formula = math.factorial(n) * sum(Fr((-1) ** k, math.factorial(k)) for k in range(n + 1))
        ensure(formula == derangements(n), f"n={n}")
    close(round(265 / 720, 4), 0.3681, 1e-12, "D6/6!")
    p20 = sum((-1) ** k / math.factorial(k) for k in range(21))
    close(p20, math.exp(-1), 1e-15, "limit")
    close(round(math.exp(-1), 4), 0.3679, 1e-12, "rounding")


@check("Q08f", "15 × 9 = 135")
def _():
    cnt = sum(1 for p in itertools.permutations(range(6)) if sum(p[i] == i for i in range(6)) == 2)
    ensure(cnt == 135, str(cnt))


# ======================================================================================
# Q09  Stars, bars and gaps
# ======================================================================================

def sols3(total, cap=None):
    return [(a, b, total - a - b) for a in range(total + 1) for b in range(total + 1 - a)
            if cap is None or max(a, b, total - a - b) <= cap]


@check("Q09a", "C(12, 2) = 66")
def _():
    ensure(len(sols3(10)) == 66, "count")


@check("Q09b", "C(7, 2) = 21", "66 − 63 + 3 = 6")
def _():
    ensure(len(sols3(10, 4)) == 6, "capped")
    ensure(sum(1 for s in sols3(10) if s[0] >= 5) == 21, "a ≥ 5")


@check("Q09c", "C(18, 3) = 816")
def _():
    cnt = sum(1 for c in itertools.combinations(range(1, 21), 3) if c[1] - c[0] > 1 and c[2] - c[1] > 1)
    ensure(cnt == 816, str(cnt))


@check("Q09f", "800", "C(16, 2) = 120", "C(17, 3) = 680")
def _():
    def ok(c):
        return all((b - a) % 20 not in (1, 19) for a, b in itertools.combinations(c, 2))
    combos = [c for c in itertools.combinations(range(1, 21), 3) if ok(c)]
    ensure(len(combos) == 800, str(len(combos)))
    ensure(sum(1 for c in combos if 1 in c) == 120, "with person 1")


# ======================================================================================
# Q10  Telescoping sums
# ======================================================================================

@check("Q10a", "n/(n + 1)")
def _():
    s = Fr(0)
    for n in range(1, 60):
        s += Fr(1, n * (n + 1))
        ensure(s == Fr(n, n + 1), f"n={n}")


@check("Q10b", "1/4 − 1/(2(n + 1)(n + 2))", "tends to 1/4")
def _():
    s = Fr(0)
    for n in range(1, 60):
        s += Fr(1, n * (n + 1) * (n + 2))
        ensure(s == Fr(1, 4) - Fr(1, 2 * (n + 1) * (n + 2)), f"n={n}")


@check("Q10c", "1 − 1/(n + 1)!", "The sum is 1")
def _():
    s = Fr(0)
    for n in range(1, 40):
        s += Fr(n, math.factorial(n + 1))
        ensure(s == 1 - Fr(1, math.factorial(n + 1)), f"n={n}")
    close(float(s), 1.0, 1e-15, "limit")


@check("Q10f", "1 − 1/(n + 1)²")
def _():
    s = Fr(0)
    for n in range(1, 200):
        s += Fr(2 * n + 1, n * n * (n + 1) ** 2)
        ensure(s == 1 - Fr(1, (n + 1) ** 2), f"n={n}")
    close(sum((2 * r + 1) / (r * r * (r + 1) ** 2) for r in range(1, 10 ** 6)), 1.0, 1e-11, "limit")


# ======================================================================================
# Q11  Iterated square root
# ======================================================================================

def x_seq(c: float, n: int) -> list[float]:
    xs = [math.sqrt(c)]
    while len(xs) < n:
        xs.append(math.sqrt(c + xs[-1]))
    return xs


@check("Q11a", "x_2 ≈ 1.848 and x_3 ≈ 1.962", "L = 2", kind="numeric")
def _():
    xs = x_seq(2, 60)
    close(round(xs[1], 3), 1.848, 1e-12, "x2")
    close(round(xs[2], 3), 1.962, 1e-12, "x3")
    close(xs[-1], 2.0, 1e-15, "limit")


@check("Q11b", "x_{n+1} < x_{n+2} < 2", kind="spot-check", note="checked for n ≤ 20 in floating point")
def _():
    xs = x_seq(2, 21)
    for n in range(20):
        ensure(math.sqrt(2) <= xs[n] < xs[n + 1] < 2, f"n={n + 1}")


@check("Q11c", "(2 − √2)/3^{n−1}", kind="numeric", note="identity and bound checked for n ≤ 20")
def _():
    xs = x_seq(2, 21)
    for n in range(20):
        close(2 - xs[n + 1], (2 - xs[n]) / (2 + xs[n + 1]), 1e-12, f"identity n={n + 1}")
        ensure(0 < 2 - xs[n] <= (2 - math.sqrt(2)) / 3 ** n * (1 + 1e-12), f"bound n={n + 1}")


@check("Q11f", "(1 + √(1 + 4c))/2", "c = 6 gives 3", kind="numeric")
def _():
    for c in (0.1, 0.5, 1, 2, 6, 12, 30):
        close(x_seq(c, 200)[-1], (1 + math.sqrt(1 + 4 * c)) / 2, 1e-12, f"c={c}")
    close(x_seq(6, 200)[-1], 3.0, 1e-12, "c=6")


# ======================================================================================
# Q12  Comparison tests
# ======================================================================================

@check("Q12a", "1 + 1/2 + … + 1/2^k ≥ 1 + k/2", kind="spot-check",
       note="H(2^k) ≥ 1 + k/2 checked for k ≤ 20; divergence itself is not a finite computation")
def _():
    h, n = 0.0, 0
    for k in range(21):
        while n < 2 ** k:
            n += 1
            h += 1 / n
        ensure(h >= 1 + k / 2, f"k={k}: {h}")


@check("Q12b", "2 − 1/N < 2", kind="spot-check", note="checked for every N ≤ 10^5")
def _():
    s = 0.0
    for N in range(1, 100_001):
        s += 1 / (N * N)
        ensure(s < 2 - 1 / N + 1e-12, f"N={N}")


@check("Q12c", "8 × 0.9^{k−1}", "S < 8/(1 − 0.9) = 80", kind="spot-check",
       note="count 8·9^(k−1) checked for k ≤ 6, group bounds and partial sum up to 10^6 checked; "
            "the infinite sum itself cannot be computed")
def _():
    total = 0.0
    for k in range(1, 7):
        cnt, grp = 0, 0.0
        for n in range(10 ** (k - 1), 10 ** k):
            if "9" not in str(n):
                cnt += 1
                grp += 1 / n
        ensure(cnt == 8 * 9 ** (k - 1), f"count k={k}: {cnt}")
        ensure(grp < 8 * 0.9 ** (k - 1), f"group bound k={k}")
        total += grp
    ensure(total < 80, "partial sum")
    close(8 / (1 - 0.9), 80, 1e-12, "geometric sum")


@check("Q12f", "1 + 1/4 + 1/2 = 7/4", "π²/6 ≈ 1.645", kind="numeric")
def _():
    N = 500
    tele = sum(Fr(1, n - 1) - Fr(1, n) for n in range(3, N + 1))
    ensure(tele == Fr(1, 2) - Fr(1, N), "telescoping tail → 1/2")
    ensure(1 + Fr(1, 4) + Fr(1, 2) == Fr(7, 4), "7/4")
    s = 0.0
    for N in range(1, 200_001):
        s += 1 / (N * N)
        if N <= 2000:
            ensure(s <= 1.75, f"N={N}")
    s += 1 / 200_000  # tail ≈ 1/N
    close(s, math.pi ** 2 / 6, 1e-9, "Basel")
    close(round(math.pi ** 2 / 6, 3), 1.645, 1e-12, "rounding")


# ======================================================================================
# Q13  AM-GM
# ======================================================================================

@check("Q13a", "(a + b)/2 ≥ √(ab)", kind="spot-check", note="100 000 random pairs")
def _():
    rng = random.Random(131)
    for _ in range(100_000):
        a, b = rng.uniform(1e-3, 100), rng.uniform(1e-3, 100)
        ensure((a + b) / 2 >= math.sqrt(a * b) - 1e-12, f"{a},{b}")
    ensure(abs((7 + 7) / 2 - math.sqrt(49)) < 1e-15, "equality case")


@check("Q13b", "3/√2 = 3√2/2 ≈ 2.121", kind="numeric")
def _():
    f = lambda x: (x * x + 3) / math.sqrt(x * x + 2)
    x, v = grid_then_golden(f, -10, 10)
    close(v, 3 / math.sqrt(2), 1e-12, "minimum")
    close(x, 0.0, 1e-5, "argmin")
    close(round(3 / math.sqrt(2), 3), 2.121, 1e-12, "rounding")


@check("Q13c", "x = 2. The minimum is 3.", kind="numeric")
def _():
    x, v = grid_then_golden(lambda x: x + 4 / x ** 2, 0.05, 50)
    close(v, 3.0, 1e-12, "minimum")
    close(x, 2.0, 1e-5, "argmin")


@check("Q13f", "a + b ≥ 2√(ab)", kind="spot-check", note="100 000 random triples")
def _():
    rng = random.Random(132)
    for _ in range(100_000):
        a, b, c = (rng.uniform(1e-3, 50) for _ in range(3))
        ensure((a + b) * (b + c) * (c + a) >= 8 * a * b * c * (1 - 1e-12), f"{a},{b},{c}")


# ======================================================================================
# Q14  Sums of squares
# ======================================================================================

@check("Q14a", "(a − b)² + (b − c)² + (c − a)² ≥ 0", kind="spot-check", note="100 000 random triples")
def _():
    rng = random.Random(141)
    for _ in range(100_000):
        a, b, c = (rng.uniform(-50, 50) for _ in range(3))
        ensure(a * a + b * b + c * c >= a * b + b * c + c * a - 1e-9, "inequality")
        close(2 * (a * a + b * b + c * c - a * b - b * c - c * a),
              (a - b) ** 2 + (b - c) ** 2 + (c - a) ** 2, 1e-9, "identity")


@check("Q14b", "S ≥ 3", "P ≤ 3", kind="spot-check", note="100 000 random triples with a + b + c = 3")
def _():
    rng = random.Random(142)
    for _ in range(100_000):
        a, b = rng.uniform(-20, 20), rng.uniform(-20, 20)
        c = 3 - a - b
        ensure(a * a + b * b + c * c >= 3 - 1e-9 and a * b + b * c + c * a <= 3 + 1e-9, f"{a},{b}")


def simplex_points(rng, n):
    for _ in range(n):
        u, v = sorted((rng.random(), rng.random()))
        x, y, z = u, v - u, 1 - v
        if min(x, y, z) > 1e-9:
            yield x, y, z


@check("Q14c", "(1/6, 1/3, 1/2)", "6 + 12 + 18 = 36", "The minimum is 36", kind="numeric",
       note="exact value at the claimed point; 300 000 random points of the simplex and a local search")
def _():
    f = lambda x, y, z: 1 / x + 4 / y + 9 / z
    ensure(1 / Fr(1, 6) + 4 / Fr(1, 3) + 9 / Fr(1, 2) == 36, "value at claimed point")
    rng = random.Random(143)
    best = min(f(*p) for p in simplex_points(rng, 300_000))
    ensure(best >= 36 - 1e-9, f"found {best} < 36")
    # local search from random starts converges to 36
    x, y = 0.3, 0.3
    step = 0.05
    while step > 1e-12:
        moved = False
        for dx, dy in ((step, 0), (-step, 0), (0, step), (0, -step), (step, -step), (-step, step)):
            nx, ny = x + dx, y + dy
            if nx > 0 and ny > 0 and nx + ny < 1 and f(nx, ny, 1 - nx - ny) < f(x, y, 1 - x - y):
                x, y, moved = nx, ny, True
        if not moved:
            step /= 2
    close(f(x, y, 1 - x - y), 36.0, 1e-9, "local search")
    close(x, 1 / 6, 1e-5, "x")
    close(y, 1 / 3, 1e-5, "y")


@check("Q14f", "1/432", kind="numeric", note="exact value at the claimed point; 300 000 random points")
def _():
    ensure(Fr(1, 6) * Fr(1, 3) ** 2 * Fr(1, 2) ** 3 == Fr(1, 432), "value")
    rng = random.Random(144)
    best = max(x * y * y * z ** 3 for x, y, z in simplex_points(rng, 300_000))
    ensure(best <= 1 / 432 + 1e-15, f"found {best} > 1/432")
    ensure(best > 1 / 432 * 0.995, "random search should get close")


# ======================================================================================
# Q15  (1 + 1/n)^n
# ======================================================================================

def a_seq(n: int) -> float:
    return math.exp(n * math.log1p(1 / n))


@check("Q15a", "a_n ≥ 1 + 1 = 2", kind="spot-check", note="Bernoulli for 20 000 random (x, n); a_n ≥ 2 for n ≤ 10^4")
def _():
    rng = random.Random(151)
    for _ in range(20_000):
        x, n = rng.uniform(-1, 3), rng.randint(1, 60)
        ensure((1 + x) ** n >= 1 + n * x - 1e-9 * max(1, abs(1 + n * x)), f"x={x} n={n}")
    ensure(all(a_seq(n) >= 2 - 1e-15 for n in range(1, 10_001)), "a_n ≥ 2")


@check("Q15b", "1 + 2 − 1/2^{n−1} < 3", kind="spot-check",
       note="term bound C(n,k)/n^k ≤ 1/k! ≤ 1/2^(k−1) checked exactly for n ≤ 40; a_n < 3 for n ≤ 10^5")
def _():
    for n in range(1, 41):
        for k in range(1, n + 1):
            t = Fr(math.comb(n, k), n ** k)
            ensure(t <= Fr(1, math.factorial(k)) <= Fr(1, 2 ** (k - 1)), f"n={n} k={k}")
    ensure(all(a_seq(n) < 3 for n in range(1, 100_001)), "a_n < 3")


@check("Q15c", "a_{n+1} > a_n", "e ≈ 2.718", kind="spot-check",
       note="exact comparison for n ≤ 80, floating point for n ≤ 10^5, limit numerically")
def _():
    prev = Fr(2)
    for n in range(2, 81):
        cur = Fr(n + 1, n) ** n
        ensure(cur > prev, f"exact n={n}")
        prev = cur
    vals = [a_seq(n) for n in range(1, 100_001)]
    ensure(all(b > a for a, b in zip(vals, vals[1:])), "float monotonicity")
    close(a_seq(10 ** 12), math.e, 1e-9, "limit")
    close(round(math.e, 3), 2.718, 1e-12, "rounding")


@check("Q15f", "≈ 2.7071 > 2.7", kind="exact")
def _():
    first5 = sum(Fr(math.comb(1000, k), 1000 ** k) for k in range(5))
    ensure(first5 > Fr(27, 10), "first five terms")
    close(round(float(first5), 4), 2.7071, 1e-12, "value of first five terms")
    ensure(Fr(1001, 1000) ** 1000 > Fr(27, 10), "exact power")


# ======================================================================================
# Q16  Additive functions
# ======================================================================================

NOT_CHECKABLE["Q16a"] = ("pure deduction from the functional equation (substituting x = y = 0 and "
                         "y = −x); there is no numerical object to test")


@check("Q16b", "f(p/q) = c × p/q", kind="spot-check",
       note="f(x) = cx satisfies the equation for random rational c, x, y; that no other "
            "solution exists is a proof")
def _():
    rng = random.Random(161)
    for _ in range(5000):
        c, x, y = rand_frac(rng), rand_frac(rng), rand_frac(rng)
        ensure(c * (x + y) == c * x + c * y, "additivity")


@check("Q16c", "f(x) = x²/2 + cx", kind="spot-check",
       note="every f(x) = x²/2 + cx satisfies the equation exactly (random rationals); "
            "that no other solution exists is a proof")
def _():
    rng = random.Random(162)
    for _ in range(5000):
        c, x, y = rand_frac(rng), rand_frac(rng), rand_frac(rng)
        f = lambda t: t * t / 2 + c * t
        ensure(f(x + y) == f(x) + f(y) + x * y, "equation")


@check("Q16f", "f(10) = 120")
def _():
    # derived from the equation alone: f(0) = 0 and f(n + 1) = f(n) + f(1) + 2n
    f = {0: 0, 1: 3}
    for n in range(1, 10):
        f[n + 1] = f[n] + f[1] + 2 * n
    ensure(f[10] == 120, str(f[10]))
    ensure(all(f[n] == n * n + 2 * n for n in f), "closed form")


# ======================================================================================
# Q17  Substitution
# ======================================================================================

@check("Q17a", "f(x) = (x² − 4x + 2)/3")
def _():
    rng = random.Random(171)
    for _ in range(500):
        x = rand_frac(rng)
        # solve the 2×2 system for (f(x), f(1−x)) independently
        fx, _f1 = solve_linear([[1, 2], [2, 1]], [x * x, (1 - x) ** 2])
        ensure(fx == (x * x - 4 * x + 2) / 3, f"x={x}")


@check("Q17b", "f(x) = 2/x − x", "x = ±√2", kind="numeric")
def _():
    rng = random.Random(172)
    for _ in range(500):
        x = rand_frac(rng)
        if x == 0:
            continue
        fx, _ = solve_linear([[1, 2], [2, 1]], [3 * x, 3 / x])
        ensure(fx == 2 / x - x, f"x={x}")
    f = lambda x: 2 / x - x
    h = lambda x: f(x) - f(-x)
    roots = [bisect_root(h, 0.5, 3), bisect_root(h, -3, -0.5)]
    close(roots[0], math.sqrt(2), 1e-12, "positive root")
    close(roots[1], -math.sqrt(2), 1e-12, "negative root")
    ensure(count_solutions(h, 1e-3, 50) == 1 and count_solutions(h, -50, -1e-3) == 1, "only ±√2")


@check("Q17c", "f(x) = ½(x + 1/x + 1/(1 − x))")
def _():
    rng = random.Random(173)
    g = lambda x: (x - 1) / x
    for _ in range(500):
        x = rand_frac(rng)
        if x in (0, 1):
            continue
        gx, ggx = g(x), g(g(x))
        ensure(g(ggx) == x, "order 3")
        A, _, _ = solve_linear([[1, 1, 0], [0, 1, 1], [1, 0, 1]], [1 + x, 1 + gx, 1 + ggx])
        ensure(A == (x + 1 / x + 1 / (1 - x)) / 2, f"x={x}")


@check("Q17f", "f(x) = 1 for all x")
def _():
    rng = random.Random(174)
    for _ in range(500):
        x = rand_frac(rng)
        fx, fmx = solve_linear([[1, x], [-x, 1]], [x + 1, -x + 1])  # unknowns f(x), f(−x)
        ensure(fx == 1 and fmx == 1, f"x={x}")


# ======================================================================================
# Q18  f(f(n)) = 3n
# ======================================================================================

def tripling_solutions(M: int) -> list[dict[int, int]]:
    """Exhaustive search: every strictly increasing f on {1..M} with f(f(n)) = 3n for all
    n ≤ M. Values may exceed M (those are kept as forced points). Uses only the necessary
    conditions n ≤ f(n) ≤ f(f(n)) = 3n and strict increase."""
    known: dict[int, int] = {}
    sols: list[dict[int, int]] = []

    def consistent() -> bool:
        items = sorted(known.items())
        for p, v in items:
            if not (p <= v <= 3 * p):
                return False
        for (p1, v1), (p2, v2) in zip(items, items[1:]):
            if v2 - v1 < p2 - p1:
                return False
        return True

    def impose(n: int) -> list[int] | None:
        """Enforce f(f(n)) = 3n; return the list of newly set points (for undo) or None."""
        m = known[n]
        if m in known:
            return [] if known[m] == 3 * n else None
        known[m] = 3 * n
        if not consistent():
            del known[m]
            return None
        return [m]

    def dfs(n: int) -> None:
        if n > M:
            sols.append({k: known[k] for k in range(1, M + 1)})
            return
        if n in known:
            added = impose(n)
            if added is not None:
                dfs(n + 1)
                for k in added:
                    del known[k]
            return
        for v in range(n, 3 * n + 1):
            known[n] = v
            if consistent():
                added = impose(n)
                if added is not None:
                    dfs(n + 1)
                    for k in added:
                        del known[k]
            del known[n]

    dfs(1)
    return sols


@lru_cache(maxsize=None)
def _tripling162():
    return tripling_solutions(162)


def f_tripling(n: int) -> int:
    k = 0
    while 3 ** (k + 1) <= n:
        k += 1
    return n + 3 ** k if n <= 2 * 3 ** k else 3 * n - 3 ** (k + 1)


@check("Q18a", "f(1) = 2, and f(2) = f(f(1)) = 3",
       note="exhaustive search over all candidate functions on {1..162}")
def _():
    sols = _tripling162()
    ensure(len(sols) >= 1, "no solution found")
    ensure({(s[1], s[2]) for s in sols} == {(2, 3)}, "f(1), f(2)")


@check("Q18b", "f(3n) = f(f(f(n))) = 3f(n)", "6, 7, 8, 9, 12, 15, 18",
       note="exhaustive search over all candidate functions on {1..162}")
def _():
    sols = _tripling162()
    ensure({tuple(s[n] for n in range(3, 10)) for s in sols} == {(6, 7, 8, 9, 12, 15, 18)}, "values")
    for s in sols:
        ensure(all(s[3 * n] == 3 * s[n] for n in range(1, 55)), "f(3n) = 3f(n)")


@check("Q18c", "f(100) = f(81 + 19) = 162 + 19 = 181",
       note="exhaustive search shows f(100) is forced; formula verified for n ≤ 10^5")
def _():
    sols = _tripling162()
    ensure({s[100] for s in sols} == {181}, f"f(100) values {sorted({s[100] for s in sols})}")
    ensure(len(sols) == 1, f"{len(sols)} solutions on 1..162")
    ensure(all(sols[0][n] == f_tripling(n) for n in range(1, 163)), "formula on 1..162")
    prev = 0
    for n in range(1, 100_001):
        v = f_tripling(n)
        ensure(v > prev and f_tripling(v) == 3 * n, f"formula fails at n={n}")
        prev = v


@check("Q18f", "power of 3", note="from the forced values on 1..162 and the formula up to 10^5")
def _():
    s = _tripling162()[0]
    ensure([n for n in range(1, 163) if s[n] == 2 * n] == [1, 3, 9, 27, 81], "on 1..162")
    powers = {3 ** k for k in range(12)}
    for n in range(1, 100_001):
        ensure((f_tripling(n) == 2 * n) == (n in powers), f"n={n}")


# ======================================================================================
# Q19  Parabola tangents
# ======================================================================================

def tangent_meet(p, q):
    # tangent at t: y = 2t x − t² ; intersect numerically by solving the 2×2 system
    a1, b1, c1 = 2 * p, -1.0, p * p     # 2p x − y = p²
    a2, b2, c2 = 2 * q, -1.0, q * q
    det = a1 * b2 - a2 * b1
    return ((c1 * b2 - c2 * b1) / det, (a1 * c2 - a2 * c1) / det)


@check("Q19a", "y = 2px − p²", "x = (p + q)/2 and y = p(p + q) − p² = pq", kind="numeric")
def _():
    rng = random.Random(191)
    for _ in range(2000):
        p, q = rng.uniform(-5, 5), rng.uniform(-5, 5)
        if abs(p - q) < 1e-3:
            continue
        h = 1e-6  # tangent gradient by finite differences
        close(((p + h) ** 2 - (p - h) ** 2) / (2 * h), 2 * p, 1e-6, "gradient")
        x, y = tangent_meet(p, q)
        close(x, (p + q) / 2, 1e-9, "x")
        close(y, p * q, 1e-9, "y")


@check("Q19b", "pq = −1/4", "y = −1/4", kind="numeric")
def _():
    rng = random.Random(192)
    for _ in range(2000):
        p = rng.uniform(0.05, 5) * rng.choice((-1, 1))
        q = -1 / (4 * p)
        close((2 * p) * (2 * q), -1.0, 1e-12, "perpendicular")
        close(tangent_meet(p, q)[1], -0.25, 1e-9, "R on directrix")
        q2 = q + rng.uniform(0.1, 1)  # any other q gives non-perpendicular tangents
        ensure(abs(4 * p * q2 + 1) > 1e-6, "converse")


@check("Q19c", "|q − p|³/4", "(q − p)³/6", "2/3 of triangle PQR", kind="numeric")
def _():
    rng = random.Random(193)
    for _ in range(300):
        p, q = sorted((rng.uniform(-4, 4), rng.uniform(-4, 4)))
        if q - p < 1e-2:
            continue
        (px, py), (qx, qy), (rx, ry) = (p, p * p), (q, q * q), ((p + q) / 2, p * q)
        area = abs((qx - px) * (ry - py) - (rx - px) * (qy - py)) / 2
        close(area, (q - p) ** 3 / 4, 1e-9, "triangle")
        seg = simpson(lambda x: (p + q) * x - p * q - x * x, p, q, 200)
        close(seg, (q - p) ** 3 / 6, 1e-9, "segment")
        close(seg / area, 2 / 3, 1e-9, "ratio")


@check("Q19f", "pq = −1/4", kind="numeric")
def _():
    rng = random.Random(194)
    for _ in range(2000):
        p = rng.uniform(0.05, 5) * rng.choice((-1, 1))
        q = -1 / (4 * p)
        close((p + q) * 0 - p * q, 0.25, 1e-12, "chord through focus")
        close(tangent_meet(p, q)[1], -0.25, 1e-9, "R")


# ======================================================================================
# Q20  Apollonius circles
# ======================================================================================

def dist_point_line(x0, y0, a, b, c):  # line ax + by + c = 0
    return abs(a * x0 + b * y0 + c) / math.hypot(a, b)


@check("Q20a", "(x − 4)² + y² = 4", kind="numeric")
def _():
    rng = random.Random(201)
    for _ in range(2000):
        th = rng.uniform(0, 2 * math.pi)
        x, y = 4 + 2 * math.cos(th), 2 * math.sin(th)
        close(math.hypot(x, y), 2 * math.hypot(x - 3, y), 1e-9, "on circle")
        x, y = rng.uniform(-10, 10), rng.uniform(-10, 10)
        on = abs((x - 4) ** 2 + y ** 2 - 4) < 1e-9
        ensure(on == (abs(math.hypot(x, y) - 2 * math.hypot(x - 3, y)) < 1e-9), "off circle")


@check("Q20b", "y = ±x/√3", "60°", kind="numeric")
def _():
    for s in (1, -1):  # line y = s x/√3  ->  s x − √3 y = 0
        close(dist_point_line(4, 0, s, -math.sqrt(3), 0), 2.0, 1e-12, "tangent")
    close(math.degrees(2 * math.atan(1 / math.sqrt(3))), 60.0, 1e-12, "angle")
    # numerically: the tangent directions from O are where the distance from (4,0) equals 2
    g = lambda phi: dist_point_line(4, 0, math.sin(phi), -math.cos(phi), 0) - 2
    phi = bisect_root(g, 0.01, math.pi / 2 - 0.01)
    close(math.degrees(2 * phi), 60.0, 1e-9, "angle from search")


@check("Q20c", "four common tangents", "y = ±(x + 4)/√15", "y = ±(3x − 4)/√7", kind="numeric",
       note="all common tangents found by a numerical search over normal directions")
def _():
    claimed = []
    for s in (1, -1):
        claimed.append((s / math.sqrt(15), s * 4 / math.sqrt(15)))     # y = m x + c
        claimed.append((s * 3 / math.sqrt(7), -s * 4 / math.sqrt(7)))
    for m, c in claimed:
        close(dist_point_line(0, 0, m, -1, c), 1.0, 1e-12, "circle 1")
        close(dist_point_line(4, 0, m, -1, c), 2.0, 1e-12, "circle 2")
    # independent search: lines x cos φ + y sin φ = 1 are exactly the tangents of circle 1
    g = lambda phi: abs(4 * math.cos(phi) - 1) - 2
    found = []
    n = 100_000
    for i in range(n):
        a, b = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        if g(a) * g(b) < 0:
            found.append(bisect_root(g, a, b))
    ensure(len(found) == 4, f"{len(found)} common tangents")
    for phi in found:  # convert to y = m x + c and match a claimed line
        m, c = -math.cos(phi) / math.sin(phi), 1 / math.sin(phi)
        ensure(any(abs(m - m2) < 1e-9 and abs(c - c2) < 1e-9 for m2, c2 in claimed), f"φ={phi}")


@check("Q20f", "Centre (3k²/(k² − 1), 0) and radius 3k/|k² − 1|", "x = 3/2", kind="numeric")
def _():
    rng = random.Random(202)
    for k in (0.3, 0.5, 2, 3, 7.5):
        cx, r = 3 * k * k / (k * k - 1), 3 * k / abs(k * k - 1)
        for _ in range(200):
            th = rng.uniform(0, 2 * math.pi)
            x, y = cx + r * math.cos(th), r * math.sin(th)
            close(math.hypot(x, y), k * math.hypot(x - 3, y), 1e-9, f"k={k}")
    for y in (-5, 0, 2.5):
        close(math.hypot(1.5, y), math.hypot(1.5 - 3, y), 1e-12, "k=1")


# ======================================================================================
# Q21  Projectiles
# ======================================================================================

U, G = 12.0, 9.81


def flight_hit_line(theta: float, slope: float) -> float:
    """Distance along the line y = x tan(slope) at which the projectile lands, found by
    bisection on the kinematic equations (not on any range formula)."""
    vx, vy = U * math.cos(theta), U * math.sin(theta)
    t_s = math.tan(slope)
    h = lambda t: (vy * t - G * t * t / 2) - (vx * t) * t_s
    T = 1.0
    while h(T) > 0:
        T *= 2
    t = bisect_root(h, 1e-9 if h(1e-9) > 0 else 1e-6, T)
    return vx * t / math.cos(slope)


@check("Q21a", "u² sin 2θ/g", "θ = 45°", "u²/g", kind="numeric")
def _():
    for th in (0.2, 0.5, 0.9, 1.3):
        close(flight_hit_line(th, 0), U * U * math.sin(2 * th) / G, 1e-9, f"range θ={th}")
    th, R = golden(lambda t: flight_hit_line(t, 0), 0.01, math.pi / 2 - 0.01, maximise=True)
    close(math.degrees(th), 45.0, 1e-5, "best angle")
    close(R, U * U / G, 1e-10, "max range")


@check("Q21b", "Y ≤ u²/(2g) − gX²/(2u²)", kind="numeric",
       note="highest reachable point above each X found by optimising over θ")
def _():
    for X in (0.5, 3, 7, 11, 14):
        height = lambda th: X * math.tan(th) - G * X * X / (2 * U * U * math.cos(th) ** 2)
        _, ymax = golden(height, -math.pi / 2 + 1e-6, math.pi / 2 - 1e-6, maximise=True)
        close(ymax, U * U / (2 * G) - G * X * X / (2 * U * U), 1e-9, f"X={X}")


@check("Q21c", "u²/(g(1 + sin α))", kind="numeric")
def _():
    for a in (0.0, 0.2, 0.5, 0.9):
        _, R = golden(lambda t: flight_hit_line(t, a), a + 1e-3, math.pi / 2 - 1e-3, maximise=True)
        close(R, U * U / (G * (1 + math.sin(a))), 1e-9, f"α={a}")


@check("Q21f", "u²/(g(1 − sin α))", "θ = 45° − α/2", "θ = 45° + α/2", kind="numeric")
def _():
    for a in (0.2, 0.5, 0.9):
        th, R = golden(lambda t: flight_hit_line(t, -a), -a + 1e-3, math.pi / 2 - 1e-3, maximise=True)
        close(R, U * U / (G * (1 - math.sin(a))), 1e-9, f"down α={a}")
        close(th, math.pi / 4 - a / 2, 1e-5, f"down angle α={a}")
        th, _ = golden(lambda t: flight_hit_line(t, a), a + 1e-3, math.pi / 2 - 1e-3, maximise=True)
        close(th, math.pi / 4 + a / 2, 1e-5, f"up angle α={a}")


# ======================================================================================
# Q22  Bouncing ball: time-stepping simulation
# ======================================================================================

def bounce_sim(h: float, e: float, g: float, dt: float = 1e-3):
    """Step the motion with exact constant-acceleration updates, resolving each impact inside
    its step. Returns (height after first bounce, total distance, total time)."""
    y, v, t, dist = h, 0.0, 0.0, 0.0
    bounces, peak1 = 0, 0.0
    while True:
        y_new = y + v * dt - g * dt * dt / 2
        if y_new > 0:
            # distance in this step (allow for the turning point inside the step)
            v_new = v - g * dt
            if v > 0 > v_new:
                ytop = y + v * v / (2 * g)  # apex inside this step
                dist += (ytop - y) + (ytop - y_new)
                if bounces == 1:
                    peak1 = max(peak1, ytop)
            else:
                dist += abs(y_new - y)
            y, v, t = y_new, v_new, t + dt
        else:
            tau = (v + math.sqrt(v * v + 2 * g * y)) / g  # time to reach the floor
            if v > 0:
                ytop = y + v * v / (2 * g)
                dist += (ytop - y) + ytop
                if bounces == 1:
                    peak1 = max(peak1, ytop)
            else:
                dist += y
            vimp = v - g * tau
            t += tau
            y, v = 0.0, -e * vimp
            bounces += 1
            if v < 1e-9:
                return peak1, dist, t


@check("Q22a", "e²h", kind="numeric")
def _():
    for h, e in ((1.25, 0.5), (2.0, 0.8), (0.7, 0.3)):
        peak, _, _ = bounce_sim(h, e, 10.0, 1e-5)
        close(peak, e * e * h, 1e-6, f"h={h} e={e}")


@check("Q22b", "h(1 + e²)/(1 − e²)", "25/12 ≈ 2.08 m", kind="numeric")
def _():
    for h, e in ((1.25, 0.5), (2.0, 0.8), (0.7, 0.3)):
        _, d, _ = bounce_sim(h, e, 10.0)
        close(d, h * (1 + e * e) / (1 - e * e), 1e-7, f"h={h} e={e}")
    close(bounce_sim(1.25, 0.5, 10.0)[1], 25 / 12, 1e-7, "numbers")


@check("Q22c", "√(2h/g) × (1 + e)/(1 − e)", "0.5 × 3 = 1.5 s", kind="numeric")
def _():
    for h, e in ((1.25, 0.5), (2.0, 0.8), (0.7, 0.3)):
        _, _, T = bounce_sim(h, e, 10.0)
        close(T, math.sqrt(2 * h / 10.0) * (1 + e) / (1 - e), 1e-7, f"h={h} e={e}")
    close(bounce_sim(1.25, 0.5, 10.0)[2], 1.5, 1e-7, "numbers")


@check("Q22f", "25/18 ≈ 1.39", kind="numeric")
def _():
    _, d, T = bounce_sim(1.25, 0.5, 10.0)
    close(d / T, 25 / 18, 1e-7, "average speed")


# ======================================================================================
# Q23  Ladder (linear feasibility in the unknown wall reaction)
# ======================================================================================

def ladder_ok(theta: float, mu: float, mu_w: float, loads: list[tuple[float, float]]) -> bool:
    """Can the ladder rest at angle θ? loads = [(weight, distance along ladder / L)].
    Unknown S ≥ 0 (wall normal); then G = M − S tan θ (wall friction, up), R = W − G,
    F = S. Requires F ≤ μR, |G| ≤ μ_w S, R ≥ 0. Each is linear in S."""
    W = sum(w for w, _ in loads)
    M = sum(w * d for w, d in loads)
    t = math.tan(theta)
    lo, hi = 0.0, math.inf
    for a, b in ((1 - mu * t, mu * (W - M)),   # S ≤ μ(W − M + S t)
                 (-(t + mu_w), -M),            # M − S t ≤ μ_w S
                 (t - mu_w, M),                # S t − M ≤ μ_w S
                 (-t, W - M)):                 # R ≥ 0
        if abs(a) < 1e-15:
            if b < -1e-12:
                return False
        elif a > 0:
            hi = min(hi, b / a)
        else:
            lo = max(lo, b / a)
    return lo <= hi + 1e-12 * max(1.0, abs(hi) if hi < math.inf else 1.0)


def least_angle(mu, mu_w, loads=((1.0, 0.5),)):
    loads = list(loads)
    lo, hi = 1e-9, math.pi / 2 - 1e-9
    if ladder_ok(lo, mu, mu_w, loads):
        return 0.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if ladder_ok(mid, mu, mu_w, loads):
            hi = mid
        else:
            lo = mid
    return hi


@check("Q23a", "tan θ ≥ 1/(2μ)", kind="numeric")
def _():
    for mu in (0.2, 0.5, 0.75, 1.3):
        close(math.tan(least_angle(mu, 0.0)), 1 / (2 * mu), 1e-9, f"μ={mu}")


@check("Q23b", "d ≤ 5L/6", kind="numeric")
def _():
    theta = math.atan(4 / 3)
    lo, hi = 0.0, 1.0
    ensure(ladder_ok(theta, 0.5, 0.0, [(1, 0.5), (1, 0.0)]), "foot")
    ensure(not ladder_ok(theta, 0.5, 0.0, [(1, 0.5), (1, 1.0)]), "top")
    for _ in range(200):
        mid = (lo + hi) / 2
        if ladder_ok(theta, 0.5, 0.0, [(1, 0.5), (1, mid)]):
            lo = mid
        else:
            hi = mid
    close(lo, 5 / 6, 1e-9, "max d / L")


@check("Q23c", "tan θ = (1 − μμ')/(2μ)", "tan θ = 5/6, θ ≈ 39.8°", kind="numeric")
def _():
    for mu, mw in ((0.5, 1 / 3), (0.3, 0.2), (0.8, 0.5), (0.25, 0.0), (0.6, 1.2)):
        close(math.tan(least_angle(mu, mw)), (1 - mu * mw) / (2 * mu), 1e-8, f"μ={mu}, μ'={mw}")
    th = least_angle(0.5, 1 / 3)
    close(math.tan(th), 5 / 6, 1e-8, "example")
    close(round(math.degrees(th), 1), 39.8, 1e-9, "degrees")


@check("Q23f", "any angle", kind="numeric")
def _():
    for mu, mw in ((2.0, 0.5), (1.5, 1.0), (1.0, 3.0)):
        for th in (1e-4, 0.01, 0.3, 1.2):
            ensure(ladder_ok(th, mu, mw, [(1.0, 0.5)]), f"μ={mu} μ'={mw} θ={th}")
    ensure(not ladder_ok(0.01, 0.9, 1.0, [(1.0, 0.5)]), "μμ' < 1 does slip at shallow angles")


# ======================================================================================
# Q24  Fifth roots of unity
# ======================================================================================

W5 = cmath.exp(2j * math.pi / 5)


@check("Q24a", "1 + ω + ω² + ω³ + ω⁴", kind="numeric")
def _():
    cclose(sum(W5 ** k for k in range(5)), 0, 1e-14, "sum")


@check("Q24b", "cos(2π/5) = (√5 − 1)/4 ≈ 0.309", kind="numeric")
def _():
    c = math.cos(2 * math.pi / 5)
    close(c, (math.sqrt(5) - 1) / 4, 1e-15, "value")
    close(4 * c * c + 2 * c - 1, 0.0, 1e-14, "quadratic")
    close(round(c, 3), 0.309, 1e-12, "rounding")


@check("Q24c", "is 1 + 1 + 1 + 1 + 1 = 5", "5/16", kind="numeric")
def _():
    p = 1 + 0j
    for k in range(1, 5):
        p *= 1 - W5 ** k
    cclose(p, 5, 1e-13, "product")
    close(math.prod(math.sin(k * math.pi / 5) for k in range(1, 5)), 5 / 16, 1e-14, "sines")


@check("Q24f", "Π_{k=1}^{n−1} sin(kπ/n) = n/2^{n−1}", kind="numeric")
def _():
    for n in range(2, 40):
        close(math.prod(math.sin(k * math.pi / n) for k in range(1, n)), n / 2 ** (n - 1), 1e-12, f"n={n}")


# ======================================================================================
# Q25  Equilateral triangles
# ======================================================================================

def is_equilateral(z1, z2, z3, tol=1e-9):
    a, b, c = abs(z2 - z1), abs(z3 - z2), abs(z1 - z3)
    return abs(a - b) < tol * max(1, a) and abs(b - c) < tol * max(1, a)


def signed_area(z1, z2, z3):
    return ((z2 - z1).conjugate() * (z3 - z1)).imag / 2


@check("Q25a", "z_3 − z_1 = e^{iπ/3}(z_2 − z_1)", kind="spot-check",
       note="random triangles: the rotation gives anticlockwise equilateral triangles, and "
            "anticlockwise equilateral triangles satisfy it")
def _():
    rng = random.Random(251)
    rot = cmath.exp(1j * math.pi / 3)
    for _ in range(5000):
        z1, z2 = complex(rng.uniform(-5, 5), rng.uniform(-5, 5)), complex(rng.uniform(-5, 5), rng.uniform(-5, 5))
        z3 = z1 + rot * (z2 - z1)
        ensure(is_equilateral(z1, z2, z3) and signed_area(z1, z2, z3) > 0, "forward")
        z3c = z1 + rot.conjugate() * (z2 - z1)  # clockwise one does not satisfy the relation
        ensure(signed_area(z1, z2, z3c) < 0 and abs(z3c - z1 - rot * (z2 - z1)) > 1e-9, "orientation")


@check("Q25b", "z = (1 − √3)/2 + i(1 + √3)/2 or z = (1 + √3)/2 + i(1 − √3)/2", kind="numeric")
def _():
    s = math.sqrt(3)
    for z in (complex((1 - s) / 2, (1 + s) / 2), complex((1 + s) / 2, (1 - s) / 2)):
        ensure(is_equilateral(0, 1 + 1j, z), f"{z}")
    # independently: intersect circles |z| = |z − (1+i)| = √2 numerically
    found = []
    n = 200_000
    g = lambda th: abs(math.sqrt(2) * cmath.exp(1j * th) - (1 + 1j)) - math.sqrt(2)
    for i in range(n):
        a, b = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        if g(a) * g(b) < 0:
            found.append(math.sqrt(2) * cmath.exp(1j * bisect_root(g, a, b)))
    ensure(len(found) == 2, f"{len(found)} third vertices")
    want = sorted([complex((1 - s) / 2, (1 + s) / 2), complex((1 + s) / 2, (1 - s) / 2)], key=lambda z: z.real)
    for f, w in zip(sorted(found, key=lambda z: z.real), want):
        cclose(f, w, 1e-9, "third vertex")


@check("Q25c", "z_1² + z_2² + z_3² − z_1z_2 − z_2z_3 − z_3z_1", kind="spot-check",
       note="identity checked for random triangles of both orientations, and random "
            "non-equilateral triangles fail it")
def _():
    rng = random.Random(252)
    w = cmath.exp(2j * math.pi / 3)
    rot = cmath.exp(1j * math.pi / 3)
    Q = lambda a, b, c: a * a + b * b + c * c - a * b - b * c - c * a
    for _ in range(5000):
        z1, z2 = complex(rng.uniform(-5, 5), rng.uniform(-5, 5)), complex(rng.uniform(-5, 5), rng.uniform(-5, 5))
        z3 = complex(rng.uniform(-5, 5), rng.uniform(-5, 5))
        cclose((z1 + w * z2 + w * w * z3) * (z1 + w * w * z2 + w * z3), Q(z1, z2, z3), 1e-9, "product")
        for r in (rot, rot.conjugate()):
            t = z1 + r * (z2 - z1)
            cclose(Q(z1, z2, t), 0, 1e-9, "equilateral ⇒ 0")
        if not is_equilateral(z1, z2, z3, 1e-3):
            ensure(abs(Q(z1, z2, z3)) > 1e-9, "non-equilateral ⇒ nonzero")


@check("Q25f", "(z − 1)³ = 8", "3√3", kind="numeric")
def _():
    r = poly_roots([1, -3, 3, -9])
    ensure(is_equilateral(*r), "equilateral")
    for z in r:
        close(abs(z - 1), 2.0, 1e-12, "circumradius")
        close(abs(z - 1) ** 3, 8.0, 1e-12, "(z − 1)³ = 8")
    close(abs(signed_area(*r)), 3 * math.sqrt(3), 1e-12, "area")


# ======================================================================================
# Q26  Binomial sums
# ======================================================================================

@check("Q26a", "e^{i(n+1)θ/2} sin(nθ/2)/sin(θ/2)", kind="numeric", note="1000 random (n, θ)")
def _():
    rng = random.Random(261)
    for _ in range(1000):
        n, th = rng.randint(1, 60), rng.uniform(0.01, 2 * math.pi - 0.01)
        close(sum(math.cos(k * th) for k in range(1, n + 1)),
              math.sin(n * th / 2) * math.cos((n + 1) * th / 2) / math.sin(th / 2), 1e-9, f"n={n} θ={th}")


@check("Q26b", "2^n cos^n(θ/2) cos(nθ/2)", kind="numeric", note="1000 random (n, θ)")
def _():
    rng = random.Random(262)
    for _ in range(1000):
        n, th = rng.randint(0, 40), rng.uniform(-7, 7)
        lhs = sum(math.comb(n, k) * math.cos(k * th) for k in range(n + 1))
        rhs = 2 ** n * math.cos(th / 2) ** n * math.cos(n * th / 2)
        # terms are as large as C(n, n/2), so allow for cancellation: tolerance relative to 2^n
        ensure(abs(lhs - rhs) <= 1e-12 * 2 ** n, f"n={n} θ={th}: {lhs} vs {rhs}")


@check("Q26c", "2^n + 2cos(nπ/3)", "(1024 − 1)/3 = 341")
def _():
    two_cos = [2, 1, -1, -2, -1, 1]  # 2cos(nπ/3) for n mod 6
    for n in range(0, 120):
        s = sum(math.comb(n, k) for k in range(0, n + 1, 3))
        ensure(3 * s == 2 ** n + two_cos[n % 6], f"n={n}")
        close(2 * math.cos(n * math.pi / 3), two_cos[n % 6], 1e-9, "cos table")
    ensure(sum(math.comb(10, k) for k in range(0, 11, 3)) == 341, "n=10")


@check("Q26f", "256", "(1 + i)^10 + 0^10 + (1 − i)^10")
def _():
    ensure(math.comb(10, 0) + math.comb(10, 4) + math.comb(10, 8) == 256, "direct")
    cclose((2 ** 10 + (1 + 1j) ** 10 + 0 + (1 - 1j) ** 10) / 4, 256, 1e-12, "roots of unity")
    cclose((1 + 1j) ** 10, 32j, 1e-12, "(1+i)^10")


# ======================================================================================
# Q27  Logistic growth with harvesting (RK4)
# ======================================================================================

@check("Q27a", "P = 1/(1 + 3e^{−t})", "t = ln 3 ≈ 1.10", kind="numeric")
def _():
    f = lambda t, P: P * (1 - P)
    for T in (0.5, 1.0, 3.0):
        close(rk4(f, 0, 0.25, T), 1 / (1 + 3 * math.exp(-T)), 1e-11, f"P({T})")
    close(rk4_hit(f, 0, 0.25, 0.5), math.log(3), 1e-9, "time to 1/2")


@check("Q27b", "h ≤ 1/4", "P = 1/4 and P = 3/4", "3/4 is stable and 1/4 is unstable", kind="numeric")
def _():
    for h in (0, 0.1, 0.2, 0.249, 0.25, 0.2501, 0.3, 1.0):
        has_eq = count_solutions(lambda P: P * (1 - P) - h, -2, 3) > 0
        ensure(has_eq == (h <= 0.25), f"h={h}")
    f = lambda t, P: P * (1 - P) - 3 / 16
    close(bisect_root(lambda P: f(0, P), 0, 0.5), 0.25, 1e-12, "lower equilibrium")
    close(bisect_root(lambda P: f(0, P), 0.5, 1), 0.75, 1e-12, "upper equilibrium")
    for P0 in (0.3, 0.6, 0.74, 0.76, 1.5):
        close(rk4(f, 0, P0, 60, 6000), 0.75, 1e-6, f"from {P0} → 3/4")
    ensure(rk4(f, 0, 0.26, 5) > 0.26 and rk4(f, 0, 0.24, 5) < 0.24, "1/4 unstable")


@check("Q27c", "t = 2 ln(5/3) ≈ 1.02", kind="numeric")
def _():
    f = lambda t, P: P * (1 - P) - 3 / 16
    t0 = rk4_hit(f, 0, 0.125, 0.0, h=1e-4)
    close(t0, 2 * math.log(5 / 3), 1e-9, "extinction time")
    close(round(2 * math.log(5 / 3), 2), 1.02, 1e-12, "rounding")


@check("Q27f", "P = (3 + e^{−t/2})/(4(1 + e^{−t/2}))", "tends to 3/4", kind="numeric")
def _():
    f = lambda t, P: P * (1 - P) - 3 / 16
    sol = lambda t: (3 + math.exp(-t / 2)) / (4 * (1 + math.exp(-t / 2)))
    for T in (0.5, 2, 6, 20):
        close(rk4(f, 0, 0.5, T), sol(T), 1e-11, f"P({T})")
    close(sol(80), 0.75, 1e-15, "limit")


# ======================================================================================
# Q28  Curves from tangent properties
# ======================================================================================

@check("Q28a", "y = Ax²", kind="numeric", note="property checked on y = Ax²; ODE solved numerically from random points")
def _():
    rng = random.Random(281)
    for _ in range(200):
        A, x = rng.uniform(-3, 3), rng.uniform(0.2, 5)
        if abs(A) < 0.05:
            continue
        y, yp = A * x * x, 2 * A * x
        close(x - y / yp, x / 2, 1e-12, "x-intercept")
    for x0, y0 in ((1, 2), (0.5, -1), (2, 0.3)):
        y = rk4(lambda x, y: 2 * y / x, x0, y0, 4.0)
        close(y, (y0 / x0 ** 2) * 16, 1e-9, "ODE")


@check("Q28b", "x² + y² = C", kind="numeric")
def _():
    rng = random.Random(282)
    for _ in range(200):
        r, th = rng.uniform(0.5, 5), rng.uniform(0.1, 1.4)
        x, y = r * math.cos(th), r * math.sin(th)
        yp = -x / y  # tangent slope of the circle by implicit differentiation
        # normal line through P: points P + s(−yp, 1)·... check it passes through O
        close(y - (-1 / yp) * x, 0.0, 1e-9, "normal through O")
    y = rk4(lambda x, y: -x / y, 0.5, 2.0, 1.5)
    close(1.5 ** 2 + y ** 2, 0.25 + 4.0, 1e-10, "ODE stays on circle")


@check("Q28c", "y = A/2 − x²/(2A)", kind="numeric",
       note="property checked on the parabolas; ODE y' = (y − √(x²+y²))/x solved numerically")
def _():
    rng = random.Random(283)
    for _ in range(200):
        A, x = rng.uniform(0.2, 5), rng.uniform(0.1, 5)
        y, yp = A / 2 - x * x / (2 * A), -x / A
        close(y - x * yp, math.hypot(x, y), 1e-12, "intercept = OP")
    ode = lambda x, y: (y - math.hypot(x, y)) / x
    for x0, y0 in ((1, 1), (0.5, -2), (2, 3)):
        A = y0 + math.hypot(x0, y0)
        y = rk4(ode, x0, y0, x0 + 2.0)
        close(y, A / 2 - (x0 + 2) ** 2 / (2 * A), 1e-9, "ODE")


@check("Q28f", "y = x²", kind="numeric")
def _():
    for X in (0.5, 1, 2.5, 4):
        close(simpson(lambda t: t * t, 0, X, 200), X * X * X / 3, 1e-12, f"area X={X}")
    close(rk4(lambda x, f: 2 * f / x, 1, 1, 3), 9.0, 1e-9, "ODE through (1,1)")


# ======================================================================================
# Q29  Symmetric functions
# ======================================================================================

@lru_cache(maxsize=None)
def _cubic_roots():
    return tuple(poly_roots([1, -2, 3, -4]))


@check("Q29a", "α + β + γ = 2, αβ + βγ + γα = 3 and αβγ = 4", "4 − 6 = −2", "one real root", kind="numeric")
def _():
    a, b, c = _cubic_roots()
    cclose(a + b + c, 2, 1e-12, "sum")
    cclose(a * b + b * c + c * a, 3, 1e-12, "pair sum")
    cclose(a * b * c, 4, 1e-12, "product")
    cclose(a * a + b * b + c * c, -2, 1e-12, "sum of squares")
    ensure(sum(abs(z.imag) < 1e-9 for z in (a, b, c)) == 1, "exactly one real root")


@check("Q29b", "−4 − 6 + 12 = 2", kind="numeric")
def _():
    cclose(sum(z ** 3 for z in _cubic_roots()), 2, 1e-12, "cubes")


@check("Q29c", "x³ − 3x² + 8x − 16 = 0", kind="numeric")
def _():
    a, b, c = _cubic_roots()
    want = [a * b, b * c, c * a]
    for g in poly_roots([1, -3, 8, -16]):  # match each root to the nearest unused target
        j = min(range(len(want)), key=lambda i: abs(want[i] - g))
        cclose(g, want.pop(j), 1e-9, "roots")


@check("Q29f", "= 18", kind="numeric")
def _():
    cclose(sum(z ** 4 for z in _cubic_roots()), 18, 1e-12, "fourth powers")


# ======================================================================================
# Q30  Remainders (exact polynomial long division)
# ======================================================================================

def xpow(n):
    return [1] + [0] * n


@check("Q30a", "The remainder is 1.")
def _():
    ensure(poly_rem(xpow(100), [1, 0, -1]) == [1], str(poly_rem(xpow(100), [1, 0, -1])))


@check("Q30b", "100x − 99")
def _():
    ensure(poly_rem(xpow(100), [1, -2, 1]) == [100, -99], "remainder")


@check("Q30c", "The remainder is x.")
def _():
    ensure(poly_rem(xpow(100), [1, 1, 1]) == [1, 0], "remainder")


@check("Q30f", "x². Write the remainder as ax² + bx + c")
def _():
    ensure(poly_rem(xpow(2026), [1, 0, -1, 0]) == [1, 0, 0], "remainder")


# ======================================================================================
# Q31  Integer polynomials
# ======================================================================================

def rand_intpoly(rng, deg=6, lim=20):
    return [rng.randint(-lim, lim) for _ in range(rng.randint(1, deg) + 1)]


def peval(c, x):
    v = 0
    for a in c:
        v = v * x + a
    return v


@check("Q31a", "divisible by a − b too", kind="spot-check", note="20 000 random integer polynomials and pairs")
def _():
    rng = random.Random(311)
    for _ in range(20_000):
        P = rand_intpoly(rng)
        a, b = rng.randint(-50, 50), rng.randint(-50, 50)
        if a != b:
            ensure((peval(P, a) - peval(P, b)) % (a - b) == 0, f"{P} {a} {b}")


@check("Q31b", "No.", "13 − 5 = 8")
def _():
    ensure((13 - 5) % (7 - 2) != 0, "5 divides 8?")


@check("Q31c", "never 0", kind="spot-check",
       note="5000 random integer polynomials with P(0), P(1) odd: P(n) odd for |n| ≤ 60")
def _():
    rng = random.Random(312)
    tested = 0
    while tested < 5000:
        P = rand_intpoly(rng)
        if peval(P, 0) % 2 == 1 and peval(P, 1) % 2 == 1:
            tested += 1
            ensure(all(peval(P, n) % 2 == 1 for n in range(-60, 61)), f"{P}")


@check("Q31f", "whose product is 9", kind="spot-check",
       note="exhaustive over 4-sets of distinct divisors of 3; plus 2000 random constructed P")
def _():
    divs = [d for d in range(-3, 4) if d != 0 and 3 % d == 0]
    for combo in itertools.combinations(divs, 4):
        prod = math.prod(combo)
        ensure(prod == 9 and 3 % prod != 0, f"{combo}")
    rng = random.Random(313)
    for _ in range(2000):
        roots = rng.sample(range(-15, 16), 4)
        Q = rand_intpoly(rng, 3, 5)
        for k in range(-40, 41):
            Pk = 5 + math.prod(k - r for r in roots) * peval(Q, k)
            ensure(Pk != 8, f"roots {roots}, Q {Q}, k {k}")


# ======================================================================================
# Q32  Induction
# ======================================================================================

@check("Q32a", "9(9^n + 7) − 56", kind="spot-check", note="checked for n ≤ 1000")
def _():
    ensure(all((9 ** n + 7) % 8 == 0 for n in range(1001)), "divisibility")
    ensure(all(9 ** (n + 1) + 7 == 9 * (9 ** n + 7) - 56 for n in range(50)), "identity")


@check("Q32b", "32 > 25", "(4 = 4, 8 < 9, 16 = 16)", kind="spot-check", note="checked for 5 ≤ n ≤ 2000")
def _():
    ensure(all(2 ** n > n * n for n in range(5, 2001)), "inequality")
    ensure([2 ** n > n * n for n in (2, 3, 4)] == [False] * 3, "fails at 2, 3, 4")


def makeable(n, a=4, b=5):
    return any((n - b * j) % a == 0 for j in range(n // b + 1))


@check("Q32c", "11, 6 or 1", kind="spot-check", note="every n from 12 to 5000 checked by brute force")
def _():
    ensure(all(makeable(n) for n in range(12, 5001)), "n ≥ 12")
    ensure(not makeable(11), "11")


@check("Q32f", "1, 2, 3, 6, 7 and 11", "ab − a − b")
def _():
    ensure([n for n in range(1, 200) if not makeable(n)] == [1, 2, 3, 6, 7, 11], "list")
    for a, b in ((3, 5), (4, 7), (5, 8), (7, 9)):
        bad = [n for n in range(1, a * b * 2) if not makeable(n, a, b)]
        ensure(len(bad) == (a - 1) * (b - 1) // 2 and max(bad) == a * b - a - b, f"{a},{b}")


# ======================================================================================
# Q33  Fibonacci
# ======================================================================================

@check("Q33a", "F_{n+3} − 1", kind="spot-check", note="checked for n ≤ 300")
def _():
    s = 0
    for n in range(1, 301):
        s += fib(n)
        ensure(s == fib(n + 2) - 1, f"n={n}")


@check("Q33b", "(−1)^{n+1}", kind="spot-check", note="checked for n ≤ 300")
def _():
    ensure(all(fib(n + 1) * fib(n - 1) - fib(n) ** 2 == (-1) ** n for n in range(1, 301)), "Cassini")


@check("Q33c", "φ^n", kind="spot-check", note="checked for n ≤ 1000 (via logarithms)")
def _():
    phi = (1 + math.sqrt(5)) / 2
    for n in range(1, 1001):
        ensure(math.log(fib(n)) <= (n - 1) * math.log(phi) + 1e-12, f"n={n}")


@check("Q33f", "F_{m+n} = F_m F_{n+1} + F_{m−1} F_n", kind="spot-check", note="checked for m, n ≤ 120")
def _():
    for m in range(1, 121):
        for n in range(1, 121):
            ensure(fib(m + n) == fib(m) * fib(n + 1) + fib(m - 1) * fib(n), f"m={m} n={n}")
    ensure(all(fib(2 * n) == fib(n) * (fib(n - 1) + fib(n + 1)) for n in range(1, 300)), "F_2n")


# ======================================================================================
# Q34  Rational function
# ======================================================================================

def f34(x):
    return (x * x + 3) / (x - 1)


@check("Q34a", "f(x) = x + 1 + 4/(x − 1)", "y = x + 1", kind="numeric")
def _():
    rng = random.Random(341)
    for _ in range(500):
        x = rand_frac(rng)
        if x != 1:
            ensure((x * x + 3) / (x - 1) == x + 1 + 4 / (x - 1), f"x={x}")
    close(f34(1e7) - (1e7 + 1), 0.0, 1e-6, "oblique asymptote +∞")
    close(f34(-1e7) - (-1e7 + 1), 0.0, 1e-6, "oblique asymptote −∞")
    ensure(f34(1 + 1e-9) > 1e8 and f34(1 - 1e-9) < -1e8, "vertical asymptote")
    ensure(f34(5) > 6 and f34(-3) < -2, "sides of asymptote")


@check("Q34b", "At x = 3, f = 6 (local minimum). At x = −1, f = −2 (local maximum).",
       "y-intercept is −3", kind="numeric", note="stationary points and values checked; the sketch is not")
def _():
    xmin, vmin = golden(f34, 1.5, 10)
    xmax, vmax = golden(f34, -10, 0.5, maximise=True)
    close(xmin, 3, 1e-6, "min x")
    close(vmin, 6, 1e-12, "min value")
    close(xmax, -1, 1e-6, "max x")
    close(vmax, -2, 1e-12, "max value")
    close(f34(0), -3, 1e-15, "y-intercept")
    ensure(count_solutions(f34, -50, 0.999) == 0 and count_solutions(f34, 1.001, 50) == 0, "no x-intercepts")


@check("Q34c", "k < −2 or k > 6", "(k − 6)(k + 2)", kind="numeric",
       note="solutions of f(x) = k counted numerically on both branches for 13 values of k")
def _():
    for k in (-60, -10, -3, -2.0001, -2, -1.9999, 0, 3, 5.9999, 6, 6.0001, 10, 60):
        n = count_solutions(lambda x: f34(x) - k, -400, 1 - 1e-7, 200_000) + \
            count_solutions(lambda x: f34(x) - k, 1 + 1e-7, 400, 200_000)
        want = 2 if (k < -2 or k > 6) else (1 if k in (-2, 6) else 0)
        ensure(n == want, f"k={k}: {n} solutions, expected {want}")
        close((k - 6) * (k + 2), k * k - 4 * k - 12, 1e-9, "factorisation")


@check("Q34f", "(3, ±√6)", kind="numeric")
def _():
    x, v = golden(lambda x: math.sqrt(f34(x)), 1.01, 20)
    close(x, 3, 1e-6, "x")
    close(v, math.sqrt(6), 1e-12, "|y| min")
    ensure(all(f34(x) < 0 for x in (-5, 0, 0.99)), "no curve for x < 1")


# ======================================================================================
# Q35  x² e^{−x}
# ======================================================================================

def f35(x):
    return x * x * math.exp(-x)


def d1(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)


def d2(f, x, h=1e-4):
    return (f(x + h) - 2 * f(x) + f(x - h)) / (h * h)


@check("Q35a", "f = 4/e² ≈ 0.541", kind="numeric")
def _():
    xmax, vmax = golden(f35, 0.5, 5, maximise=True)
    close(xmax, 2, 1e-6, "max x")
    close(vmax, 4 / math.e ** 2, 1e-12, "max value")
    xmin, vmin = golden(f35, -1, 1)
    close(xmin, 0, 1e-6, "min x")
    close(vmin, 0, 1e-12, "min value")
    close(round(4 / math.e ** 2, 3), 0.541, 1e-12, "rounding")


@check("Q35b", "x = 2 ± √2 (≈ 0.59 and 3.41)", kind="numeric", note="inflections and limits checked; the sketch is not")
def _():
    g = lambda x: d2(f35, x)
    r1, r2 = bisect_root(g, 0.2, 1.0, 80), bisect_root(g, 3.0, 4.0, 80)
    close(r1, 2 - math.sqrt(2), 1e-5, "first inflection")
    close(r2, 2 + math.sqrt(2), 1e-5, "second inflection")
    ensure(g(r1 - 0.05) * g(r1 + 0.05) < 0 and g(r2 - 0.05) * g(r2 + 0.05) < 0, "sign changes")
    ensure(f35(60) < 1e-20 and f35(60) > 0 and f35(-30) > 1e15, "behaviour at ±∞")


@check("Q35c", "k < 0: 0 solutions; k = 0: 1; 0 < k < 4/e²: 3; k = 4/e²: 2; k > 4/e²: 1", kind="numeric",
       note="solutions counted numerically for 9 values of k")
def _():
    km = 4 / math.e ** 2
    for k, want in ((-0.5, 0), (-1e-3, 0), (0.0, 1), (1e-3, 3), (0.3, 3), (km - 1e-4, 3), (km, 2),
                    (km + 1e-4, 1), (3.0, 1)):
        n = count_solutions(lambda x: f35(x) - k, -30.0001, 80, 400_000)
        ensure(n == want, f"k={k}: {n} solutions, expected {want}")


@check("Q35f", "2 − (N² + 2N + 2)e^{−N}", kind="numeric")
def _():
    close(simpson(f35, 0, 80, 20000), 2.0, 1e-10, "integral")
    for N in (1, 3, 7):
        close(simpson(f35, 0, N, 2000), 2 - (N * N + 2 * N + 2) * math.exp(-N), 1e-11, f"N={N}")


# ======================================================================================
# Q36  Folium-type loop
# ======================================================================================

def loop_pt(t):
    return 3 * t / (1 + t ** 3), 3 * t * t / (1 + t ** 3)


@check("Q36a", "x = 3t/(1 + t³), y = 3t²/(1 + t³)", kind="numeric")
def _():
    rng = random.Random(361)
    for _ in range(2000):
        t = rng.uniform(-5, 5)
        if abs(t + 1) < 1e-2:
            continue
        x, y = loop_pt(t)
        close(x ** 3 + y ** 3, 3 * x * y, 1e-9, f"t={t}")
        close(y, t * x, 1e-12, "on y = tx")
    # along y = tx the curve is x²((1 + t³)x − 3t) = 0: check the factorisation at random x
    for _ in range(200):
        t, x = rng.uniform(-3, 3), rng.uniform(-3, 3)
        close(x ** 3 + (t * x) ** 3 - 3 * x * (t * x), x * x * ((1 + t ** 3) * x - 3 * t), 1e-9, "factor")


@check("Q36b", "x + y = 3t/(1 − t + t²)", "(∛2, ∛4)", kind="numeric")
def _():
    for eps in (1e-4, -1e-4, 1e-7, -1e-7):
        x, y = loop_pt(-1 + eps)
        close(x + y, -1, 1e-3 if abs(eps) > 1e-6 else 1e-6, f"x+y near t=−1 (eps={eps})")
        ensure(abs(x) > 1e3, "goes to infinity")
    t, ymax = golden(lambda t: loop_pt(t)[1], 0.5, 3, maximise=True)
    close(t, 2 ** (1 / 3), 1e-6, "t")
    close(loop_pt(t)[0], 2 ** (1 / 3), 1e-9, "x")
    close(ymax, 4 ** (1 / 3), 1e-12, "y")
    ensure(abs(d1(lambda s: loop_pt(s)[0], t)) > 0.5, "dx/dt ≠ 0")


@check("Q36c", "= 3/2", kind="numeric", note="polar integral and an independent grid count of the region")
def _():
    # polar integral with t = tan φ, φ ∈ [0, π/2]
    integrand = lambda phi: 0.5 * 9 * math.tan(phi) ** 2 / (1 + math.tan(phi) ** 3) ** 2 / math.cos(phi) ** 2 \
        if phi < math.pi / 2 - 1e-12 else 0.0
    close(simpson(integrand, 0, math.pi / 2, 20000), 1.5, 1e-9, "polar integral")
    # independent: count grid cells inside x³ + y³ < 3xy in the first quadrant
    n, L = 800, 1.6
    h = L / n
    inside = 0
    for i in range(n):
        x = (i + 0.5) * h
        x3 = x ** 3
        for j in range(n):
            y = (j + 0.5) * h
            if x3 + y * y * y < 3 * x * y:
                inside += 1
    close(inside * h * h, 1.5, 4e-3, "grid area")


@check("Q36f", "(3/2, 3/2), at distance 3/√2", kind="numeric")
def _():
    r = lambda t: math.hypot(*loop_pt(t))
    t, rmax = grid_then_golden(r, 1e-3, 50, 20000, maximise=True)
    close(t, 1.0, 1e-5, "t")
    close(rmax, 3 / math.sqrt(2), 1e-12, "distance")


# ======================================================================================
# Q37  Skew lines
# ======================================================================================

P1, D1 = (1, 2, 0), (1, 0, 1)
P2, D2 = (0, 0, 3), (1, 1, 0)


def L1(s):
    return tuple(p + s * d for p, d in zip(P1, D1))


def L2(t):
    return tuple(p + t * d for p, d in zip(P2, D2))


def dist37(s, t):
    return math.dist(L1(s), L2(t))


def min_dist37():
    def inner(s):
        return golden(lambda t: dist37(s, t), -50, 50)[1]
    return golden(inner, -50, 50)


@check("Q37a", "t = 2 and t = 4", kind="numeric")
def _():
    cross = (D1[1] * D2[2] - D1[2] * D2[1], D1[2] * D2[0] - D1[0] * D2[2], D1[0] * D2[1] - D1[1] * D2[0])
    ensure(cross != (0, 0, 0), "parallel")
    ensure(min_dist37()[1] > 0.5, "lines meet")


@check("Q37b", "s = 7/3 and t = 8/3", "P = (10/3, 2, 7/3) and Q = (8/3, 8/3, 3)", "PQ = (2/3)(−1, 1, 1)")
def _():
    s, t = Fr(7, 3), Fr(8, 3)
    P = tuple(Fr(p) + s * d for p, d in zip(P1, D1))
    Q = tuple(Fr(p) + t * d for p, d in zip(P2, D2))
    ensure(P == (Fr(10, 3), 2, Fr(7, 3)) and Q == (Fr(8, 3), Fr(8, 3), 3), "points")
    PQ = tuple(q - p for p, q in zip(P, Q))
    ensure(sum(a * b for a, b in zip(PQ, D1)) == 0 and sum(a * b for a, b in zip(PQ, D2)) == 0, "perpendicular")
    ensure(PQ == (Fr(-2, 3), Fr(2, 3), Fr(2, 3)), "PQ")
    s_num, d = min_dist37()
    close(s_num, 7 / 3, 1e-5, "s from minimisation")


@check("Q37c", "2/√3 ≈ 1.155", kind="numeric")
def _():
    close(min_dist37()[1], 2 / math.sqrt(3), 1e-9, "distance")
    close(round(2 / math.sqrt(3), 3), 1.155, 1e-12, "rounding")


@check("Q37f", "−x + y + z = 1", "2/√3")
def _():
    plane = lambda p: -p[0] + p[1] + p[2]
    for s in (Fr(0), Fr(1), Fr(-7, 2)):
        ensure(plane(tuple(Fr(p) + s * d for p, d in zip(P1, D1))) == 1, "contains L1")
    ensure(-D2[0] + D2[1] + D2[2] == 0, "parallel to L2")
    close(abs(plane(P2) - 1) / math.sqrt(3), 2 / math.sqrt(3), 1e-12, "distance of L2")


# ======================================================================================
# Q38  Medians
# ======================================================================================

def rand_tri(rng):
    return [(rng.uniform(-5, 5), rng.uniform(-5, 5)) for _ in range(3)]


def tri_with_sides(a, b, c):
    """Coordinates of A, B, C with BC = a, CA = b, AB = c."""
    B, C = (0.0, 0.0), (a, 0.0)
    x = (c * c - b * b + a * a) / (2 * a)
    return (x, math.sqrt(c * c - x * x)), B, C


@check("Q38a", "(a + b + c)/3", "AG : GM = 2 : 1", kind="numeric", note="1000 random triangles")
def _():
    rng = random.Random(381)
    for _ in range(1000):
        A, B, C = rand_tri(rng)
        Gx, Gy = (A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3
        for P, Q, R in ((A, B, C), (B, C, A), (C, A, B)):
            M = ((Q[0] + R[0]) / 2, (Q[1] + R[1]) / 2)
            close(math.dist(P, (Gx, Gy)) / math.dist((Gx, Gy), M), 2.0, 1e-9, "ratio")
            cross = (M[0] - P[0]) * (Gy - P[1]) - (M[1] - P[1]) * (Gx - P[0])
            close(cross, 0.0, 1e-9, "collinear")


@check("Q38b", "2|a|² + 2|b|²", kind="spot-check", note="identity checked on 1000 random triangles")
def _():
    rng = random.Random(382)
    for _ in range(1000):
        A, B, C = rand_tri(rng)
        M = ((B[0] + C[0]) / 2, (B[1] + C[1]) / 2)
        close(math.dist(A, B) ** 2 + math.dist(A, C) ** 2, 2 * math.dist(A, M) ** 2 + 2 * math.dist(B, M) ** 2,
              1e-9, "Apollonius")


@check("Q38c", "√49 = 7", "√241/2 ≈ 7.76", "√145/2 ≈ 6.02", "145.5 = ¾(49 + 64 + 81)", kind="numeric")
def _():
    A, B, C = tri_with_sides(8, 7, 9)  # BC = 8, CA = 7, AB = 9
    ensure(abs(math.dist(B, C) - 8) + abs(math.dist(C, A) - 7) + abs(math.dist(A, B) - 9) < 1e-12, "sides")
    mid = lambda P, Q: ((P[0] + Q[0]) / 2, (P[1] + Q[1]) / 2)
    m8, m7, m9 = math.dist(A, mid(B, C)), math.dist(B, mid(C, A)), math.dist(C, mid(A, B))
    close(m8, 7, 1e-12, "median to 8")
    close(m7, math.sqrt(241) / 2, 1e-12, "median to 7")
    close(m9, math.sqrt(145) / 2, 1e-12, "median to 9")
    close(round(m7, 2), 7.76, 1e-12, "rounding")
    close(round(m9, 2), 6.02, 1e-12, "rounding")
    close(m8 ** 2 + m7 ** 2 + m9 ** 2, 145.5, 1e-12, "sum of squares")
    close(145.5, 0.75 * (49 + 64 + 81), 1e-15, "3/4 rule")


@check("Q38f", "194/3", kind="numeric", note="identity on 1000 random triangles and the 7–8–9 triangle")
def _():
    rng = random.Random(383)
    tris = [rand_tri(rng) for _ in range(1000)] + [list(tri_with_sides(8, 7, 9))]
    for A, B, C in tris:
        G_ = ((A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3)
        lhs = sum(math.dist(G_, P) ** 2 for P in (A, B, C))
        close(lhs, (math.dist(A, B) ** 2 + math.dist(B, C) ** 2 + math.dist(C, A) ** 2) / 3, 1e-9, "identity")
    A, B, C = tris[-1]
    G_ = ((A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3)
    close(sum(math.dist(G_, P) ** 2 for P in (A, B, C)), 194 / 3, 1e-12, "7–8–9")


# ======================================================================================
# Q39  Tilings and strings (brute force)
# ======================================================================================

def domino_tilings(rows: int, cols: int) -> int:
    """Count domino tilings of a rows × cols board by backtracking (fill first empty cell)."""
    full = (1 << (rows * cols)) - 1

    @lru_cache(maxsize=None)
    def go(mask: int) -> int:
        if mask == full:
            return 1
        i = 0
        while mask >> i & 1:
            i += 1
        r, c = divmod(i, cols)
        total = 0
        if c + 1 < cols and not mask >> (i + 1) & 1:
            total += go(mask | 1 << i | 1 << (i + 1))
        if r + 1 < rows:
            total += go(mask | 1 << i | 1 << (i + cols))
        return total

    return go(0)


def coloured_tilings(n: int) -> int:
    """Enumerate every tiling of 1×n by red/blue squares and dominoes explicitly."""
    count = 0
    stack = [0]
    while stack:
        pos = stack.pop()
        if pos == n:
            count += 1
            continue
        stack.extend([pos + 1, pos + 1])  # red square, blue square
        if pos + 2 <= n:
            stack.append(pos + 2)
    return count


@check("Q39a", "1, 2, 3, 5, 8, 13, 21, 34, 55, 89", "T_10 = 89")
def _():
    ensure([domino_tilings(2, n) for n in range(1, 11)] == [1, 2, 3, 5, 8, 13, 21, 34, 55, 89], "values")


@check("Q39b", "[(1 + √2)^{n+1} − (1 − √2)^{n+1}]/(2√2)", "2, 5, 12, 29, 70")
def _():
    s = math.sqrt(2)
    for n in range(0, 13):
        closed = ((1 + s) ** (n + 1) - (1 - s) ** (n + 1)) / (2 * s)
        ensure(coloured_tilings(n) == round(closed) and abs(closed - round(closed)) < 1e-6, f"n={n}")
    ensure([coloured_tilings(n) for n in range(1, 6)] == [2, 5, 12, 29, 70], "first values")


@check("Q39c", "1, 2, 4, 7, 13, 24, 44, 81, 149, 274, 504", "b_10 = 504")
def _():
    vals = [sum(1 for w in itertools.product("01", repeat=n) if "111" not in "".join(w)) for n in range(11)]
    ensure(vals == [1, 2, 4, 7, 13, 24, 44, 81, 149, 274, 504], str(vals))


@check("Q39f", "153", "1, 3, 11, 41, 153")
def _():
    vals = [domino_tilings(3, n) for n in range(1, 11)]
    ensure(vals == [0, 3, 0, 11, 0, 41, 0, 153, 0, 571], str(vals))


# ======================================================================================
# Q40  Recurrences (exact)
# ======================================================================================

@check("Q40a", "u_n = 4 × 3^n + 1")
def _():
    u = 5
    for n in range(60):
        ensure(u == 4 * 3 ** n + 1, f"n={n}")
        u = 3 * u - 2


@check("Q40b", "u_n = 3^n − 2^n")
def _():
    u = [0, 1]
    for _ in range(60):
        u.append(5 * u[-1] - 6 * u[-2])
    ensure(all(u[n] == 3 ** n - 2 ** n for n in range(len(u))), "closed form")


@check("Q40c", "x_n = 2^{2^n} + 2^{−2^n}", "x_3 = 256 + 1/256")
def _():
    x = Fr(5, 2)
    for n in range(7):
        ensure(x == 2 ** (2 ** n) + Fr(1, 2 ** (2 ** n)), f"n={n}")
        if n == 3:
            ensure(x == 256 + Fr(1, 256), "x_3")
        x = x * x - 2


@check("Q40f", "(2/3)(2^{2^n} − 2^{−2^n})")
def _():
    x, prod = Fr(5, 2), Fr(1)
    for n in range(1, 7):
        prod *= x
        ensure(prod == Fr(2, 3) * (2 ** (2 ** n) - Fr(1, 2 ** (2 ** n))), f"n={n}")
        x = x * x - 2


# ======================================================================================
# Q41  Irrationality
# ======================================================================================

@check("Q41a", "p² = 2q²", kind="spot-check", note="no q ≤ 10^6 has 2q² a perfect square")
def _():
    for q in range(1, 1_000_001):
        r = math.isqrt(2 * q * q)
        if r * r == 2 * q * q:
            raise CheckFailed(f"q={q}")


@check("Q41b", "2^p = 3^q", kind="spot-check", note="2^p ≠ 3^q for 1 ≤ p, q ≤ 400")
def _():
    threes = {3 ** q for q in range(1, 401)}
    ensure(not any(2 ** p in threes for p in range(1, 401)), "equality found")


@check("Q41c", "no rational root", kind="spot-check",
       note="exhaustive over odd a, b, c with |a|, |b|, |c| ≤ 61: discriminant never a square")
def _():
    odds = [v for v in range(-61, 62) if v % 2]
    for a in odds:
        for b in odds:
            for c in odds:
                D = b * b - 4 * a * c
                ensure(D < 0 or math.isqrt(D) ** 2 != D, f"{a},{b},{c}")


@check("Q41f", "b² − 4ac ≡ 5", "0, 1 or 4 (mod 8)", kind="spot-check",
       note="all odd a, b, c with |·| ≤ 61, and squares mod 8")
def _():
    odds = [v for v in range(-61, 62) if v % 2]
    ensure(all((b * b - 4 * a * c) % 8 == 5 for a in odds for b in odds for c in odds), "≡ 5")
    ensure({(n * n) % 8 for n in range(8)} == {0, 1, 4}, "squares mod 8")


# ======================================================================================
# Q42  Primes
# ======================================================================================

PRIMES = [p for p in range(2, 2000) if is_prime(p)]


@check("Q42a", "30031 = 59 × 509", kind="spot-check",
       note="for k ≤ 10 every prime factor of p_1⋯p_k + 1 is new; the value 30031 checked exactly")
def _():
    for k in range(1, 11):
        N = math.prod(PRIMES[:k]) + 1
        ensure(not set(factorise(N)) & set(PRIMES[:k]), f"k={k}")
    ensure(math.prod(PRIMES[:6]) + 1 == 30031 == 59 * 509 and is_prime(59) and is_prime(509), "30031")


@check("Q42b", "N ≡ −1 (mod p_i)", kind="spot-check",
       note="for the first k ≤ 8 primes ≡ 3 (mod 4), 4·Πp − 1 has a new prime factor ≡ 3 (mod 4)")
def _():
    threes = [p for p in PRIMES if p % 4 == 3]
    for k in range(1, 9):
        N = 4 * math.prod(threes[:k]) - 1
        fs = factorise(N)
        ensure(N % 4 == 3, "N ≡ 3 mod 4")
        ensure(any(q % 4 == 3 and q not in threes[:k] for q in fs), f"k={k}: {fs}")


@check("Q42c", "2021 = 43 × 47", kind="spot-check",
       note="P(1 + 43k) divisible by 43 for k ≤ 500; the value at n = 44 checked exactly")
def _():
    P = lambda n: n * n + n + 41
    ensure(P(1) == 43 and P(44) == 2021 == 43 * 47, "n = 44")
    ensure(all(P(1 + 43 * k) % 43 == 0 for k in range(501)), "divisibility")


@check("Q42f", "21 = 3 × 7")
def _():
    ensure(21 == 3 * 7 and 21 % 4 == 1 and 3 % 4 == 3 and 7 % 4 == 3, "example")


# ======================================================================================
# Runner
# ======================================================================================

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("-v", "--verbose", action="store_true", help="one line per part")
    ap.add_argument("--only", help="run only keys starting with this prefix, e.g. Q18")
    ap.add_argument("--bank", type=Path, default=BANK, help="path to the question bank (default: alongside this script)")
    args = ap.parse_args()

    answers = parse_bank(args.bank.read_text(encoding="utf-8"))
    keys = sorted(answers)
    if args.only:
        keys = [k for k in keys if k.startswith(args.only)]

    results: dict[str, tuple[str, str, float]] = {}  # key -> (status, message, seconds)
    for key in keys:
        if key in NOT_CHECKABLE:
            results[key] = ("unchecked", NOT_CHECKABLE[key], 0.0)
            continue
        chk = CHECKS.get(key)
        if chk is None:
            results[key] = ("MISSING", "no check and no reason given", 0.0)
            continue
        t0 = time.perf_counter()
        try:
            ans = answers[key]
            ensure(ans != "", "model answer not found in the bank")
            for snip in chk.snippets:
                ensure(normalise(snip) in ans, f"value {snip!r} not found in the model answer")
            chk.fn()
            results[key] = ("PASS", chk.note, time.perf_counter() - t0)
        except CheckFailed as e:
            results[key] = ("FAIL", str(e), time.perf_counter() - t0)
        except Exception as e:  # a crash in a check is a failure, not a pass
            results[key] = ("FAIL", f"{type(e).__name__}: {e}", time.perf_counter() - t0)

    stray = sorted((set(CHECKS) | set(NOT_CHECKABLE)) - set(answers))
    stray = [k for k in stray if not args.only or k.startswith(args.only)]

    for key in keys:
        status, msg, secs = results[key]
        kind = CHECKS[key].kind if key in CHECKS else "-"
        if args.verbose or status in ("FAIL", "MISSING"):
            print(f"{status:9} {key}  [{kind}] {secs:6.2f}s  {msg}")

    fails = [k for k in keys if results[k][0] == "FAIL"]
    missing = [k for k in keys if results[k][0] == "MISSING"]
    passed = [k for k in keys if results[k][0] == "PASS"]
    by_kind = {kd: [k for k in passed if CHECKS[k].kind == kd] for kd in KINDS}
    unchecked = [k for k in keys if results[k][0] == "unchecked"]

    n_probs = len({k[:3] for k in keys})
    print()
    print("=" * 78)
    print(f"Bank: {n_probs} problems, {len(keys)} answers checked here "
          f"({sum(k[-1] != 'f' for k in keys)} parts + {sum(k[-1] == 'f' for k in keys)} follow-ups)")
    print(f"PASS  {len(passed):3d}   exact/brute force {len(by_kind['exact'])}, numeric {len(by_kind['numeric'])}, "
          f"simulation {len(by_kind['simulation'])}, proof spot-checks {len(by_kind['spot-check'])}")
    print(f"FAIL  {len(fails):3d}   {' '.join(fails)}")
    print(f"MISSING {len(missing):1d}   {' '.join(missing)}")
    if stray:
        print(f"Checks for parts not in the bank: {' '.join(stray)}")

    print("\nCould not be checked numerically at all:")
    for k in unchecked:
        print(f"  {k}: {results[k][1]}")
    print("\nProofs: the statement was tested on many cases, but the argument itself cannot be checked numerically:")
    for k in by_kind["spot-check"]:
        print(f"  {k}: {results[k][1]}")
    print("=" * 78)
    return 1 if (fails or missing or stray) else 0


if __name__ == "__main__":
    sys.exit(main())
