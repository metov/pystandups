import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict

import coloredlogs
import dictdiffer
from openeditor import edit_temp
import questionary
from tabulate import tabulate

DATA_DIR = Path("~").expanduser() / ".local/share/pystandups"
STANDUPS_FILE = "standups.json"

# Encourage editors to use markdown highlight for temp files
TEMP_EXTENSION = "md"

# Set up logging
log = logging.getLogger(__name__)
LOGFMT = "%(programname)s:%(lineno)d %(message)s"
coloredlogs.install(fmt=LOGFMT, datefmt="%H:%M:%S", level="DEBUG", logger=log)


class Standups:
    TStandup = Dict[str, str]

    def __init__(self):
        self._data = {"standups": {}, "later": ""}
        self.today = None
        self.last = None

    standup = Dict[str, str]

    @property
    def standups(self) -> Dict[str, TStandup]:
        return self._data["standups"]

    @property
    def later(self):
        return self._data["later"]

    @later.setter
    def later(self, value: str):
        self._data["later"] = value

    @property
    def todaystr(self):
        return datetime.today().strftime("%Y%m%d")

    def get_done(self) -> str:
        if self.today["done"]:
            log.debug('Found a "done" in today\'s standup.')
            return self.today["done"]
        elif self.last and self.last["todo"]:
            log.info("There's no \"done\" for today. Using the last day's todo.")
            return self.last["todo"]
        else:
            log.info("There's no standups at all. Using blank todo.")
            return ""

    def get_todo(self) -> str:
        if self.today["todo"] == "":
            log.info('There\'s no standup for today, returning "later".')
            return self.later
        return self.today["todo"]

    def load(self, path: Path):
        if path.exists():
            log.debug(f"Loading {path}")
            with path.open() as f:
                j = json.load(f)

            if self.standups or self.later:
                log.warning("Overwriting existing data with what is loaded from file.")

            self._data = j
        else:
            log.warning(f"{path} does not exist, loading nothing.")

    def save(self, path: Path):
        # Prepare diff baseline
        if path.exists():
            with path.open() as f:
                old = json.load(f)
        else:
            old = {}

        # Check diff
        diff = list(dictdiffer.diff(old, self._data))
        if len(diff) == 0:
            log.debug("No changes, writing nothing.")
            return

        t = tabulate(diff, tablefmt="plain", headers=["type", "path", "change"])
        log.info(f"Saving the following changes:\n{t}")
        if questionary.confirm(f"Write data to {path}?", default=True).ask():
            if not DATA_DIR.exists():
                log.warning(f"Creating {DATA_DIR}")
                DATA_DIR.mkdir(parents=True)

            with path.open("w") as f:
                json.dump(self._data, f, indent=4)

    def __enter__(self):
        self.load(self.standups_path())

        today = self.todaystr
        self.today = self.standups.setdefault(today, {"done": "", "todo": ""})
        past = [s for s in self.standups if s != today]
        if len(past) > 0:
            last_date = max(past)
            self.last = self.standups[last_date]

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save(self.standups_path())

    @staticmethod
    def standups_path():
        return DATA_DIR / STANDUPS_FILE


def set_today():
    with Standups() as standups:
        # User reviews done items (normally previous day's)
        done = standups.get_done()
        print(f"The previous standup was:\n{done}")
        if questionary.confirm("Edit?", default=done == "").ask():
            done = edit_temp(contents=done, name=f"done.{TEMP_EXTENSION}")
        standups.today["done"] = done

        # User reviews pending items
        todo = standups.get_todo()
        print(f"Today's standup is:\n{todo}")
        if questionary.confirm("Edit?", default=(todo == "")).ask():
            todo = edit_temp(contents=todo, name=f"todo.{TEMP_EXTENSION}")
        standups.today["todo"] = todo

        # If there was nothing for today then user would have seen later's items
        if todo == standups.later:
            if questionary.confirm('Clear "later"?', default=True).ask():
                standups.later = ""


def set_later():
    with Standups() as standups:
        # User reviews notes for the next standup
        later = standups.later
        print(f"Notes for later:\n{later}")
        standups.later = edit_temp(contents=later, name=f"later.{TEMP_EXTENSION}")
