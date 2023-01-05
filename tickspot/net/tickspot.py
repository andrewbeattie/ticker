"""
A class for interacting with TickSpot's API. Provides methods for listing tasks, projects, entries, and creating new entries.
"""

import time
import datetime
from pprint import PrettyPrinter
from tickspot.settings import env
from tickspot.net.service import Entry, Project, Task, Authorize


def current_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")


class TickSpot(Authorize):
    def __init__(self, username: str, password: str):
        super(TickSpot, self).__init__(username, password)
        self.user = username
        self.entry = Entry(self.token, self.user, self.sub_id)
        self.task = Task(self.token, self.user, self.sub_id)
        self.project = Project(self.token, self.user, self.sub_id)
        self.pp = PrettyPrinter(indent=4)

    def list_tasks(self, project_id: int):
        tasks = self.task.list(project_id=project_id)
        for task in tasks:
            print(f"Task Name: {task.get('name')}")
            print(f"       Id: {task.get('id')}")

    def list_projects(self):
        projects = self.project.list()
        for project in projects:
            print(f"Project Name: {project.get('name')}")
            print(f"          Id: {project.get('id')}")

    def list_entries(self, project_id: int, start_date: str, end_date: str):
        self.pp.pprint(
            self.entry.list(project_id=project_id, start_date=start_date, end_date=end_date)
        )

    def list_entries_today(self, project_id: int):
        if not project_id:
            entries = []
            projects = self.project.list()
            project_ids = [project.get("id") for project in projects]
            for project_id in project_ids:
                entries += self.entry.list(project_id=project_id,
                                           start_date=current_date(), end_date=current_date())
        else:
            entries = self.entry.list(project_id=project_id,
                                      start_date=current_date(), end_date=current_date())
        hours = 0
        print("---------------------------------------------")
        for entry in entries:
            print(f"Hours: {entry.get('hours')}")
            print(f"       {entry.get('notes')}")
            print("---------------------------------------------")
            hours += entry.get("hours")
        print(f"Hours Remaining: {8-hours}")

    def create_entry(self, project_id: int, task_id: int, hours: float, date: str, note: str):
        self.entry.post(
            {
                "project_id": project_id,
                "hours": hours,
                "date": date,
                "task_id": task_id,
                "notes": note,
            }
        )


def fetch(args):
    tickspot = TickSpot(
        username=env.get("TICKSPOT_USERNAME"), password=env.get("TICKSPOT_PASSWORD")
    )
    if args.category == "project":
        tickspot.list_projects()
    elif args.category == "task":
        tickspot.list_tasks(project_id=args.project)
    elif args.category == "time":
        tickspot.list_entries_today(project_id=args.project)
    else:
        raise ValueError("Only project, task and time are supported for list.")


def create(args):
    tickspot = TickSpot(
        username=env.get("TICKSPOT_USERNAME"), password=env.get("TICKSPOT_PASSWORD")
    )
    tickspot.create_entry(
        project_id=args.project, task_id=args.task, hours=args.hours, date=args.date, note=None
    )


def start(args):
    start_time = time.time()
    if not args.project:
        raise ValueError("Require project")
    if not args.task:
        raise ValueError("Require task")
    if args.message:
        print(f"Working on: {args.message}")
        input("     Press Enter to Submit Time: ")
    else:
        try:
            import os 
            from git import Repo
            repo = Repo(os.getcwd())
            branch = repo.active_branch.name
            args.message = branch
            print(f"Working on: {args.message}")
            input("     Press Enter to Submit Time: ")
        except:
            args.message = input("     Enter Note to Submit Time: ")

    end_time = time.time()
    time_lapsed = end_time - start_time
    hours = time_lapsed / 3600.0

    tickspot = TickSpot(
        username=env.get("TICKSPOT_USERNAME"), password=env.get("TICKSPOT_PASSWORD")
    )

    tickspot.create_entry(
        project_id=args.project, task_id=args.task, hours=hours, date=current_date(), note=args.message
    )
