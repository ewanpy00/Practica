"""Graded subprocess.

Invoked as ``python -m examshell.worker <rank_dir> <exercise> <student_file>
<seed>``. Runs the differential test battery and prints a single JSON line with
the verdict on stdout. Running in a separate process lets the parent enforce a
timeout (infinite loops) and isolates crashes.
"""

import copy
import importlib.util
import json
import os
import random
import sys

from examshell import specs

_counter = 0


def _load_module(path):
    global _counter
    _counter += 1
    spec = importlib.util.spec_from_file_location("submission_%d" % _counter, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)            # runs the file (prints suppressed)
    return module


def _fmt(args):
    return ", ".join(repr(a) for a in args)


def _run(rank_dir, exercise, student_file, seed):
    spec = specs.REGISTRY[exercise]
    func_names = spec.get("funcs") or [spec["func"]]
    ref_path = os.path.join(rank_dir, exercise, exercise + ".py")

    try:
        ref_module = _load_module(ref_path)
        ref_funcs = {name: getattr(ref_module, name) for name in func_names}
    except Exception as exc:                    # broken reference -> tooling bug
        return {"status": "error", "detail": "reference solution failed: %r" % exc}

    try:
        student_module = _load_module(student_file)
    except SyntaxError as exc:
        return {"status": "ko", "detail": "syntax error: %s" % exc}
    except FileNotFoundError:
        return {"status": "ko", "detail": "no file submitted at %s" % student_file}
    except Exception as exc:
        return {"status": "ko", "detail": "could not import your file: %r" % exc}

    student_funcs = {}
    for name in func_names:
        try:
            fn = getattr(student_module, name)
        except AttributeError:
            return {"status": "ko",
                    "detail": "function %s() is not defined in your file" % name}
        if not callable(fn):
            return {"status": "ko",
                    "detail": "%s is defined but is not a function" % name}
        student_funcs[name] = fn

    rng = random.Random(seed)
    multi = "funcs" in spec
    inputs = [tuple(c) for c in spec.get("cases", [])]
    gen = spec.get("gen")
    for _ in range(spec.get("n", 0)):
        if gen:
            inputs.append(gen(rng))

    check = spec.get("check")
    passed = 0
    for entry in inputs:
        if multi:
            func_name, args = entry
        else:
            func_name, args = func_names[0], entry
        ref, student = ref_funcs[func_name], student_funcs[func_name]

        try:
            expected = ref(*copy.deepcopy(args))
        except Exception:
            continue                            # skip inputs the oracle rejects
        try:
            got = student(*copy.deepcopy(args))
        except Exception as exc:
            return {"status": "ko", "tests": passed,
                    "detail": "%s(%s) raised %s: %s"
                              % (func_name, _fmt(args), type(exc).__name__, exc)}

        if check:
            ok = check(args, got, expected)
        else:
            ok = got == expected and isinstance(got, bool) == isinstance(expected, bool)
        if not ok:
            return {"status": "ko", "tests": passed,
                    "detail": "%s(%s)\n    expected: %r\n    got:      %r"
                              % (func_name, _fmt(args), expected, got)}
        passed += 1

    return {"status": "ok", "tests": passed}


def main():
    rank_dir, exercise, student_file, seed = sys.argv[1:5]
    real_stdout = sys.stdout
    sys.stdout = open(os.devnull, "w")          # silence student/reference prints
    try:
        result = _run(rank_dir, exercise, student_file, int(seed))
    except Exception as exc:
        result = {"status": "error", "detail": "grader crashed: %r" % exc}
    finally:
        sys.stdout.close()
        sys.stdout = real_stdout
    print(json.dumps(result))


if __name__ == "__main__":
    main()
