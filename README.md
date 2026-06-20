# 42 Python Exam Practice

A collection of exam practice assignments, made as part of the
**42** exam.

This repository will be updated over time - as updates appear, as new assignments
are added, or as inaccuracies in the problem wording are found and corrected.

The project is split into exam *content* and the exam *simulator*:

- [`exam_rank_03/`](exam_rank_03/) — Python tasks based on 42exam.net Rank 03.
- [`exam_rank_04/`](exam_rank_04/) — Rank 04 tasks, recreated from memory.
- [`examshell/`](examshell/) — a local grademe-style exam shell that renders
  subjects and grades your code.

Each task folder contains:

```
<task>/
  ├── <task>.txt   problem statement (42-style subject)
  └── <task>.py    reference solution
```

## examshell — practice like the real exam

`examshell` simulates the 42 exam: it picks random exercises, shows the subject,
gives you a stub to fill in under `rendu/`, and grades your code. Grading is
**differential** — your function is run against the reference solution (used as
an oracle) on the subject examples plus many random inputs.

```sh
# list exercises
python3 -m examshell list

# start a timed exam session (3 exercises, 60 min) — type `grademe` to test
python3 -m examshell start --rank 03 --exercises 3 --time 60

# grade a single submission directly
python3 -m examshell grade 03 py_anagram --file path/to/your.py
```

Inside a session: `grademe` (run the tests), `subject` (reprint), `skip`, `quit`.
Your work lives in `rendu/` (git-ignored); the reference solutions stay in the
`exam_rank_0X/` folders as the grading oracle.

## Exam Rank 04

| Folder | Function | Summary |
|--------|----------|---------|
| [array_merger](exam_rank_04/array_merger/) | `merge_sorted(arrays)` | merge a list of int lists into one sorted list |
| [list_intersection_finder](exam_rank_04/list_intersection_finder/) | `find_intersection(l1, l2)` | intersection of two lists (unique, sorted) |
| [list_rotation](exam_rank_04/list_rotation/) | `list_rotation(l1, l2)` | check whether one list is a rotation of another |
| [sliding_window](exam_rank_04/sliding_window/) | `max_sliding_window(nums, k)` | maximums of every window of size k |
| [palindrome_partitioner](exam_rank_04/palindrome_partitioner/) | `min_palindrome_partitions(s)` | minimum number of palindromic pieces of a string |
| [constellation_mapper](exam_rank_04/constellation_mapper/) | `is_match(s, pattern)` | string matching against a pattern (`*` and `.`) |
| [package_dependency_resolver](exam_rank_04/package_dependency_resolver/) | `topological_order(graph)` | package install order (topological sort) |

## Exam Rank 03

| # | Folder | Function | Summary |
|---|--------|----------|---------|
| 01 | [py_bracket_validator](exam_rank_03/py_bracket_validator/) | `bracket_validator(s)` | check that `()[]{}` brackets are balanced and ordered |
| 02 | [py_cryptic_sorter](exam_rank_03/py_cryptic_sorter/) | `cryptic_sorter(strings)` | sort strings by length, case-insensitive order, vowels |
| 03 | [py_echo_validator](exam_rank_03/py_echo_validator/) | `echo_validator(text)` | palindrome check ignoring case and non-letters |
| 04 | [py_mirror_matrix](exam_rank_03/py_mirror_matrix/) | `mirror_matrix(matrix)` | reverse every row of a 2D matrix |
| 05 | [py_hidenp](exam_rank_03/py_hidenp/) | `hidenp(small, big)` | is `small` a subsequence of `big` |
| 06 | [py_inter](exam_rank_03/py_inter/) | `inter(s1, s2)` | common characters, no repeats, order of first string |
| 07 | [py_number_base_converter](exam_rank_03/py_number_base_converter/) | `number_base_converter(number, from_base, to_base)` | convert a number between bases 2–36 |
| 08 | [py_pattern_tracker](exam_rank_03/py_pattern_tracker/) | `pattern_tracker(text)` | count adjacent digit pairs that increase by one |
| 09 | [py_anagram](exam_rank_03/py_anagram/) | `anagram(s1, s2)` | anagram check, ignoring case and spaces |
| 10 | [py_shadow_merge](exam_rank_03/py_shadow_merge/) | `shadow_merge(list1, list2)` | merge two sorted lists into one |
| 11 | [py_string_permutation_checker](exam_rank_03/py_string_permutation_checker/) | `string_permutation_checker(s1, s2)` | are two strings permutations (case-sensitive) |
| 12 | [py_string_sculptor](exam_rank_03/py_string_sculptor/) | `string_sculptor(text)` | alternate case of letters, reset on spaces |
| 13 | [py_twist_sequence](exam_rank_03/py_twist_sequence/) | `twist_sequence(arr, k)` | rotate an array right by k positions |
| 14 | [py_whisper_cipher](exam_rank_03/py_whisper_cipher/) | `whisper_cipher(text, shift)` | Caesar cipher with positive/negative shift |

> ⚠️ The problem statements were recreated from memory and may differ slightly
> from the original exam wording. If you spot an inaccuracy, adjust the statement
> or the solution to match your own version.
