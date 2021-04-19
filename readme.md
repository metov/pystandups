# PyStandups
A command line utility for working with daily standups. A "standup" is a brief description of what work will be done that day. PyStandups supports:

* Storing standups for each day
* Reviewing the previous day's standup (in case the actual work done ended up being different from what was planned)
* A rudimentary "backlog" to save things for later standups

Standups are stored as a JSON dictionary. The location is hardcoded (see `DATA_DIR`). The schema and format may change without warning between versions of PyStandups, so back this up if it's important. However, the goal is to keep the data simple enough to be self-explanatory and trivial to migrate.

## Usage
* `standup today` - prepare standup at the beginning of the day. PyStandups will try to intelligently fill in as much information as possible, and you will have the opportunity to edit it in your editor.
* `standup later` - take quick notes for future standups. `standup today` automatically fills in the data from `standup later`. For more sophisticated management of planned tasks, use an external tool like Jira.
* `standup get today` and `standup get last` - print the relevant standup to standard out. These are mainly intended for use in scripts.

### Old Standups
PyStandups does not support working with standups older than today or other complex tasks. You can use an external tool like `jq` to work with the JSON file directly.

## Install
`pip install pystandups` to install latest release.

The project is managed by [poetry](https://python-poetry.org/) so if you want to work on the code see [`poetry install`](https://python-poetry.org/docs/cli/#install).

