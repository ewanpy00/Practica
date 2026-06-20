"""Command-line entry point for the exam shell.

    python3 -m examshell list [--rank 03|04]
    python3 -m examshell grade <rank> <exercise> [--file FILE] [--seed N]
    python3 -m examshell start [--rank 03|04] [--exercises N] [--time MINUTES]
"""

import argparse
import os
import random
import re
import sys
import time

from examshell import specs
from examshell.grader import REPO_ROOT, RANKS, grade, rank_dir

RENDU = os.path.join(REPO_ROOT, "rendu")


# --------------------------------------------------------------------------
# discovery / scaffolding
# --------------------------------------------------------------------------
def exercises_for(rank):
    base = rank_dir(rank)
    found = []
    for name in sorted(os.listdir(base)):
        ref = os.path.join(base, name, name + ".py")
        if name in specs.REGISTRY and os.path.isfile(ref):
            found.append(name)
    return found


def subject_path(rank, exercise):
    return os.path.join(rank_dir(rank), exercise, exercise + ".txt")


def signature(rank, exercise):
    func = specs.REGISTRY[exercise]["func"]
    ref = os.path.join(rank_dir(rank), exercise, exercise + ".py")
    with open(ref) as handle:
        source = handle.read()
    match = re.search(r"^(def\s+%s\b.*:)\s*$" % re.escape(func), source, re.M)
    return match.group(1) if match else "def %s():" % func


def scaffold(rank, exercise):
    """Create rendu/<exercise>/<exercise>.py with a stub if it doesn't exist."""
    folder = os.path.join(RENDU, exercise)
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, exercise + ".py")
    if not os.path.exists(path):
        with open(path, "w") as handle:
            handle.write(signature(rank, exercise) +
                         "\n    # Write your solution here\n    pass\n")
    return path


def print_subject(rank, exercise):
    with open(subject_path(rank, exercise)) as handle:
        print("\n" + handle.read().rstrip() + "\n")


# --------------------------------------------------------------------------
# subcommands
# --------------------------------------------------------------------------
def cmd_list(args):
    ranks = [args.rank] if args.rank else sorted(RANKS)
    for rank in ranks:
        print("\nExam Rank %s" % rank)
        for name in exercises_for(rank):
            print("  %-32s %s()" % (name, specs.REGISTRY[name]["func"]))


def _report(verdict):
    status = verdict["status"]
    if status == "ok":
        print("  \033[32mOK\033[0m  -  %d tests passed" % verdict.get("tests", 0))
    elif status == "ko":
        print("  \033[31mKO\033[0m  -  %s" % verdict.get("detail", ""))
    else:
        print("  \033[33mERROR\033[0m  -  %s" % verdict.get("detail", ""))
    return status


def cmd_grade(args):
    if args.exercise not in specs.REGISTRY:
        sys.exit("unknown exercise: %s" % args.exercise)
    file = args.file or os.path.join(RENDU, args.exercise, args.exercise + ".py")
    verdict = grade(args.rank, args.exercise, file, seed=args.seed)
    print("\n%s" % args.exercise)
    return 0 if _report(verdict) == "ok" else 1


def cmd_start(args):
    pool = exercises_for(args.rank)
    if not pool:
        sys.exit("no exercises found for rank %s" % args.rank)
    count = min(args.exercises, len(pool))
    chosen = random.sample(pool, count)
    deadline = time.time() + args.time * 60

    print("=" * 70)
    print(" 42 examshell  -  Rank %s  -  %d exercise(s)  -  %d min"
          % (args.rank, count, args.time))
    print(" commands: grademe | subject | skip | quit")
    print("=" * 70)

    results = {}
    for exercise in chosen:
        path = scaffold(args.rank, exercise)
        print_subject(args.rank, exercise)
        print("Edit your solution in:  %s" % os.path.relpath(path, REPO_ROOT))

        while True:
            remaining = int(deadline - time.time())
            if remaining <= 0:
                print("\n\033[31mTime is up!\033[0m")
                return _summary(results, chosen)
            try:
                cmd = input("\nexamshell [%s | %dm%02ds] > "
                            % (exercise, remaining // 60, remaining % 60)).strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return _summary(results, chosen)

            if cmd == "grademe":
                if _report(grade(args.rank, exercise, path)) == "ok":
                    results[exercise] = "OK"
                    break
                results[exercise] = "KO"
            elif cmd == "subject":
                print_subject(args.rank, exercise)
            elif cmd == "skip":
                results.setdefault(exercise, "SKIPPED")
                break
            elif cmd in ("quit", "exit"):
                return _summary(results, chosen)
            elif cmd:
                print("  commands: grademe | subject | skip | quit")

    return _summary(results, chosen)


def _summary(results, chosen):
    print("\n" + "=" * 70)
    print(" Results")
    print("=" * 70)
    passed = 0
    for exercise in chosen:
        status = results.get(exercise, "SKIPPED")
        passed += status == "OK"
        print("  %-34s %s" % (exercise, status))
    print("-" * 70)
    print("  Score: %d / %d" % (passed, len(chosen)))
    return 0 if passed == len(chosen) else 1


def main(argv=None):
    parser = argparse.ArgumentParser(prog="examshell",
                                     description="Local 42 exam shell emulator.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="list available exercises")
    p_list.add_argument("--rank", choices=sorted(RANKS))
    p_list.set_defaults(func=cmd_list)

    p_grade = sub.add_parser("grade", help="grade a single submission")
    p_grade.add_argument("rank", choices=sorted(RANKS))
    p_grade.add_argument("exercise")
    p_grade.add_argument("--file")
    p_grade.add_argument("--seed", type=int)
    p_grade.set_defaults(func=cmd_grade)

    p_start = sub.add_parser("start", help="start an interactive exam session")
    p_start.add_argument("--rank", choices=sorted(RANKS), default="03")
    p_start.add_argument("--exercises", type=int, default=3)
    p_start.add_argument("--time", type=int, default=60, help="time limit in minutes")
    p_start.set_defaults(func=cmd_start)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
