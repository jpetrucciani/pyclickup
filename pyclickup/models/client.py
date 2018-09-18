"""
base client model to create and use http endpoints
"""
import requests
import urllib.parse
from pyclickup.globals import __version__, API_URL, LIBRARY, TEST_TOKEN, TEST_API_URL
from pyclickup.models import User, Task, Team
from pyclickup.models.error import RateLimited
from pyclickup.utils.text import datetime_to_ts, filter_locals


def test_client():
    """returns a test client"""
    return ClickUp(TEST_TOKEN, api_url=TEST_API_URL, debug=True)


class ClickUp:
    """client http wrapper"""

    task_boolean_options = ["reverse", "subtasks", "include_closed"]
    task_list_options = [
        "space_ids",
        "project_ids",
        "list_ids",
        "statuses",
        "assignees",
    ]

    def __init__(self, token, api_url=API_URL, cache=True, debug=False):
        """creates a new client"""
        if not token:
            raise Exception("no token specified!")
        self.token = token
        self.api_url = api_url
        self.version = __version__
        self.cache = cache
        self.debug = debug

        # cache
        self._user = None
        self._teams = None

    @property
    def headers(self):
        """forms the headers required for the API calls"""
        return {
            "Accept": "application/json",
            "AcceptEncoding": "gzip, deflate",
            "Authorization": self.token,
            "User-Agent": "{}/{}".format(LIBRARY, self.version),
        }

    @property
    def user(self):
        """get the user associated with this token"""
        if not self._user or not self.cache:
            self._user = User(self.get("user"), client=self)
        return self._user

    @property
    def teams(self):
        """get authorized teams"""
        if not self._teams or not self.cache:
            self._teams = [Team(x, client=self) for x in self.get("team")["teams"]]
        return self._teams

    def get_team_by_id(self, team_id):
        """given an team_id, return the team if it exists"""
        return Team(self.get("team/{}".format(team_id))["team"], client=self)

    def _log(self, *args):
        """logging method"""
        if not self.debug:
            return
        print(*args)

    def _req(self, path, method="get", **kwargs):
        """requests wrapper"""
        full_path = urllib.parse.urljoin(self.api_url, path)
        self._log("[{}]: {}".format(method.upper(), full_path))
        request = requests.request(method, full_path, headers=self.headers, **kwargs)
        if request.status_code == 429:
            raise RateLimited()
        return request

    def get(self, path, **kwargs):
        """makes a get request to the API"""
        return self._req(path, **kwargs).json()

    def post(self, path, **kwargs):
        """makes a post request to the API"""
        return self._req(path, method="post", **kwargs).json()

    def put(self, path, **kwargs):
        """makes a put request to the API"""
        return self._req(path, method="put", **kwargs).json()

    def _get_tasks(
        self,
        team_id,
        page=None,  # integer - it appears to fetch 100 at a time
        order_by=None,  # string, [id, created, updated, due_date]
        reverse=None,  # bool
        subtasks=None,  # bool
        space_ids=None,  # List
        project_ids=None,  # List
        list_ids=None,  # List
        statuses=None,  # List
        include_closed=False,  # bool
        assignees=None,  # List
        due_date_gt=None,  # integer, posix time
        due_date_lt=None,  # integer, posix time
        date_created_gt=None,  # integer, posix time
        date_created_lt=None,  # integer, posix time
        date_updated_gt=None,  # integer, posix time
        date_updated_lt=None,  # integer, posix time
        **kwargs
    ):
        """fetches the tasks according to the given options"""
        params = filter_locals(locals(), extras=["team_id"])

        for option in self.task_boolean_options:
            if option in params:
                params[option] = str(params[option]).lower()

        options = [
            "{}{}={}".format(
                x,
                "[]" if x in self.task_list_options else "",
                ",".join(params[x]) if x in self.task_list_options else params[x],
            )
            for x in params
        ]
        path = "team/{}/task?{}".format(team_id, "&".join(options))
        return [Task(x, client=self) for x in self.get(path)["tasks"]]

    def _get_all_tasks(self, team_id, **kwargs):
        """get all tasks wrapper"""
        tasks = []
        page_count = 0
        task_page = self._get_tasks(team_id, page=page_count, **kwargs)
        while task_page:
            tasks += task_page
            page_count += 1
            task_page = self._get_tasks(team_id, page=page_count, **kwargs)
        return tasks

    def _create_task(
        self,
        list_id,
        name,  # string
        content,  # string
        status,  # string
        assignees=None,  # array
        priority=None,  # integer
        due_date=None,  # integer posix time, or python datetime
    ):
        """creates a task in the specified list"""
        data = {"name": name, "content": content, "status": status}
        if assignees:
            data["assignees"] = assignees
        if priority:
            data["priority"] = priority
        if due_date:
            data["due_date"] = (
                due_date if isinstance(due_date, int) else datetime_to_ts(due_date)
            )
        return self.post("list/{}/task".format(list_id), data=data)
