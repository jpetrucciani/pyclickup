"""
base client model to create and use http endpoints
"""
import requests
import urllib.parse
from datetime import datetime
from requests.models import Response
from pyclickup.globals import (
    __version__,
    API_URL,
    API_V2_URL,
    LIBRARY,
    TEST_TOKEN,
    TEST_API_URL,
    TEST_API_V2_URL,
)
from pyclickup.models import User, Task, Team
from pyclickup.models.error import RateLimited
from pyclickup.utils.text import datetime_to_ts, filter_locals
from typing import Any, Dict, List, Optional, Union  # noqa


class ClickUp:
    """client http wrapper"""

    class API_VERSIONS:
        """api version enum"""

        V1 = 1
        V2 = 2

    task_boolean_options = ["reverse", "subtasks", "include_closed"]
    task_list_options = [
        "space_ids",
        "project_ids",
        "list_ids",
        "statuses",
        "assignees",
    ]

    def __init__(
        self,
        token: str,
        api_url: str = API_URL,
        api_v2_url: str = API_V2_URL,
        cache: bool = True,
        debug: bool = False,
        user_agent: str = "{}/{}".format(LIBRARY, __version__),
    ) -> None:
        """creates a new client"""
        if not token:
            raise Exception("no token specified!")
        self.token = token
        self.api_urls = {1: api_url, 2: api_v2_url}
        self.version = __version__
        self.cache = cache
        self.debug = debug
        self.user_agent = user_agent

        # cache
        self._user = None  # type: Optional[User]
        self._teams = None  # type: Optional[List[Team]]

    @property
    def headers(self) -> dict:
        """forms the headers required for the API calls"""
        return {
            "Accept": "application/json",
            "AcceptEncoding": "gzip, deflate",
            "Authorization": self.token,
            "User-Agent": self.user_agent,
        }

    @property
    def user(self) -> User:
        """get the user associated with this token"""
        if not self._user or not self.cache:
            self._user = User(self.get("user"), client=self)  # type: ignore
        return self._user

    @property
    def teams(self) -> List[Team]:
        """get authorized teams"""
        if not self._teams or not self.cache:
            teams_data = self.get("team")
            if not isinstance(teams_data, dict):
                raise Exception("invalid response while looking up teams")
            self._teams = [Team(x, client=self) for x in teams_data["teams"]]
        return self._teams

    def get_team_by_id(self, team_id: str) -> Team:
        """given an team_id, return the team if it exists"""
        team_data = self.get("team/{}".format(team_id))
        if not isinstance(team_data, dict):
            raise Exception("no team found")
        return Team(team_data["team"], client=self)

    def _log(self, *args: Any) -> None:
        """logging method"""
        if not self.debug:
            return
        print(*args)

    def _req(
        self, path: str, method: str = "get", version: int = 1, **kwargs: Any
    ) -> Response:
        """requests wrapper"""
        if version not in list(self.api_urls.keys()):
            raise Exception("unsupported api version")
        full_path = urllib.parse.urljoin(self.api_urls[version], path)
        self._log("[{}]: {}".format(method.upper(), full_path))
        request = requests.request(method, full_path, headers=self.headers, **kwargs)
        if request.status_code == 429:
            raise RateLimited()
        return request

    def get(
        self, path: str, raw: bool = False, version: int = 1, **kwargs: Any
    ) -> Union[list, dict, Response]:
        """makes a get request to the API"""
        request = self._req(path, version=version, **kwargs)
        return request if raw else request.json()

    def post(
        self, path: str, raw: bool = False, version: int = 1, **kwargs: Any
    ) -> Union[list, dict, Response]:
        """makes a post request to the API"""
        request = self._req(path, version=version, method="post", **kwargs)
        return request if raw else request.json()

    def put(
        self, path: str, raw: bool = False, version: int = 1, **kwargs: Any
    ) -> Union[list, dict, Response]:
        """makes a put request to the API"""
        request = self._req(path, version=version, method="put", **kwargs)
        return request if raw else request.json()

    def delete(
        self, path: str, raw: bool = False, version: int = 1, **kwargs: Any
    ) -> Union[list, dict, Response]:
        """makes a delete request to the API"""
        request = self._req(path, version=version, method="delete", **kwargs)
        return request if raw else request.json()

    def get_task(self, task_id: str) -> Optional[Task]:
        """
        @cc 2
        @desc v2 get a task by id!
        @arg task_id: the id
        @ret the task associated with this id
        @link api: https://jsapi.apiary.io/apis/clickup20/reference/0/tasks/get-task.html
        """
        task_data = self.get("task/{}".format(task_id), version=2)
        if task_data:
            return Task(task_data, client=self)
        return None

    def delete_task(self, task_id: str) -> bool:
        """
        @cc 2
        @desc v2: delete task by id!
        @arg task_id: the id to delete
        @ret success
        @link api: https://jsapi.apiary.io/apis/clickup20/reference/0/tasks/delete-task.html
        """
        try:
            self.delete("task/{}".format(task_id), version=2)
            return True
        except Exception:
            self._log("failed to delete task `{}`".format(task_id))
            return False

    def _get_tasks(
        self,
        team_id: str,
        page: int = None,  # integer - it appears to fetch 100 at a time
        order_by: str = None,  # string, [id, created, updated, due_date]
        reverse: bool = None,  # bool
        subtasks: bool = None,  # bool
        space_ids: list = None,  # List
        project_ids: list = None,  # List
        list_ids: list = None,  # List
        statuses: list = None,  # List
        include_closed: bool = False,  # bool
        assignees: list = None,  # List
        due_date_gt: int = None,  # integer, posix time
        due_date_lt: int = None,  # integer, posix time
        date_created_gt: int = None,  # integer, posix time
        date_created_lt: int = None,  # integer, posix time
        date_updated_gt: int = None,  # integer, posix time
        date_updated_lt: int = None,  # integer, posix time
        **kwargs: Any
    ) -> List[Task]:
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
        task_list = self.get(path)
        if not isinstance(task_list, dict):
            return []
        return [Task(x, client=self) for x in task_list["tasks"]]

    def _get_all_tasks(
        self, team_id: str, page_limit: int = -1, **kwargs: Any
    ) -> List[Task]:
        """get all tasks wrapper"""
        tasks = []  # type: List[Task]
        page_count = 0
        task_page = self._get_tasks(team_id, page=page_count, **kwargs)
        while task_page and (page_limit == -1 or page_count < page_limit):
            tasks += task_page
            page_count += 1
            task_page = self._get_tasks(team_id, page=page_count, **kwargs)
        return tasks

    def _create_task(
        self,
        list_id: str,
        name: str,  # string
        content: str,  # string
        status: str,  # string
        assignees: List[Union[int, User]] = None,  # list of integers, or user objects
        priority: int = None,  # integer
        due_date: Union[int, datetime] = None,  # integer posix time, or python datetime
    ) -> Any:
        """creates a task in the specified list"""
        data = {
            "name": name,
            "content": content,
            "status": status,
        }  # type: Dict[str, Any]
        if assignees:
            data["assignees"] = assignees
        if priority:
            data["priority"] = priority
        if due_date:
            data["due_date"] = (
                due_date if isinstance(due_date, int) else datetime_to_ts(due_date)
            )
        return self.post("list/{}/task".format(list_id), data=data)


def test_client() -> ClickUp:
    """returns a test client"""
    return ClickUp(
        TEST_TOKEN, api_url=TEST_API_URL, api_v2_url=TEST_API_V2_URL, debug=True
    )
