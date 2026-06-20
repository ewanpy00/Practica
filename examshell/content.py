"""Exercise discovery and workspace scaffolding.

Shared by the CLI and the interactive shell. Exam content lives in
``exam_bank/exam_rank_0X/<exercise>/``; the current subject is exposed at
``subjects/subject.en.txt`` and the student works under ``rendu/<exercise>/``
(both git-ignored), mirroring the real 42 exam layout.
"""

import os
import re

from examshell import specs
from examshell.grader import REPO_ROOT, rank_dir

RENDU = os.path.join(REPO_ROOT, "rendu")
SUBJECTS_DIR = os.path.join(REPO_ROOT, "subjects")
TRACES_DIR = os.path.join(REPO_ROOT, "traces")


def exercises_for(rank):
    base = rank_dir(rank)
    found = []
    if not os.path.isdir(base):
        return found
    for name in sorted(os.listdir(base)):
        ref = os.path.join(base, name, name + ".py")
        if name in specs.REGISTRY and os.path.isfile(ref):
            found.append(name)
    return found


def subject_path(rank, exercise):
    return os.path.join(rank_dir(rank), exercise, exercise + ".txt")


def read_subject(rank, exercise):
    with open(subject_path(rank, exercise)) as handle:
        return handle.read()


def signature(rank, exercise):
    func = specs.REGISTRY[exercise]["func"]
    with open(os.path.join(rank_dir(rank), exercise, exercise + ".py")) as handle:
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


def publish_subject(rank, exercise):
    """Expose the current subject at subjects/subject.en.txt (like the real exam)."""
    os.makedirs(SUBJECTS_DIR, exist_ok=True)
    dest = os.path.join(SUBJECTS_DIR, "subject.en.txt")
    with open(dest, "w") as handle:
        handle.write(read_subject(rank, exercise))
    return dest
