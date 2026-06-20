"""Test specifications for every exercise.

Grading is *differential*: for each generated input we run both the student's
function and the reference solution (the oracle) and compare. Therefore a spec
only needs to describe how to build valid inputs, not the expected outputs.

A spec is a dict with:
    func   : name of the function the student must define
    rank   : "03" or "04" (which exam_rank folder holds the exercise)
    cases  : list of fixed argument tuples (the subject examples)
    gen    : callable(rng) -> argument tuple, for random inputs
    n      : how many random inputs to generate
    check  : optional callable(args, student_out, ref_out) -> bool, used when
             several answers are valid (e.g. topological sort). Defaults to
             strict equality.
"""

import random
import string

LOWER = string.ascii_lowercase
LETTERS = LOWER + LOWER.upper()
DIGITS36 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _ints(rng, lo, hi, nmin, nmax):
    return [rng.randint(lo, hi) for _ in range(rng.randint(nmin, nmax))]


def _word(rng, nmin, nmax, alpha=LOWER):
    return "".join(rng.choice(alpha) for _ in range(rng.randint(nmin, nmax)))


# --------------------------------------------------------------------------
# Rank 04 generators
# --------------------------------------------------------------------------
def gen_array_merger(rng):
    return ([_ints(rng, -20, 20, 0, 5) for _ in range(rng.randint(0, 5))],)


def gen_intersection(rng):
    return (_ints(rng, 0, 15, 0, 8), _ints(rng, 0, 15, 0, 8))


def gen_rotation(rng):
    n = rng.randint(0, 6)
    l2 = [rng.randint(0, 5) for _ in range(n)]
    r = rng.random()
    if n > 0 and r < 0.4:
        k = rng.randint(0, n - 1)
        l1 = l2[k:] + l2[:k]
    elif r < 0.7:
        l1 = [rng.randint(0, 5) for _ in range(n)]
    else:
        l1 = [rng.randint(0, 5) for _ in range(rng.randint(0, 6))]
    return (l1, l2)


def gen_sliding_window(rng):
    n = rng.randint(1, 8)
    nums = [rng.randint(-10, 10) for _ in range(n)]
    return (nums, rng.randint(1, n))


def gen_palindrome(rng):
    return (_word(rng, 1, 9, "abc"),)


def gen_constellation(rng):
    alpha = "abc"
    pattern = ""
    for _ in range(rng.randint(1, 5)):
        pattern += rng.choice(alpha)
        r = rng.random()
        if r < 0.3:
            pattern += "*"
        elif r < 0.5:
            pattern += "."
    return (_word(rng, 0, 8, alpha), pattern)


def gen_package(rng):
    n = rng.randint(2, 6)
    nodes = list(string.ascii_uppercase[:n])
    order = nodes[:]
    rng.shuffle(order)
    graph = {node: [] for node in nodes}
    for i, node in enumerate(order):
        for earlier in order[:i]:
            if rng.random() < 0.3:
                graph[node].append(earlier)
    if rng.random() < 0.25:
        a, b = rng.sample(nodes, 2)
        graph[a].append(b)
        graph[b].append(a)
    return (graph,)


def check_package(args, got, ref):
    graph = args[0]
    if ref == "":                       # reference detected a cycle
        return got == ""
    if not isinstance(got, list) or sorted(got) != sorted(graph.keys()):
        return False
    pos = {node: i for i, node in enumerate(got)}
    return all(pos[d] < pos[node] for node, deps in graph.items() for d in deps)


# --------------------------------------------------------------------------
# Rank 03 generators
# --------------------------------------------------------------------------
def gen_bracket(rng):
    chars = "()[]{}" if rng.random() < 0.8 else "()[]{}abc"
    return ("".join(rng.choice(chars) for _ in range(rng.randint(0, 10))),)


def gen_cryptic(rng):
    return ([_word(rng, 1, 6, LETTERS) for _ in range(rng.randint(0, 6))],)


def gen_echo(rng):
    if rng.random() < 0.4:
        half = _word(rng, 0, 4)
        return (half + half[::-1],)
    return (_word(rng, 0, 8, LETTERS + "  "),)


def gen_mirror(rng):
    cols = rng.randint(0, 4)
    return ([[rng.randint(0, 9) for _ in range(cols)]
             for _ in range(rng.randint(0, 4))],)


def gen_hidenp(rng):
    big = _word(rng, 0, 10, LOWER + "012")
    if rng.random() < 0.5 and big:
        idxs = sorted(rng.sample(range(len(big)), rng.randint(0, len(big))))
        small = "".join(big[i] for i in idxs)
    else:
        small = _word(rng, 0, 4)
    return (small, big)


def gen_inter(rng):
    return (_word(rng, 0, 8), _word(rng, 0, 8))


def gen_base(rng):
    r = rng.random()
    if r < 0.15:
        return (_word(rng, 1, 4, "01"), rng.choice([0, 1, 37, 40]), 10)
    fb, tb = rng.randint(2, 36), rng.randint(2, 36)
    if r < 0.3:
        return ("".join(rng.choice(DIGITS36) for _ in range(rng.randint(1, 5))), fb, tb)
    return ("".join(rng.choice(DIGITS36[:fb]) for _ in range(rng.randint(1, 5))), fb, tb)


def gen_pattern(rng):
    chars = "0123456789" if rng.random() < 0.8 else "0123456789ab "
    return ("".join(rng.choice(chars) for _ in range(rng.randint(0, 10))),)


def gen_anagram(rng):
    a = _word(rng, 0, 8)
    if rng.random() < 0.5:
        b = list(a)
        rng.shuffle(b)
        b = "".join(c.upper() if rng.random() < 0.3 else c for c in b)
        return (a, b + (" " if rng.random() < 0.3 else ""))
    return (a, _word(rng, 0, 8))


def gen_shadow(rng):
    return (sorted(_ints(rng, -10, 10, 0, 6)), sorted(_ints(rng, -10, 10, 0, 6)))


def gen_perm(rng):
    a = _word(rng, 0, 8, LOWER + "  .")
    if rng.random() < 0.5:
        b = list(a)
        rng.shuffle(b)
        return (a, "".join(b))
    return (a, _word(rng, 0, 8, LOWER + "  ."))


def gen_sculptor(rng):
    return (_word(rng, 0, 10, LETTERS + "  12"),)


def gen_twist(rng):
    return (_ints(rng, 0, 20, 0, 7), rng.randint(0, 12))


def gen_whisper(rng):
    return (_word(rng, 0, 10, LETTERS + " 12"), rng.randint(-30, 30))


REGISTRY = {
    # ---- Rank 04 ----
    "array_merger": {
        "func": "merge_sorted", "rank": "04", "gen": gen_array_merger, "n": 60,
        "cases": [([[3, 1], [2], [5, 4]],), ([],), ([[2, 2], [1, 2]],)],
    },
    "list_intersection_finder": {
        "func": "find_intersection", "rank": "04", "gen": gen_intersection, "n": 60,
        "cases": [([1, 2, 3, 4], [2, 4, 6]), ([1, 1, 2], [1, 1, 1]), ([1, 2], [3, 4])],
    },
    "list_rotation": {
        "func": "list_rotation", "rank": "04", "gen": gen_rotation, "n": 60,
        "cases": [([3, 4, 5, 1, 2], [1, 2, 3, 4, 5]), ([2, 1, 3], [1, 2, 3]),
                  ([1, 2], [1, 2, 3])],
    },
    "sliding_window": {
        "func": "max_sliding_window", "rank": "04", "gen": gen_sliding_window, "n": 60,
        "cases": [([1, 2, 5, -1, 0, 3], 3)],
    },
    "palindrome_partitioner": {
        "func": "min_palindrome_partitions", "rank": "04", "gen": gen_palindrome, "n": 50,
        "cases": [("abddbba",), ("aab",), ("racecar",), ("abc",)],
    },
    "constellation_mapper": {
        "func": "is_match", "rank": "04", "gen": gen_constellation, "n": 80,
        "cases": [("aab", "a*b"), ("aaab", "a.b"), ("ab", "a.b"), ("ab", "a*b"),
                  ("abc", "abc")],
    },
    "package_dependency_resolver": {
        "func": "topological_order", "rank": "04", "gen": gen_package, "n": 60,
        "check": check_package,
        "cases": [({"A": ["B"], "D": [], "B": ["C", "D"], "C": []},),
                  ({"A": ["B"], "B": ["A"]},)],
    },
    # ---- Rank 03 ----
    "py_bracket_validator": {
        "func": "bracket_validator", "rank": "03", "gen": gen_bracket, "n": 80,
        "cases": [("()",), ("()[]{}",), ("(]",), ("([)]",), ("{[]}",)],
    },
    "py_cryptic_sorter": {
        "func": "cryptic_sorter", "rank": "03", "gen": gen_cryptic, "n": 60,
        "cases": [(["apple", "cat", "banana", "dog", "elephant"],)],
    },
    "py_echo_validator": {
        "func": "echo_validator", "rank": "03", "gen": gen_echo, "n": 60,
        "cases": [("racecar",), ("A man a plan a canal Panama",), ("hello",)],
    },
    "py_mirror_matrix": {
        "func": "mirror_matrix", "rank": "03", "gen": gen_mirror, "n": 60,
        "cases": [([[1, 2, 3], [4, 5, 6]],), ([[1, 2], [3, 4], [5, 6]],)],
    },
    "py_hidenp": {
        "func": "hidenp", "rank": "03", "gen": gen_hidenp, "n": 80,
        "cases": [("abc", "a1b2c3"), ("abc", "acb"), ("", "anything")],
    },
    "py_inter": {
        "func": "inter", "rank": "03", "gen": gen_inter, "n": 80,
        "cases": [("hello", "world"), ("banana", "band")],
    },
    "py_number_base_converter": {
        "func": "number_base_converter", "rank": "03", "gen": gen_base, "n": 80,
        "cases": [("1010", 2, 10), ("FF", 16, 2), ("10", 2, 99)],
    },
    "py_pattern_tracker": {
        "func": "pattern_tracker", "rank": "03", "gen": gen_pattern, "n": 80,
        "cases": [("123",), ("1357",), ("90",)],
    },
    "py_anagram": {
        "func": "anagram", "rank": "03", "gen": gen_anagram, "n": 80,
        "cases": [("listen", "silent"), ("Triangle", "Integral"), ("hello", "world")],
    },
    "py_shadow_merge": {
        "func": "shadow_merge", "rank": "03", "gen": gen_shadow, "n": 60,
        "cases": [([1, 3, 5], [2, 4, 6]), ([1, 2, 3], [4, 5, 6])],
    },
    "py_string_permutation_checker": {
        "func": "string_permutation_checker", "rank": "03", "gen": gen_perm, "n": 80,
        "cases": [("abc", "bca"), ("abc", "def")],
    },
    "py_string_sculptor": {
        "func": "string_sculptor", "rank": "03", "gen": gen_sculptor, "n": 80,
        "cases": [("hello",), ("ab cd",)],
    },
    "py_twist_sequence": {
        "func": "twist_sequence", "rank": "03", "gen": gen_twist, "n": 80,
        "cases": [([1, 2, 3, 4, 5], 2), ([1, 2, 3], 1)],
    },
    "py_whisper_cipher": {
        "func": "whisper_cipher", "rank": "03", "gen": gen_whisper, "n": 80,
        "cases": [("hello", 3), ("khoor", -3)],
    },
}
