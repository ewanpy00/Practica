"""ExamShell v2.1 - a faithful local emulation of the 42 exam shell.

The interface (menus, connexion animation, status board, prompt, grademe flow,
SUCCESS / FAILURE screens) reproduces jcluzet's 42_EXAM C++ examshell. The
grading backend is this project's differential grader, and the exercises come
from exam_bank/. This is NOT the real 42 exam and is not affiliated with 42.
"""

import os
import random
import re
import signal
import sys
import time
from datetime import datetime

from examshell import content
from examshell.grader import REPO_ROOT, grade

# ---- colours ----
BOLD = "\033[1m"
RESET = "\033[0m"
CYAN = "\033[36m"
UNDERLINE = "\033[4m"
WHITE = "\033[97m"
LIME = "\033[92m"
RED = "\033[91m"
MAGENTA = "\033[95m"
YELLOW = "\033[93m"
GRAY = "\033[90m"
REMOVE_LINE = "\033[1A\033[K"

TIME_MAX_MIN = 180

# Menu order and how many levels each exam runs (drawn randomly from the pool).
RANKS_ORDER = ["03", "04"]
EXAM_LEVELS = {"03": 6, "04": 4}

ANSI_RE = re.compile(r"\033\[[0-9;]*m")
BOX_WIDTH = 56


def clear():
    sys.stdout.write("\033[2J\033[3J\033[H")
    sys.stdout.flush()


def _vlen(text):
    """Visible length of a string, ignoring ANSI colour codes."""
    return len(ANSI_RE.sub("", text))


def box(lines, color=CYAN, width=BOX_WIDTH):
    """Return a rounded box around the given (possibly coloured) lines."""
    inner = width - 2
    out = [color + "╭" + "─" * inner + "╮" + RESET]
    for line in lines:
        pad = max(0, inner - 2 - _vlen(line))
        out.append(color + "│ " + RESET + line + " " * pad + color + " │" + RESET)
    out.append(color + "╰" + "─" * inner + "╯" + RESET)
    return "\n".join(out)


def prompt_glyph():
    return "  " + CYAN + "›" + RESET + " "


def sigd(*_):
    print("\nYou have been disconnected after using Ctrl+D")
    sys.exit(0)


def sigc(sig, _frame):
    name = {signal.SIGINT: "Ctrl+C", signal.SIGQUIT: "Ctrl+\\ (SIGQUIT)"}.get(sig, "a signal")
    print("\nYou have been disconnected after using %s" % name)
    sys.exit(0)


def ask(prompt=""):
    try:
        return input(prompt)
    except EOFError:
        sigd()
    except KeyboardInterrupt:
        sigc(signal.SIGINT, None)


def typewrite(text, delay):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)


def here():
    home = os.path.expanduser("~")
    return REPO_ROOT.replace(home, "~", 1) if REPO_ROOT.startswith(home) else REPO_ROOT


def remaining_time(end_time):
    left = int(end_time - time.time())
    if left < 0:
        return "0"
    return "%dhrs, %02dmin and %02dsec" % (left // 3600, (left % 3600) // 60, left % 60)


def grade_time(assignement):
    """Fibonacci-style wait (minutes) before the next grademe, like the real shell."""
    if assignement == 0:
        return 0
    fib = [0.5, 2.5]
    for i in range(2, 100):
        fib.append(fib[i - 1] + fib[i - 2])
        if i - 2 == assignement - 1:
            return fib[i - 2]
    return 0


class ExamShell:
    def __init__(self):
        self.username = os.environ.get("USER", "student")
        self.rank = None
        self.exercises = []
        self.level_max = 0
        self.points_per = 0
        self.passed = []            # exercise names, one per cleared level
        self.current = None
        self.assignement = 0        # failed attempts on the current exercise
        self.time_bef_grade = 0.0
        self.end_time = 0
        self.backup = False
        self.changex = False
        # settings
        self.redo_passed = False
        self.cheats = False
        self.waiting_time = True

    # ----------------------------------------------------------------- menus
    def _exam_row(self, key, rank):
        levels = EXAM_LEVELS[rank]
        glyph = CYAN + BOLD + "[%s]" % key + RESET
        title = ("Python  ·  Exam Rank %s" % rank).ljust(28)
        return "   %s  %s%s%s%s%d levels%s" % (
            glyph, WHITE + BOLD, title, RESET, GRAY, levels, RESET)

    def main_menu(self):
        keys = {str(i + 1): rank for i, rank in enumerate(RANKS_ORDER)}
        while True:
            clear()
            print()
            print(box([
                BOLD + WHITE + "Practica" + RESET + GRAY + "   Python practice trainer" + RESET,
                GRAY + "Offline 42-style exam simulator" + RESET,
            ]))
            print()
            print("  " + BOLD + WHITE + "Pick an exam to begin" + RESET + "\n")
            for key, rank in keys.items():
                print(self._exam_row(key, rank))
            print()
            print("   " + CYAN + BOLD + "[s]" + RESET + "  " + WHITE + "Settings" + RESET)
            print("   " + RED + BOLD + "[q]" + RESET + "  " + WHITE + "Quit" + RESET)
            print()
            choice = (ask(prompt_glyph()) or "").strip().lower()
            if choice in keys:
                return keys[choice]
            if choice == "s":
                self.settings_menu()
            elif choice in ("q", "quit", "exit", "0"):
                print("\n  " + GRAY + "See you next time." + RESET)
                sys.exit(0)

    def _setting_row(self, key, label, enabled):
        state = (LIME + BOLD + "● ON " + RESET) if enabled else (GRAY + "○ OFF" + RESET)
        return "   %s%s%s  %s%s%s %s" % (
            CYAN + BOLD, "[%s]" % key, RESET, WHITE, label.ljust(42), RESET, state)

    def settings_menu(self):
        while True:
            clear()
            print()
            print(box([BOLD + WHITE + "Settings" + RESET]))
            print()
            print(self._setting_row("1", "Replay exercises you already passed", self.redo_passed))
            print(self._setting_row("2", "Enable cheat commands", self.cheats))
            print()
            print("   " + RED + BOLD + "[0]" + RESET + "  " + WHITE + "Back" + RESET)
            print()
            choice = (ask(prompt_glyph()) or "").strip()
            if choice == "1":
                self.redo_passed = not self.redo_passed
            elif choice == "2":
                self.cheats = not self.cheats
            elif choice in ("0", "q"):
                break
        print("  " + GRAY + "Settings saved." + RESET)
        time.sleep(0.4)

    # ------------------------------------------------------------ onboarding
    def ask_param(self):
        while True:
            self.rank = self.main_menu()
            levels = EXAM_LEVELS[self.rank]
            clear()
            print()
            print(box([
                BOLD + WHITE + "Python  ·  Exam Rank %s" % self.rank + RESET,
                GRAY + "%d levels   ·   %d hours   ·   TEST mode" % (levels, TIME_MAX_MIN // 60) + RESET,
            ]))
            print()
            print("  Start this exam?  " + GRAY + "(y / n)" + RESET)
            if (ask(prompt_glyph()) or "").strip().lower() in ("y", "yes"):
                break

        # The pool is every exercise in the rank; the exam runs a fixed number
        # of levels, each drawn at random from that pool.
        self.exercises = content.exercises_for(self.rank)
        self.level_max = min(EXAM_LEVELS[self.rank], len(self.exercises))
        self.points_per = round(100 / self.level_max) if self.level_max else 0

        self.explanation()
        self.connexion()
        self.briefing()
        self.end_time = time.time() + TIME_MAX_MIN * 60

    def explanation(self):
        clear()
        print()
        print(box([BOLD + WHITE + "How it works" + RESET]))
        print()
        print("  " + CYAN + BOLD + "1." + RESET + "  Open a " + BOLD + WHITE + "second terminal" + RESET +
              " — keep this one for grading.")
        print("  " + CYAN + BOLD + "2." + RESET + "  Each level gives you a random subject at")
        print("        " + GRAY + here() + "/subjects/subject.en.txt" + RESET)
        print("  " + CYAN + BOLD + "3." + RESET + "  Write your answer in the " + LIME + "rendu" + RESET +
              " folder named in the subject.")
        print("  " + CYAN + BOLD + "4." + RESET + "  Run " + LIME + BOLD + "grademe" + RESET +
              " here to test it.")
        print("        " + GRAY + "Pass → next level    ·    Fail → try again" + RESET)
        print()
        print("  " + YELLOW + "Heads up  " + RESET + GRAY +
              "repeated failures add a cooldown before the next grademe." + RESET)
        print()
        print("  " + GRAY + "Local practice tool — not the real 42 exam, not affiliated with 42." + RESET)
        print()
        print("  " + GRAY + "Press Enter to continue." + RESET)
        ask(prompt_glyph())

    def connexion(self):
        clear()
        print()
        print("  " + CYAN + "Connecting to exam session" + RESET, end="")
        sys.stdout.flush()
        for _ in range(3):
            time.sleep(0.35)
            sys.stdout.write(GRAY + " ." + RESET)
            sys.stdout.flush()
        time.sleep(0.3)
        print()

    def briefing(self):
        clear()
        print()
        print(box([BOLD + WHITE + "You're in, " + LIME + self.username + RESET +
                   BOLD + WHITE + "!" + RESET], color=LIME))
        print()
        print("  Project    " + WHITE + BOLD + "Python Exam Rank %s" % self.rank + RESET)
        print("  Mode       " + YELLOW + "TEST" + RESET + GRAY + "  (your grade is not counted)" + RESET)
        print("  Levels     " + WHITE + "%d" % self.level_max + RESET)
        print("  Time       " + WHITE + "%d hours" % (TIME_MAX_MIN // 60) + RESET)
        print()
        print("  " + GRAY + "You can log out at any time." + RESET)
        print("  " + GRAY + "Press Enter to start the exam." + RESET)
        ask(prompt_glyph())

    # ------------------------------------------------------------- exercises
    def pick_exercise(self):
        pool = [e for e in self.exercises if self.redo_passed or e not in self.passed]
        return random.choice(pool) if pool else None

    def prepare_current(self):
        content.publish_subject(self.rank, self.current)
        content.scaffold(self.rank, self.current)

    def rendu_file(self):
        return os.path.join(content.RENDU, self.current, self.current + ".py")

    def info(self):
        grade = round(len(self.passed) / self.level_max * 100) if self.level_max else 0
        print("\n==================================================================\n")
        print("Mode: " + YELLOW + "TEST" + RESET + " (Your grade will not be counted)")
        print("Current Grade: " + LIME + str(grade) + RESET + " / 100\n")
        for lvl, name in enumerate(self.passed):
            print("  Level " + LIME + str(lvl) + RESET + ": ")
            print("    " + YELLOW + "0" + RESET + ": " + LIME + name + RESET +
                  " for " + str(self.points_per) + " potential points (" + LIME + "Success" + RESET + ")")
        print("  Level " + LIME + str(len(self.passed)) + RESET + ": ")
        for i in range(self.assignement):
            print("    " + YELLOW + str(i) + RESET + ": " + LIME + self.current + RESET +
                  " for " + str(self.points_per) + " potential points (" + RED + "Failure" + RESET + ")")
        print("    " + YELLOW + str(self.assignement) + RESET + ": " + LIME + self.current + RESET +
              " for " + str(self.points_per) + " potential points (" + CYAN + "Current" + RESET + ")")
        xp = round((len(self.passed) + 1) / self.level_max * 100) if self.level_max else 0
        print("\nAssignment: " + LIME + self.current + RESET + " for " + LIME + BOLD +
              ("%d" % xp) + RESET + "xp, try: " + YELLOW + str(self.assignement) + RESET + "\n")
        print("Subject location:  " + LIME + here() + "/subjects/subject.en.txt" + RESET)
        print("Exercise location: " + RED + here() + "/rendu/" + self.current + "/" + RESET)
        print("Here you " + RED + BOLD + "don't need" + RESET + " to use git.\n")
        print("End date: " + LIME + datetime.fromtimestamp(self.end_time).strftime("%d/%m/%Y %H:%M:%S") + RESET)
        print("Left time: " + LIME + remaining_time(self.end_time) + RESET)
        print("\n==================================================================")
        print("Use the \"" + LIME + "grademe" + RESET + "\" command to be graded, or \"" +
              LIME + "help" + RESET + "\" to get some help.")
        self.backup = True

    def start_new_ex(self):
        if not self.backup:
            self.current = self.pick_exercise()
            if self.current is None:
                self.end_exam()
            self.assignement = 0
            self.time_bef_grade = 0.0
            self.prepare_current()
        self.info()
        self.exam_prompt()

    # ---------------------------------------------------------------- prompt
    def exam_help(self):
        print("Commands:")
        print(LIME + "    help:" + RESET + " display this help")
        print(LIME + "    settings:" + RESET + " display settings menu")
        print(LIME + "    status:" + RESET + " display information about the exam")
        print(LIME + "    finish:" + RESET + " exit the exam")
        print(LIME + "    grademe:" + RESET + " grade your exercise")
        if self.cheats:
            print(BOLD + LIME + "CHEAT MENU:" + RESET)
            print(LIME + "    force_success:" + RESET + " force the current exercise to success")
            print(LIME + "    new_ex:" + RESET + " generate a new exercise for the same level")
            print(LIME + "    remove_grade_time:" + RESET + " remove the wait between two grademe")

    def exam_prompt(self):
        while True:
            line = ask(YELLOW + "examshell" + RESET + "> ")
            if line is None:
                sigd()
            cmd = line.strip()
            if not cmd:
                continue
            if cmd == "grademe":
                self.grademe()
            elif cmd == "status":
                self.changex = True
                self.info()
            elif cmd == "help":
                self.exam_help()
            elif cmd == "settings":
                self.settings_menu()
                self.info()
            elif cmd in ("finish", "exit", "quit"):
                print("Are you sure you want to" + RED + " exit" + RESET + " the exam?")
                print("All your progress will be " + RED + "lost" + RESET + ".")
                print("Type " + LIME + BOLD + "yes" + RESET + " to confirm.")
                if (ask() or "").strip() == "yes":
                    sys.exit(0)
                print(" ** Abort ** ")
            elif cmd == "force_success" and self.cheats:
                self.success_ex(force=True)
            elif cmd == "new_ex" and self.cheats:
                self.change_ex()
            elif cmd == "remove_grade_time" and self.cheats:
                self.waiting_time = False
                print("Time between grading is now removed for this exam")
            elif cmd in ("force_success", "new_ex", "remove_grade_time"):
                print(" ❌ Cheat commands are currently disabled, use " +
                      LIME + BOLD + "settings" + RESET + " command.")
            else:
                print("           **Unknown command**     type " + LIME + "help" + RESET + " for more help")

    def change_ex(self):
        if len([e for e in self.exercises if self.redo_passed or e not in self.passed]) <= 1:
            print("You can't change exercise, there is only one exercise in this level")
            return
        self.backup = False
        clear()
        print("  > You have generated a new exercise")
        self.start_new_ex()

    # --------------------------------------------------------------- grading
    def grademe(self):
        print("\nBefore continuing, please make " + RED + "ABSOLUTELY SURE" + RESET + " that you are in the right directory,")
        print("that you didn't forget anything, etc...")
        print("If your assignment is wrong, you will have the same assignment")
        print("\n but with less potential points to earn !")
        answer = ask(RED + "Are you sure?" + RESET + " [y/N] ")
        if (answer or "").strip().lower() != "y":
            print(" Abort")
            return
        wait = self.time_bef_grade - time.time()
        if wait > 0 and self.waiting_time:
            msg = RED + "ERROR: " + RESET + "You must wait at least " + YELLOW + BOLD
            if wait // 60 >= 1:
                msg += "%d minutes" % (wait // 60) + RESET + " and " + YELLOW + BOLD + "%d seconds" % (int(wait) % 60) + RESET
            else:
                msg += "%d seconds" % int(wait) + RESET
            print(msg + " until next grading request, so take your time to make more tests"
                  " and be sure you will succeed next try!")
            return
        print("Ok, making grading request to server now.")
        self.grade_request()

    def grade_request(self):
        print("\nWe will now wait for the job to complete.")
        print("Please be " + LIME + "patient" + RESET + ", this " + LIME + "CAN" + RESET + " take several minutes...")
        print("(10 seconds is fast, 30 seconds is expected, 3 minutes is a maximum)")
        for _ in range(random.randint(1, 3)):
            print("waiting...")
            time.sleep(random.uniform(0.3, 1.1))

        verdict = grade(self.rank, self.current, self.rendu_file())
        if verdict.get("status") == "ok":
            self.success_ex(force=False)
        else:
            print(RED + ">>>>>>>>>> FAILURE <<<<<<<<<<" + RESET)
            time.sleep(1)
            print("You have failed the assignment.")
            self.save_trace(verdict)
            self.fail_ex()
            print("(Press enter to continue...)")
            ask()
            self.info()

    def save_trace(self, verdict):
        os.makedirs(content.TRACES_DIR, exist_ok=True)
        name = "%d-%d_%s.trace" % (len(self.passed), self.assignement, self.current)
        with open(os.path.join(content.TRACES_DIR, name), "w") as handle:
            handle.write(verdict.get("detail", "no detail") + "\n")
        print("Trace saved to " + LIME + here() + "/traces/" + name + RESET + "\n")

    def fail_ex(self):
        self.assignement += 1
        self.time_bef_grade = time.time() + grade_time(self.assignement) * 60

    def success_ex(self, force):
        self.passed.append(self.current)
        print("\n" + LIME + ">>>>>>>>>> SUCCESS <<<<<<<<<<" + RESET + "\n")
        print("(Press enter to continue...)")
        ask()
        self.backup = False
        self.changex = False
        if len(self.passed) >= self.level_max:
            self.end_exam()
        self.start_new_ex()

    def end_exam(self):
        print(WHITE + BOLD + "\U0001F973 Congratulation! You have finished the Exam Rank %s !" % self.rank + RESET)
        print(WHITE + BOLD + "Thanks for studying with us " + LIME + BOLD + self.username + WHITE + BOLD + " ❤️" + RESET)
        sys.exit(0)

    # ------------------------------------------------------------------ main
    def run(self):
        signal.signal(signal.SIGINT, sigc)
        try:
            signal.signal(signal.SIGQUIT, sigc)
        except (AttributeError, ValueError):
            pass
        self.ask_param()
        self.start_new_ex()
