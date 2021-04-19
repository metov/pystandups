"""
A command line utility to help work with daily standups.

For details, see: https://github.com/metov/pystandups

Usage:
    standup (--help | -h)
    standup today
    standup later
    standup get last
    standup get today
"""

from docopt import docopt

from pystandups.lib import Standups, set_today, set_later


def main():
    args = docopt(__doc__)

    if args["get"]:

        def st():
            with Standups() as standups:
                return standups

        if args["today"]:
            print(st().today["todo"])
        elif args["last"]:
            print(st().get_done())
    else:
        if args["today"]:
            set_today()
        elif args["later"]:
            set_later()


if __name__ == "__main__":
    main()
