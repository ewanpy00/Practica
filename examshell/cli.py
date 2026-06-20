"""Command-line entry point.

    python3 -m examshell                 # launch the interactive exam shell
    python3 -m examshell list [--rank]   # list available exercises
    python3 -m examshell grade <rank> <exercise> [--file] [--seed]
"""

import argparse
import os
import sys

from examshell import specs
from examshell.content import RENDU, exercises_for
from examshell.grader import RANKS, grade
from examshell.shell import ExamShell


def cmd_shell(_args=None):
    ExamShell().run()
    return 0


def cmd_list(args):
    ranks = [args.rank] if args.rank else sorted(RANKS)
    for rank in ranks:
        print("\nExam Rank %s" % rank)
        for name in exercises_for(rank):
            print("  %-32s %s()" % (name, specs.REGISTRY[name]["func"]))
    return 0


def cmd_grade(args):
    if args.exercise not in specs.REGISTRY:
        sys.exit("unknown exercise: %s" % args.exercise)
    file = args.file or os.path.join(RENDU, args.exercise, args.exercise + ".py")
    verdict = grade(args.rank, args.exercise, file, seed=args.seed)
    print("\n%s" % args.exercise)
    status = verdict["status"]
    if status == "ok":
        print("  \033[92mOK\033[0m  -  %d tests passed" % verdict.get("tests", 0))
        return 0
    colour = "\033[91m" if status == "ko" else "\033[93m"
    print("  %s%s\033[0m  -  %s" % (colour, status.upper(), verdict.get("detail", "")))
    return 1


def main(argv=None):
    parser = argparse.ArgumentParser(prog="examshell",
                                     description="Local 42 exam shell emulator.")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("start", help="launch the interactive exam shell (default)")

    p_list = sub.add_parser("list", help="list available exercises")
    p_list.add_argument("--rank", choices=sorted(RANKS))
    p_list.set_defaults(func=cmd_list)

    p_grade = sub.add_parser("grade", help="grade a single submission")
    p_grade.add_argument("rank", choices=sorted(RANKS))
    p_grade.add_argument("exercise")
    p_grade.add_argument("--file")
    p_grade.add_argument("--seed", type=int)
    p_grade.set_defaults(func=cmd_grade)

    args = parser.parse_args(argv)
    if not getattr(args, "func", None):     # no subcommand, or `start`
        return cmd_shell()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
