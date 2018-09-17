"""
test file for pyclickup
"""
from pyclickup.models.client import test_client


clickup = test_client()


user = clickup.user
teams = clickup.teams
t = teams[0]
spaces = t.spaces
s = spaces[0]
projects = s.projects
p = projects[0]
lists = p.lists
l = lists[0]
