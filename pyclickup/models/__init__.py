"""
models for each object in the clickup api
"""
import json
from pyclickup.globals import DEFAULT_STATUSES, LIBRARY
from pyclickup.utils.text import snakeify, ts_to_datetime, datetime_to_ts
from typing import Any


class BaseModel:
    """basic model that just parses camelCase json to snake_case keys"""

    def __init__(self, data: dict, client: Any = None, **kwargs: Any) -> None:
        """constructor"""
        self._data = {**data, **kwargs}
        self._json = self._jsond(data)
        self._client = client

        for key in self._data:
            setattr(self, snakeify(key), self._data[key])

    def _jsond(self, json_data: dict) -> str:
        """json dumps"""
        return json.dumps(json_data)

    def _jsonl(self, dictionary: str) -> dict:
        """json loads"""
        return json.loads(dictionary)


class User(BaseModel):
    """user object"""

    def __init__(self, data: dict, **kwargs: Any) -> None:
        """override"""
        if "user" in data.keys():
            data = data["user"]
        super(User, self).__init__(data, **kwargs)

    def __repr__(self):
        """repr"""
        return "<{}.User[{}] '{}'>".format(LIBRARY, self.id, self.username)


class Status(BaseModel):
    """status model"""

    def __repr__(self):
        """repr"""
        return "<{}.Status[{}] '{}'>".format(LIBRARY, self.orderindex, self.status)


class List(BaseModel):
    """List model"""

    def __repr__(self):
        """repr"""
        return "<{}.List[{}] '{}'>".format(LIBRARY, self.id, self.name)

    def rename(self, new_name):
        """renames a list"""
        rename_call = self._client.put(
            "list/{}".format(self.id), data={"name": new_name}
        )
        self.name = new_name
        return rename_call

    def get_tasks(self, **kwargs):
        """gets tasks for the list"""
        return self._client._get_tasks(
            self.project.space.team.id, list_ids=[self.id], **kwargs
        )

    def get_all_tasks(self, **kwargs):
        """gets every task for this list"""
        return self._client._get_all_tasks(
            self.project.space.team.id, list_ids=[self.id], **kwargs
        )

    def create_task(
        self,
        name,  # string
        content="",  # optional, but nice
        assignees=None,  # list of User objects, or int IDs
        status="Open",  # needs to match your given statuses for the list
        priority=0,  # default to no priority (0). check Task class for enum
        due_date=None,  # integer posix time, or python datetime
    ):
        """
        creates a task within this list, returning the id of the task.

        unfortunately right now, there is no way to retreive a task by id
        this will return the ID of the newly created task,
        but you'll need to re-query the list for tasks to get the task object
        """
        task_data = {"name": name, "content": content, "status": status}

        if assignees and isinstance(list, assignees):
            if isinstance(User, assignees[0]):
                task_data["assignees"] = [x.id for x in assignees]
            elif isinstance(int, assignees[0]):
                task_data["assignees"] = assignees

        if due_date:
            task_data["due_date"] = (
                due_date if isinstance(due_date, int) else datetime_to_ts(due_date)
            )

        if priority > 0:
            task_data["priority"] = priority

        new_task_call = self._client.post(
            "list/{}/task".format(self.id), data=task_data
        )
        return new_task_call["id"]


class Project(BaseModel):
    """project model"""

    def __init__(self, data, **kwargs):
        """override to parse the members"""
        super(Project, self).__init__(data, **kwargs)
        if self.override_statuses:
            self.statuses = (
                [Status(x, client=self._client, project=self) for x in self.statuses]
                if self.statuses
                else []
            )
        else:
            self.statuses = [
                Status(x, client=self._client, project=self) for x in DEFAULT_STATUSES
            ]
        self.lists = [List(x, client=self._client, project=self) for x in self.lists]

    def __repr__(self):
        """repr"""
        return "<{}.Project[{}] '{}'>".format(LIBRARY, self.id, self.name)

    def create_list(self, list_name):
        """creates a new list in this project: TODO get it updating"""
        new_list = self._client.post(
            "project/{}/list".format(self.id), data={"name": list_name}
        )
        return new_list

    def get_tasks(self, **kwargs):
        """gets tasks for the project"""
        return self._client._get_tasks(
            self.space.team.id, project_ids=[self.id], **kwargs
        )

    def get_all_tasks(self, **kwargs):
        """gets all of the tasks for the project"""
        return self._client._get_all_tasks(
            self.space.team.id, project_ids=[self.id], **kwargs
        )


class Space(BaseModel):
    """space model"""

    def __init__(self, data, **kwargs):
        """override to parse the members and statuses"""
        super(Space, self).__init__(data, **kwargs)
        self.statuses = [
            Status(x, client=self._client, space=self) for x in self.statuses
        ]
        self._projects = None

    def __repr__(self):
        """repr"""
        return "<{}.Space[{}] '{}'>".format(LIBRARY, self.id, self.name)

    @property
    def projects(self):
        if not self._projects or not self._client.cache:
            self._projects = [
                Project(x, client=self._client, space=self)
                for x in self._client.get("space/{}/project".format(self.id))[
                    "projects"
                ]
            ]
        return self._projects

    def get_tasks(self, **kwargs):
        """gets tasks for the space"""
        return self._client._get_tasks(self.team.id, space_ids=[self.id], **kwargs)

    def get_all_tasks(self, **kwargs):
        """gets all the tasks for the space"""
        return self._client._get_all_tasks(self.team.id, space_ids=[self.id], **kwargs)


class Team(BaseModel):
    """team object"""

    def __init__(self, data, **kwargs):
        """override to parse the members"""
        super(Team, self).__init__(data, **kwargs)
        self.members = [User(x, client=self._client, team=self) for x in self.members]
        self._spaces = None

    def __repr__(self):
        """repr"""
        return "<{}.Team[{}] '{}'>".format(LIBRARY, self.id, self.name)

    @property
    def spaces(self):
        if not self._spaces or not self._client.cache:
            self._spaces = [
                Space(x, client=self._client, team=self)
                for x in self._client.get("team/{}/space".format(self.id))["spaces"]
            ]
        return self._spaces

    def get_tasks(self, **kwargs):
        """gets tasks for the team"""
        return self._client._get_tasks(self.id, **kwargs)

    def get_all_tasks(self, **kwargs):
        """gets all of the tasks for the team"""
        return self._client._get_all_tasks(self.id, **kwargs)


class Tag(BaseModel):
    """Tag object"""

    def __repr__(self):
        """repr"""
        return "<{}.Tag '{}'>".format(LIBRARY, self.name)


class Task(BaseModel):
    """Task object"""

    class Priority:
        """task priority enum"""

        NONE = 0
        URGENT = 1
        HIGH = 2
        NORMAL = 3
        LOW = 4

    def __init__(self, data, **kwargs):
        """override to parse the data"""
        super(Task, self).__init__(data, **kwargs)
        self.creator = User(self.creator, client=self._client)
        self.status = Status(self.status, client=self._client)
        self.tags = [Tag(x) for x in self.tags]
        self.assignees = [User(x, client=self._client) for x in self.assignees]
        self.due_date = ts_to_datetime(self.due_date) if self.due_date else None
        self.start_date = ts_to_datetime(self.start_date) if self.start_date else None
        self.date_created = (
            ts_to_datetime(self.date_created) if self.date_created else None
        )
        self.date_updated = (
            ts_to_datetime(self.date_updated) if self.date_updated else None
        )
        self.date_closed = (
            ts_to_datetime(self.date_closed) if self.date_closed else None
        )

    def __repr__(self):
        """repr"""
        return "<{}.Task[{}] '{}'>".format(LIBRARY, self.id, self.name)

    def update(
        self,
        name=None,  # string
        content=None,  # string
        add_assignees=None,  # list of integers, or user objects
        remove_assignees=None,  # list of integers, or user objects
        status=None,  # string
        priority=None,  # integer
        due_date=None,  # integer posix time, or python datetime
    ):
        """updates the task"""
        if not add_assignees:
            add_assignees = []
        if not remove_assignees:
            remove_assignees = []
        path = "task/{}".format(self.id)
        data = {
            "assignees": {
                "add": [x if isinstance(x, int) else x.id for x in add_assignees],
                "rem": [x if isinstance(x, int) else x.id for x in remove_assignees],
            }
        }

        if name:
            data["name"] = name
        if content:
            data["content"] = content
        if status:
            data["status"] = status
        if priority:
            data["priority"] = priority
        if due_date:
            data["due_date"] = (
                due_date if isinstance(due_date, int) else datetime_to_ts(due_date)
            )

        return self._client.put(path, data=data)
