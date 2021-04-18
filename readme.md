# PyStandups
A command line utility to help work with daily standups. A "standup" is a brief description of what work will be tackled that day, usually determined in the beginning of that day. PyStandups supports:

* Storing standups for each day
* Reviewing the last day's standup (in case the actual work was different from what was planned)
* A rudimentary "backlog" to save things for later sprints

Standups are stored as a JSON dictionary. The location is hardcoded (see `STANDUPS_FILE`). The schema and format may change without warning between versions of PyStandups, so back this up if you care. However, it should always stay simple enough as to be self-explanatory and trivial to migrate.

## Usage
* At the start of every day, run `standup today` to prepare your standup. PyStandups will try to intelligently fill in as much information as possible, and you will have the opportunity to edit it in your editor.
* If you ever think of something you need to do later, run `standup later` to take quick notes about what you are planning for future standups. The reason this exists is so that `standup today` can automatically fill in the data from `standup later` on the next day. For more sophisticated management of planned tasks, you should use an external tool like Jira.

### Getting Standups
To see current standups, just use `standup today`. If you don't make changes it won't write data, and even if you do, you will be asked for confirmation.

`standup get today` and `standup get yesterday` will also print the contents of the relevant standup. These are provided mainly for use in scripts. If you just want to check your standups manually, `standup today` with no arguments is more convenient. 

### Old Standups
Working with standups older than today or any other complex task is out of scope. You can use an external tool like `jq` to work with the JSON file directly.

## Install
Run `pip install .` from inside the repo root.

The project is managed by [poetry](https://python-poetry.org/) so if you want to work on the code see [`poetry install`](https://python-poetry.org/docs/cli/#install).

