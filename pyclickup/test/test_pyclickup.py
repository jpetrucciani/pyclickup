"""
a base test suite for pyclickup
"""
import datetime
from pyclickup.models import List, Project, Space, Status, Tag, Task, Team, User
from pyclickup.models.client import test_client

CLICKUP = test_client()


def test_user():
    """testing the user property"""
    user = CLICKUP.user
    assert user
    assert isinstance(user, User)
    assert user.id == 123
    assert user.username == "John Doe"
    assert user.color
    assert user.profile_picture


def test_teams():
    """testing the teams property"""
    teams = CLICKUP.teams
    assert teams
    assert isinstance(teams, list)
    team = teams[0]
    assert isinstance(team, Team)
    assert team.id == "1234"
    assert isinstance(team.members, list)
    assert isinstance(team.members[0], User)


def test_get_team_by_id():
    """testing getting a team by id"""
    team = CLICKUP.get_team_by_id("1234")
    assert isinstance(team, Team)
    assert team.id == "1234"
    assert isinstance(team.members, list)
    assert isinstance(team.members[0], User)


def test_spaces():
    """testing if we can get the spaces"""
    team = CLICKUP.teams[0]
    spaces = team.spaces

    assert spaces
    assert isinstance(spaces, list)
    space = spaces[0]

    assert space
    assert isinstance(space, Space)
    assert space.id == "12345"
    assert space.name == "My Space"
    assert space.private
    assert space.statuses

    assert isinstance(space.statuses, list)
    assert isinstance(space.statuses[0], Status)


def test_projects():
    """testing if we can access projects"""
    team = CLICKUP.teams[0]
    spaces = team.spaces
    space = spaces[0]
    projects = space.projects

    assert projects
    assert isinstance(projects, list)
    project = projects[0]
    assert project
    assert isinstance(project, Project)

    assert project.id == "1234"
    assert project.name == "My project"

    assert isinstance(project.statuses, list)
    assert isinstance(project.statuses[0], Status)

    assert isinstance(project.lists, list)
    assert isinstance(project.lists[0], List)


def test_tasks():
    """testing if we can generate a list of tasks"""
    team = CLICKUP.teams[0]
    tasks = team.get_tasks()
    assert tasks
    assert isinstance(tasks, list)
    task = tasks[0]
    assert isinstance(task, Task)
    assert task.id == "av1"
    assert task.name == "My First Task"

    assert isinstance(task.status, Status)
    assert isinstance(task.creator, User)

    assert isinstance(task.assignees, list)
    assert isinstance(task.assignees[0], User)

    assert isinstance(task.tags, list)
    assert isinstance(task.tags[0], Tag)

    assert isinstance(task.date_created, datetime.datetime)
    assert isinstance(task.date_updated, datetime.datetime)
    assert isinstance(task.date_closed, datetime.datetime)
    assert isinstance(task.due_date, datetime.datetime)
    assert isinstance(task.start_date, datetime.datetime)
