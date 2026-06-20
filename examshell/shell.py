"""ExamShell v2.1 - a faithful local emulation of the 42 exam shell.

The interface (menus, connexion animation, status board, prompt, grademe flow,
SUCCESS / FAILURE screens) reproduces jcluzet's 42_EXAM C++ examshell. The
grading backend is this project's differential grader, and the exercises come
from exam_bank/. This is NOT the real 42 exam and is not affiliated with 42.
"""

import os
import random
import signal
import sys
import time
from datetime import datetime

from examshell import content
from examshell.grader import REPO_ROOT, grade

# ---- colours (same codes as exam.hpp) ----
BOLD = "\033[1m"
RESET = "\033[0m"
CYAN = "\033[36m"
UNDERLINE = "\033[4m"
WHITE = "\033[97m"
LIME = "\033[92m"
RED = "\033[91m"
MAGENTA = "\033[95m"
YELLOW = "\033[93m"
REMOVE_LINE = "\033[1A\033[K"

TIME_MAX_MIN = 180


def clear():
    sys.stdout.write("\033[2J\033[3J\033[H")
    sys.stdout.flush()


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
    def main_menu(self):
        while True:
            clear()
            print(WHITE + BOLD + "         42EXAM ")
            print("     Made by " + LIME + "jcluzet" + RESET + "\n\n")
            print(LIME + BOLD + "            3" + RESET)
            print(WHITE + BOLD + "    | PYTHON EXAM RANK 03 |" + RESET + BOLD + "\n     \\ ------------------- /\n\n")
            print(LIME + BOLD + "            4" + RESET)
            print(WHITE + BOLD + "    | PYTHON EXAM RANK 04 |" + RESET + BOLD + "\n     \\ ------------------- /\n\n")
            print(LIME + BOLD + "            s" + RESET)
            print(WHITE + BOLD + "    |      SETTINGS       |" + RESET + BOLD + "\n     \\ ------------------- /\n\n")
            print(WHITE + BOLD + "    Enter your choice (" + RED + "q" + WHITE + " to quit):" + RESET + "\n            ", end="")
            choice = (ask() or "").strip().lower()
            if choice in ("3", "4"):
                return "%02d" % int(choice)
            if choice == "s":
                self.settings_menu()
            elif choice in ("q", "quit", "exit", "0"):
                print("\n  Bye!")
                sys.exit(0)

    def settings_menu(self):
        choice = ""
        while choice != "0":
            clear()
            print(WHITE + BOLD + "     === SETTINGS MENU ===" + "\n" + RED +
                  "          BACK" + RESET + WHITE + BOLD + " with " + RED + "0" + RESET + "\n")
            print(LIME + "1." + WHITE + BOLD + " Enable exercises you already passed" +
                  (LIME + BOLD + " ON" if self.redo_passed else RED + BOLD + " OFF") + RESET)
            print(LIME + "2." + WHITE + BOLD + " Enable cheat commands" +
                  (LIME + BOLD + " ON" if self.cheats else RED + BOLD + " OFF") + RESET)
            choice = (ask() or "").strip()
            if choice == "1":
                self.redo_passed = not self.redo_passed
            elif choice == "2":
                self.cheats = not self.cheats
        print(REMOVE_LINE + RESET + WHITE + BOLD + "Save settings..." + RESET)
        time.sleep(0.4)

    # ------------------------------------------------------------ onboarding
    def ask_param(self):
        while True:
            self.rank = self.main_menu()
            clear()
            print(LIME + BOLD + "       PYTHON EXAM RANK %s" % self.rank + RESET + "\n")
            print("   Confirm" + BOLD + WHITE + " Registration" + RESET + "?\n          (y/n)\n            ", end="")
            if (ask() or "").strip().lower() == "y":
                break

        self.exercises = content.exercises_for(self.rank)
        self.level_max = len(self.exercises)
        self.points_per = round(100 / self.level_max) if self.level_max else 0

        self.explanation()
        self.connexion()
        print("You're connected " + LIME + self.username + RESET + "!")
        print("You can log out at any time. If this program tells you you earned points,\n"
              "then they will be counted whatever happens.\n")
        print(BOLD + WHITE + "You are about to start the project " + LIME + BOLD + "ExamRank" +
              self.rank + BOLD + WHITE + ", in " + YELLOW + "TEST" + BOLD + WHITE +
              " mode, at level " + YELLOW + "0" + BOLD + WHITE + "." + RESET)
        print(WHITE + BOLD + "You would have " + LIME + BOLD + "%dhrs " % (TIME_MAX_MIN // 60) +
              BOLD + WHITE + "to complete this project." + RESET)
        print("Press a key to start exam \U0001F3C1")
        ask()
        self.end_time = time.time() + TIME_MAX_MIN * 60

    def explanation(self):
        clear()
        print("\n" + LIME + "        EXPLANATION : " + WHITE + BOLD + "\n")
        print("     ⚠️  You have to work from a new window to keep this one " + LIME + "available" + WHITE + BOLD + "\n")
        print("     \U0001F4DD A random subject named " + LIME + "subject.en.txt" + WHITE + BOLD + " will be generated")
        print("         > You must write your file in the assignment folder (see subject),")
        print("           this folder must be in folder: " + LIME + "rendu" + WHITE + BOLD + "\n")
        print("     \U0001F393 Once completed, correct your project with: " + LIME + "grademe" + WHITE + BOLD)
        print("         If your level is validated, you move on to the next level \U0001F389")
        print("         If not, you have to start again ❌\n")
        print("     ⌛️ Warning: the more you retry the same project, the longer you")
        print("        will have to wait before it can be " + LIME + "corrected" + WHITE + BOLD + ".\n")
        print(RED + "     ‼️  DISCLAIMER" + WHITE)
        print("         This program is " + RED + "not" + WHITE + " the real 42 exam and is " + RED + "not" + WHITE + " made by 42.")
        print("         Interface modelled on jcluzet/42_EXAM; grading is local and offline.\n")
        print(RESET + "     (Press enter to continue...)\n      ", end="")
        ask()

    def connexion(self):
        clear()
        typewrite("examshell", 0.05)
        print()
        time.sleep(0.4)
        clear()
        print(BOLD + UNDERLINE + "ExamShell v2.1" + RESET + "\n")
        print(BOLD + "login:" + RESET, end="")
        sys.stdout.flush()
        time.sleep(0.4)
        typewrite(self.username, 0.07)
        print("\n" + BOLD + "password:" + RESET, end="")
        sys.stdout.flush()
        for _ in range(random.randint(4, 13)):
            time.sleep(0.08)
            sys.stdout.write("*")
            sys.stdout.flush()
        print("\n\n")

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
        grade = self.points_per * len(self.passed)
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
        xp = (len(self.passed) + 1) / self.level_max * 100
        print("\nAssignment: " + LIME + self.current + RESET + " for " + LIME + BOLD +
              ("%g" % xp) + RESET + "xp, try: " + YELLOW + str(self.assignement) + RESET + "\n")
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
