"""Test specifications for every exercise.

Grading is *differential*: for each generated input we run both the student's
function and the reference solution (the oracle) and compare. Therefore a spec
only needs to describe how to build valid inputs, not the expected outputs.

A spec is a dict with:
    func   : name of the function the student must define
    rank   : "03".."06" (which exam_rank folder holds the exercise)
    cases  : list of fixed argument tuples (the subject examples)
    gen    : callable(rng) -> argument tuple, for random inputs
    n      : how many random inputs to generate
    check  : optional callable(args, student_out, ref_out) -> bool, used when
             several answers are valid (e.g. topological sort). Defaults to
             strict equality.
    cls    : instead of ``func``, the class the student must define; each case
             is ``(ctor_args, [(method, args), ...])`` (see the Rank 06 section)
    selftest: optional callable(funcs, rng) -> None | failure detail, for tasks
             that are checked by a property of the student's own functions
             rather than against the reference (e.g. pack/unpack round-trip)
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
# Rank 05 generators
# --------------------------------------------------------------------------
def gen_compress(rng):
    return ("compress", (_word(rng, 0, 12, LOWER),))


def gen_decompress(rng):
    parts = []
    for _ in range(rng.randint(0, 6)):
        ch = rng.choice(LOWER)
        if rng.random() < 0.6:
            parts.append(ch + str(rng.randint(1, 20)))
        else:
            parts.append(ch)
    return ("decompress", ("".join(parts),))


def gen_compress_decompress(rng):
    return gen_compress(rng) if rng.random() < 0.5 else gen_decompress(rng)


def gen_spiral(rng):
    return (rng.randint(0, 6),)


def gen_graph_cycle(rng):
    nodes = list(range(rng.randint(0, 6)))
    graph = {node: [] for node in nodes}
    for node in nodes:
        for other in nodes:
            if other != node and rng.random() < 0.25:
                graph[node].append(other)
    return (graph,)


def gen_room_scheduler(rng):
    n = rng.randint(0, 8)
    meetings = []
    for _ in range(n):
        start = rng.randint(0, 30)
        end = start + rng.randint(1, 15)
        meetings.append([start, end])
    return (meetings,)


def check_room_scheduler(args, got, ref):
    meetings = args[0]
    if not isinstance(got, dict) or "total_rooms" not in got or "schedule" not in got:
        return False
    if got["total_rooms"] != ref["total_rooms"]:
        return False
    schedule = got["schedule"]
    if not isinstance(schedule, list) or len(schedule) != got["total_rooms"]:
        return False
    flattened = [tuple(m) for room in schedule for m in room]
    if sorted(flattened) != sorted(tuple(m) for m in meetings):
        return False
    for room in schedule:
        ordered = sorted(room, key=lambda iv: iv[0])
        for i in range(1, len(ordered)):
            if ordered[i][0] < ordered[i - 1][1]:
                return False
    return True


def gen_island_matrix(rng):
    rows = rng.randint(0, 5)
    cols = rng.randint(0, 5) if rows else 0
    return ([[rng.choice(["1", "0"]) for _ in range(cols)] for _ in range(rows)],)


def gen_prism(rng):
    alpha = "AB" if rng.random() < 0.5 else "ABC"
    rows = rng.randint(1, 5)
    cols = rng.randint(1, 5)
    grid = ["".join(rng.choice(alpha) for _ in range(cols)) for _ in range(rows)]
    pattern = "".join(rng.choice(alpha) for _ in range(rng.randint(1, 4)))
    return (grid, pattern)


def check_prism(args, got, ref):
    if not isinstance(got, list):
        return False
    try:
        return sorted(tuple(m) for m in got) == sorted(tuple(m) for m in ref)
    except TypeError:
        return False


def gen_word_ladder(rng):
    length = rng.randint(3, 4)
    alpha = "ab" if rng.random() < 0.5 else "abc"
    start = _word(rng, length, length, alpha)
    end = _word(rng, length, length, alpha)
    sentence = [_word(rng, length, length, alpha) for _ in range(rng.randint(0, 8))]
    if end not in sentence and rng.random() < 0.6:
        sentence.append(end)
    return (start, end, sentence)


# --------------------------------------------------------------------------
# Rank 04 generators
# --------------------------------------------------------------------------
def gen_rotation_detector(rng):
    n = rng.randint(0, 6)
    arr = [rng.randint(0, 4) for _ in range(n)]
    r = rng.random()
    if n > 0 and r < 0.4:
        k = rng.randint(0, n - 1)
        other = arr[k:] + arr[:k]
    elif r < 0.7:
        other = [rng.randint(0, 4) for _ in range(n)]
    else:
        other = [rng.randint(0, 4) for _ in range(rng.randint(0, 6))]
    return (arr, other)


def gen_constellation(rng):
    dim = rng.randint(0, 5)
    stars = [(rng.randint(-1, dim), rng.randint(-1, dim))
             for _ in range(rng.randint(0, 8))]
    return (stars, dim)


def gen_intersection(rng):
    lists = [sorted(_ints(rng, 0, 8, 0, 6)) for _ in range(rng.randint(0, 4))]
    return (lists,)


def gen_merge_sorted(rng):
    return ([sorted(_ints(rng, -10, 10, 0, 5)) for _ in range(rng.randint(0, 5))],)


def gen_palindrome(rng):
    return (_word(rng, 0, 9, "abc"),)


def gen_package(rng):
    names = ["app", "api", "db", "web", "core", "cli", "lib", "ui"]
    nodes = rng.sample(names, rng.randint(0, 6))
    graph = {}
    for node in nodes:
        deps = [rng.choice(names) for _ in range(rng.randint(0, 2))]
        graph[node] = [d for d in deps if d != node or rng.random() < 0.1]
    if rng.random() < 0.7:               # mostly acyclic: only depend "forward"
        order = {node: i for i, node in enumerate(nodes)}
        graph = {n: [d for d in deps if d not in order or order[d] < order[n]]
                 for n, deps in graph.items()}
    return (graph,)


def gen_sliding_maximum(rng):
    nums = _ints(rng, -10, 10, 0, 8)
    return (nums, rng.randint(-1, len(nums) + 2))


# --------------------------------------------------------------------------
# Rank 06 generators
#
# Class tasks use ``cls`` in the registry. A test case is a pair
# ``(constructor_args, [(method, args), ...])``: the same operations are replayed
# on the reference and on the student's object and every return value is compared.
# --------------------------------------------------------------------------
def gen_prefix_ops(rng):
    ops = []
    for _ in range(rng.randint(1, 14)):
        word = _word(rng, 0, 3, "ab")
        ops.append((rng.choice(["insert", "search", "starts_with"]), (word,)))
    return ((), ops)


def selftest_pack(funcs, rng):
    pack, unpack = funcs["pack"], funcs["unpack"]
    alphabet = "ab1#: \n9"
    samples = [[], [""], ["", ""], ["42", "exam#net", "level:6"], ["3:abc", "1:"]]
    samples += [[_word(rng, 0, 6, alphabet) for _ in range(rng.randint(0, 5))]
                for _ in range(80)]
    for strs in samples:
        packed = pack(list(strs))
        if not isinstance(packed, str):
            return "pack(%r) returned %r instead of a str" % (strs, packed)
        got = unpack(packed)
        if got != strs:
            return ("unpack(pack(%r))\n    expected: %r\n    got:      %r"
                    % (strs, strs, got))
    return None


def gen_task_order(rng):
    n = rng.randint(0, 6)
    prereqs = []
    for _ in range(rng.randint(0, 8)):
        if n < 2:
            break
        a, b = rng.sample(range(n), 2)
        if rng.random() < 0.8 and a < b:
            a, b = b, a                  # mostly acyclic: higher depends on lower
        prereqs.append([a, b])
    return (n, prereqs)


def gen_redundant_link(rng):
    n = rng.randint(3, 7)
    edges = [[rng.randint(1, i - 1), i] for i in range(2, n + 1)]
    u, v = rng.sample(range(1, n + 1), 2)
    edges.append([u, v])
    rng.shuffle(edges)
    edges = [e if rng.random() < 0.5 else e[::-1] for e in edges]
    return (edges,)


def check_redundant_link(args, got, ref):
    return isinstance(got, list) and sorted(got) == sorted(ref)


def gen_union_find_ops(rng):
    n = rng.randint(1, 6)
    ops = []
    for _ in range(rng.randint(1, 14)):
        method = rng.choice(["union", "connected", "find"])
        if method == "find":
            ops.append(("same_root", (rng.randrange(n), rng.randrange(n))))
        else:
            ops.append((method, (rng.randrange(n), rng.randrange(n))))
    return ((n,), ops)


def gen_cache_ops(rng):
    capacity = rng.randint(1, 3)
    ops = []
    for _ in range(rng.randint(1, 16)):
        if rng.random() < 0.5:
            ops.append(("put", (rng.randint(0, 4), rng.randint(0, 99))))
        else:
            ops.append(("get", (rng.randint(0, 4),)))
    return ((capacity,), ops)


def gen_heap_ops(rng):
    ops = []
    for _ in range(rng.randint(1, 20)):
        method = rng.choice(["push", "push", "pop", "peek", "size"])
        ops.append((method, (rng.randint(-9, 9),) if method == "push" else ()))
    return ((), ops)


def gen_autocomplete(rng):
    words = [_word(rng, 0, 4, "abc") for _ in range(rng.randint(0, 7))]
    prefix = _word(rng, 0, 2, "abc")
    if words and rng.random() < 0.5:
        prefix = rng.choice(words)[:rng.randint(0, 2)]
    return (words, prefix)


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
    # ---- Rank 05 ----
    "py_compress_decompress": {
        "funcs": ["compress", "decompress"], "rank": "05",
        "gen": gen_compress_decompress, "n": 80,
        "cases": [("compress", ("aabcccccaaa",)), ("decompress", ("a2bc5a3",)),
                  ("compress", ("",))],
    },
    "py_spiral_matrix": {
        "func": "generate_spiral", "rank": "05", "gen": gen_spiral, "n": 30,
        "cases": [(3,), (1,)],
    },
    "py_graph_cycle_detector": {
        "func": "py_graph_cycle_detector", "rank": "05", "gen": gen_graph_cycle, "n": 80,
        "cases": [({0: [1], 1: [2], 2: [0]},), ({0: [1], 1: [2], 2: []},), ({},)],
    },
    "py_room_scheduler": {
        "func": "py_room_scheduler", "rank": "05", "gen": gen_room_scheduler, "n": 60,
        "check": check_room_scheduler,
        "cases": [([[0, 30], [5, 10], [15, 20]],), ([],)],
    },
    "py_island_matrix_counter": {
        "func": "island_matrix_counter", "rank": "05", "gen": gen_island_matrix, "n": 60,
        "cases": [
            ([["1", "1", "1", "1", "0"], ["1", "1", "1", "0", "0"],
              ["1", "1", "1", "1", "0"], ["0", "0", "0", "0", "0"]],),
            ([["1", "1", "0", "0", "0"], ["1", "1", "0", "0", "0"],
              ["0", "0", "1", "0", "0"], ["0", "0", "0", "1", "1"]],),
            ([],),
        ],
    },
    "py_prism_detector": {
        "func": "prism_detector", "rank": "05", "gen": gen_prism, "n": 60,
        "check": check_prism,
        "cases": [(["CAT", "A..", "T.."], "CAT"), ([], "CAT")],
    },
    "py_word_ladder": {
        "func": "word_ladder", "rank": "05", "gen": gen_word_ladder, "n": 60,
        "cases": [("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]),
                  ("hit", "cog", ["hot", "dot", "dog", "lot", "log"])],
    },
    # ---- Rank 06 ----
    "prefix_dictionary": {
        "cls": "PrefixDictionary", "rank": "06", "gen": gen_prefix_ops, "n": 60,
        "cases": [((), [("insert", ("apple",)), ("search", ("apple",)),
                        ("search", ("app",)), ("starts_with", ("app",)),
                        ("insert", ("app",)), ("search", ("app",))])],
    },
    "pack_strings": {
        "funcs": ["pack", "unpack"], "rank": "06", "selftest": selftest_pack,
    },
    "task_order": {
        "func": "task_order", "rank": "06", "gen": gen_task_order, "n": 80,
        "cases": [(2, [[1, 0]]), (4, [[1, 0], [2, 0], [3, 1], [3, 2]]),
                  (2, [[0, 1], [1, 0]]), (3, [])],
    },
    "redundant_link": {
        "func": "redundant_link", "rank": "06", "gen": gen_redundant_link, "n": 80,
        "check": check_redundant_link,
        "cases": [([[1, 2], [1, 3], [2, 3]],),
                  ([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]],),
                  ([[1, 4], [3, 4], [1, 3], [1, 2], [4, 5]],)],
    },
    "union_find_system": {
        "cls": "UnionFind", "rank": "06", "gen": gen_union_find_ops, "n": 60,
        "cases": [((5,), [("connected", (0, 1)), ("union", (0, 1)),
                          ("union", (0, 1)), ("connected", (0, 1)),
                          ("union", (1, 2)), ("connected", (0, 2))])],
    },
    "cache_keeper": {
        "cls": "CacheKeeper", "rank": "06", "gen": gen_cache_ops, "n": 80,
        "cases": [((2,), [("put", (1, 1)), ("put", (2, 2)), ("get", (1,)),
                          ("put", (3, 3)), ("get", (2,)), ("get", (1,))])],
    },
    "min_heap": {
        "cls": "MinHeap", "rank": "06", "gen": gen_heap_ops, "n": 60,
        "cases": [((), [("pop", ()), ("push", (5,)), ("push", (3,)), ("push", (8,)),
                        ("peek", ()), ("pop", ()), ("size", ())])],
    },
    "trie_autocomplete": {
        "func": "trie_autocomplete", "rank": "06", "gen": gen_autocomplete, "n": 60,
        "cases": [(["apple", "app", "apricot", "banana"], "app"),
                  (["a", "ab", "abc"], ""), ([], "test"), (["test"], "xyz")],
    },
    # ---- Rank 04 ----
    "py_array_rotation_detector": {
        "func": "array_rotation_detector", "rank": "04", "gen": gen_rotation_detector,
        "n": 60,
        "cases": [([1, 2, 3, 4, 5], [4, 5, 1, 2, 3]), ([1, 2, 3, 4, 5], [5, 1, 2, 3, 4]),
                  ([1, 2, 3], [3, 2, 1]), ([1, 2], [1, 2, 3]), ([], [])],
    },
    "py_constellation_mapper": {
        "func": "constellation_mapper", "rank": "04", "gen": gen_constellation, "n": 60,
        "cases": [([(0, 0), (1, 1), (2, 2)], 3), ([], 2), ([(0, 0), (0, 0), (1, 1)], 2),
                  ([(0, 0), (5, 5)], 3)],
    },
    "py_list_intersection_finder": {
        "func": "list_intersection_finder", "rank": "04", "gen": gen_intersection, "n": 60,
        "cases": [([[1, 2, 3], [2, 3, 4], [2, 3, 5]],), ([],), ([[1, 2, 3], []],),
                  ([[5]],), ([[1, 1, 2, 3], [1, 2, 2, 3], [1, 2, 3, 3]],)],
    },
    "py_merge_sorted_lists": {
        "func": "merge_sorted_lists", "rank": "04", "gen": gen_merge_sorted, "n": 60,
        "cases": [([[1, 3, 5], [2, 4, 6]],), ([[]],), ([[-5, -1, 0], [-3, 2, 4]],),
                  ([[10], [10], [10]],), ([],)],
    },
    "py_palindrome_partitioner": {
        "func": "palindrome_partitioner", "rank": "04", "gen": gen_palindrome, "n": 50,
        "cases": [("aab",), ("aba",), ("abc",), ("",), ("a",)],
    },
    "py_package_dependency_resolver": {
        "func": "package_dependency_resolver", "rank": "04", "gen": gen_package, "n": 80,
        "cases": [({"app": ["database"], "database": ["driver"], "driver": []},),
                  ({"A": [], "B": ["A"], "C": ["A", "B"]},), ({},),
                  ({"X": ["Y"], "Y": ["X"]},), ({"A": ["A"]},), ({"A": ["missing"]},),
                  ({"web": [], "api": [], "frontend": ["web"], "backend": ["api"]},)],
    },
    "py_sliding_window_maximum": {
        "func": "sliding_window_maximum", "rank": "04", "gen": gen_sliding_maximum,
        "n": 60,
        "cases": [([1, 3, -1, -3, 5, 3, 6, 7], 3), ([1, 2, 3], 4), ([], 2), ([1, 2, 3], 0)],
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
