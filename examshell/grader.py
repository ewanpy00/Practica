"""Spawns the grading worker as a subprocess and parses its verdict."""

import json
import os
import random
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAM_BANK = os.path.join(REPO_ROOT, "exam_bank")

RANKS = {"03": "exam_rank_03", "04": "exam_rank_04"}


def rank_dir(rank):
    return os.path.join(EXAM_BANK, RANKS[rank])


def grade(rank, exercise, student_file, seed=None, timeout=10):
    """Return a verdict dict: {status: ok|ko|error, detail?, tests?}."""
    if seed is None:
        seed = random.randrange(1 << 30)
    cmd = [sys.executable, "-m", "examshell.worker",
           rank_dir(rank), exercise, os.path.abspath(student_file), str(seed)]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              timeout=timeout, cwd=REPO_ROOT)
    except subprocess.TimeoutExpired:
        return {"status": "ko", "detail": "timed out after %ss (infinite loop?)" % timeout}

    line = proc.stdout.strip().splitlines()
    if not line:
        return {"status": "error",
                "detail": proc.stderr.strip() or "worker produced no output"}
    try:
        return json.loads(line[-1])
    except json.JSONDecodeError:
        return {"status": "error", "detail": proc.stdout.strip() or proc.stderr.strip()}
