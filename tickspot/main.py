"""
This script is a command line interface for interacting with the TickSpot API. It allows the user to list projects, tasks, and time entries, as well as create and start new time entries.

The script is called with the ticker command followed by one of three subcommands: list, start, or create.

The list subcommand is used to retrieve information from TickSpot. It takes one required argument, category, which can be project, task, or time.

The start subcommand is used to start a new time entry in TickSpot. It takes two optional arguments: project, the ID of the project the time entry belongs to, and task, the ID of the task the time entry belongs to.

The create subcommand is used to create a new time entry in TickSpot. It takes four optional arguments: hours, the number of hours to be recorded in the time entry; project, the ID of the project the time entry belongs to; task, the ID of the task the time entry belongs to; and date, the date the time entry should be recorded for.

Examples of how to use the script:

ticker list project: lists all projects in TickSpot
ticker list task 11934: lists all tasks for project with ID 11934
ticker create -p 1955215 -t 14519343 -ho 8 -d 2021-10-11: creates a time entry for 8 hours on 2021-10-11 for task with ID 14519343 in project with ID 1955215
ticker start -p <project> -t <task> -m <summary>: starts a new time entry for the specified project and task with the given summary
ticker list time -p: lists all time entries for the current day for all projects
"""
from argparse import ArgumentParser
from tickspot.net.tickspot import TickSpot, fetch, create, start


def main():
    parser = ArgumentParser(prog="TickSpot")
    subparsers = parser.add_subparsers(help="help for subcommands")
    # parser for the list command allows user to collect information from TickSpot
    parser_list = subparsers.add_parser("list")
    parser_list.set_defaults(func=fetch)
    parser_list.add_argument(
        "category",
        choices=["project", "task", "time"],
        type=str,
        help="Defines the action to take, can be either task, project or entry",
    )
    parser_list.add_argument(
        "-p",
        "--project",
        type=int,
        help="To return tasks we require that a project id is provided.",
    )
    # parser for start command which allows user to start a TickSpot entry
    parser_start = subparsers.add_parser("start")
    parser_start.set_defaults(func=start)
    parser_start.add_argument(
        "-p", "--project", type=int, help="Project id as int to use when creating an entry."
    )
    parser_start.add_argument(
        "-t", "--task", type=int, help="Task id to use as int when creating an entry."
    )
    parser_start.add_argument(
        "-m", "--message", type=str, help="Task id to use as int when creating an entry."

    )
    # parser for create command which allows user to create a TickSpot entry
    parser_create = subparsers.add_parser("create")
    parser_create.set_defaults(func=create)
    parser_create.add_argument(
        "-ho", "--hours", type=float, help="How many hours to use when creating an entry."
    )
    parser_create.add_argument(
        "-p", "--project", type=int, help="Project id as int to use when creating an entry."
    )
    parser_create.add_argument(
        "-t", "--task", type=int, help="Task id to use as int when creating an entry."
    )
    parser_create.add_argument(
        "-d", "--date", help="Date to use when creating an entry in the format %Y-%m-%d."
    )
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    """Examples of How To Use
    ticker list project
    ticker list task 11934
    ticker create -p 1955215 -t 14519343 -ho 8 -d 2021-10-11
    ticker start -p <project> -t <task> -m <summary>
    ticker list time -p
    """
    main()
