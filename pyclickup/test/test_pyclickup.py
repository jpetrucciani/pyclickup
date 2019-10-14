"""
a base test suite for pyclickup
"""
from datetime import datetime
from pyclickup.models import (
    LIBRARY,
    List,
    Project,
    Space,
    Status,
    Tag,
    Task,
    Team,
    User,
)
from pyclickup.models.client import test_client, ClickUp
from pyclickup.globals import __version__, TEST_TOKEN


CLICKUP = test_client()


def is_list_of_type(check_list, check_type):
    """helper function for checking if it's a list and of a specific type"""
    assert isinstance(check_list, list)
    assert isinstance(check_list[0], check_type)
    return True


def test_user_agent():
    """tests the default user agent"""
    headers = CLICKUP.headers
    assert isinstance(headers, (dict,))
    assert headers["User-Agent"] == "{}/{}".format(LIBRARY, __version__)


def test_custom_user_agent():
    """tests the custom user agent"""
    test_user_agent = "brwnppr/0.96"
    headers = ClickUp(token=TEST_TOKEN, user_agent=test_user_agent).headers
    assert isinstance(headers, (dict,))
    assert headers["User-Agent"] == test_user_agent


def test_user():
    """testing the user property"""
    user = CLICKUP.user
    assert user
    assert isinstance(user, User)
    assert user.id == 123
    assert user.username == "John Doe"
    assert user.color
    assert user.profile_picture
    assert "<pyclickup.User" in str(user)


def test_teams():
    """testing the teams property"""
    teams = CLICKUP.teams
    assert teams
    assert isinstance(teams, list)
    team = teams[0]
    assert isinstance(team, Team)
    assert team.id == "1234"
    assert is_list_of_type(team.members, User)
    assert "<pyclickup.Team" in str(team)


def test_get_team_by_id():
    """testing getting a team by id"""
    team = CLICKUP.get_team_by_id("1234")
    assert isinstance(team, Team)
    assert team.id == "1234"
    assert is_list_of_type(team.members, User)


def test_spaces():
    """testing if we can get the spaces"""
    team = CLICKUP.teams[0]
    spaces = team.spaces

    assert is_list_of_type(spaces, Space)
    space = spaces[0]

    assert space.id == "12345"
    assert space.name == "My Space"
    assert space.private
    assert space.statuses
    assert "<pyclickup.Space" in str(space)

    assert is_list_of_type(space.statuses, Status)

    space_check = team.get_space("12345")
    assert space_check
    assert space_check == space


def test_projects():
    """testing if we can access projects"""
    team = CLICKUP.teams[0]
    spaces = team.spaces
    space = spaces[0]
    projects = space.projects

    assert is_list_of_type(projects, Project)
    project = projects[0]

    assert project.id == "1234"
    assert project.name == "My project"
    assert "<pyclickup.Project" in str(project)

    assert is_list_of_type(project.statuses, Status)
    assert is_list_of_type(project.lists, List)

    project_check = space.get_project("1234")
    assert project_check
    assert project_check == project


def test_lists():
    """testing if we can access lists"""
    team = CLICKUP.teams[0]
    spaces = team.spaces
    space = spaces[0]
    project = space.projects[0]
    lists = project.lists

    assert is_list_of_type(lists, List)
    list_0 = lists[0]
    assert "<pyclickup.List" in str(list_0)

    tasks = list_0.get_tasks()
    assert is_list_of_type(tasks, Task)


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

    assert is_list_of_type(task.assignees, User)
    assert is_list_of_type(task.tags, Tag)
    assert "<pyclickup.Tag" in str(task.tags[0])

    assert isinstance(task.date_created, datetime)
    assert isinstance(task.date_updated, datetime)
    assert isinstance(task.date_closed, datetime)
    assert isinstance(task.due_date, datetime)
    assert isinstance(task.start_date, datetime)
    assert "<pyclickup.Task" in str(task)
    assert "<pyclickup.Status" in str(task.status)

    all_tasks_for_team = team.get_all_tasks(page_limit=4)
    assert is_list_of_type(all_tasks_for_team, Task)


def test_get_task_by_id():
    """test v2 get task by id"""
    task = CLICKUP.get_task("9hz")
    assert isinstance(task, Task)


def test_delete_task_by_id():
    """test v2 delete task by id"""
    deleted = CLICKUP.delete_task("9xh")
    assert deleted


def test_get_task_members():
    """test v2 get task members"""
    task = CLICKUP.get_task("9hz")
    members = task.members
    assert isinstance(members, list)
    assert isinstance(members[0], User)
