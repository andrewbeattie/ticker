"""
Base model for calls to TickSpot. Provides methods for making POST, GET, and list requests to TickSpot's API.
"""

import json
import requests
import logging
from typing import Tuple, List, Dict, Any
from tickspot.net.manual_settings import Constants


logger = logging.getLogger(__name__)

constants = Constants()

class Authorize:
    """
    A class for authorizing a TickSpot user.
    """

    __slots__ = ["username", "password", "token", "sub_id"]

    def __init__(self, username: str, password: str) -> None:
        """
        Initialize a new Authorize object with the given username and password.

        Args:
        - username: The TickSpot username to authorize.
        - password: The TickSpot password to authorize.
        """
        self.token, self.sub_id = self.authorize(username, password)

    def authorize(self, username: str, password: str) -> Tuple[str, str]:
        """
        Authorize the given username and password, and return a tuple containing the API token and subscription ID.

        Args:
        - username: The TickSpot username to authorize.
        - password: The TickSpot password to authorize.

        Returns:
        - A tuple containing the API token and subscription ID for the authorized user.

        Raises:
        - Exception: If the authorization is unsuccessful.
        """
        headers = {"User-agent": f"Ticker ({username})"}
        r = requests.get(
            constants.BASE_URL + "roles.json", headers=headers, auth=(username, password)
        )
        try:
            data = json.loads(r.text)[0]
            return data.get("api_token"), data.get("subscription_id")
        except Exception as error:
            raise Exception(r.text) from error


class Resource(object):
    __slots__ = ["token", "sub_id"]
    """
    Base model for calls to TickSpot
    """

    def __init__(self, token: str, user: str, sub_id: str):
        self.token = token
        self.sub_id = sub_id
        self.user = user

    @property
    def headers(self) -> dict:
        return {
            "User-agent":  f"Ticker ({self.user})",
            "Authorization": f"Token token={self.token}"
        }

    def post(self, obj: str, data: dict) -> Any:
        """
        Make a POST request to TickSpot's API.
        
        Args:
        - obj: the endpoint to make the request to.
        - data: a dictionary containing the data to be sent in the request.
        
        Returns:
        The response data, parsed as a dictionary. If the request fails, raises an exception.
        """
        r = requests.post(constants.BASE_URL_SUB_ID % self.sub_id + obj, json=data, headers=self.headers)
        try:
            return json.loads(r.text)
        except Exception as error:
            raise Exception(r.text) from error

    def get(self, obj: str) -> Any:
        """
        Make a GET request to TickSpot's API.
        
        Args:
        - obj: the endpoint to make the request to.
        
        Returns:
        The response data, parsed as a dictionary. If the request fails, returns an exception.
        """
        r = requests.get(constants.BASE_URL_SUB_ID % self.sub_id + obj, headers=self.headers)
        try:
            return json.loads(r.text)
        except Exception as error:
            raise Exception(r.text) from error

    def list(self, obj: str) -> Any:
        """
        Make a GET request to TickSpot's API to retrieve a list of resources.
        
        Args:
        - obj: the endpoint to make the request to.
        
        Returns:
        The response data, parsed as a dictionary. If the request fails, returns an exception.
        """
        r = requests.get(constants.BASE_URL_SUB_ID % self.sub_id + obj, headers=self.headers)
        try:
            return json.loads(r.text)
        except Exception as error:
            raise Exception(r.text) from error

class Entry(Resource):
    """
    A class for interacting with TickSpot entries.
    """

    def __init__(self, token: str, user: str, sub_id: str):
        """
        Initialize a new Entry object with the given sub_id and token.

        Args:
        - sub_id: The TickSpot subscription ID.
        - token: The authorization token for the TickSpot API.
        """
        self.sub_id = sub_id
        self.token = token
        self.user = user

    def post(self, data: Dict) -> Dict:
        """
        Make a POST request to the TickSpot API to create a new entry.

        Args:
        - data: The data for the new entry.

        Returns:
        - The JSON response from the API.
        """
        return super(Entry, self).post("/entries.json", data)

    def list(self, project_id: int, start_date: str, end_date: str) -> Dict:
        """
        Get a list of entries for the given project and date range.

        Args:
        - project_id: The ID of the project to retrieve entries for.
        - start_date: The start date for the date range to retrieve entries for.
        - end_date: The end date for the date range to retrieve entries for.

        Returns:
        - The JSON response from the API.
        """
        return super(Entry, self).get(
            f"/projects/{project_id}/entries.json?start_date={start_date}&end_date={end_date}"
        )


class Task(Resource):
    def __init__(self, token: str, user: str, sub_id: str):
        """
        Initialize a new Task object with the given sub_id and token.

        Args:
        - sub_id: The TickSpot subscription ID.
        - token: The authorization token for the TickSpot API.
        """
        self.sub_id = sub_id
        self.token = token
        self.user = user

    def list(self, project_id: int) -> List[Dict]:
        """
        Get a list of tasks available to the user.

        Args:
        - project_id: The ID of a specific TickSpot project. If provided, only tasks belonging to the project will be returned.

        Returns:
        - A list of dictionaries containing information on each task available to the user.
        """
        if project_id:
            return super(Task, self).list(f"/projects/{project_id}/tasks.json")
        else:
            return super(Task, self).list("tasks.json")

    def get(self, task_id: int) -> Dict:
        """
        Get information on a specific task.

        Args:
        - task_id: The ID of the task to retrieve information on.

        Returns:
        - A dictionary containing information on the task.
        """
        return super(Task, self).get(f"/tasks/{task_id}.json")


class Project(Resource):
    def __init__(self, token: str, user: str, sub_id: str):
        """
        Initialize a new Project object with the given sub_id and token.

        Args:
        - sub_id: The TickSpot subscription ID.
        - token: The authorization token for the TickSpot API.
        """
        self.sub_id = sub_id
        self.token = token
        self.user = user

    def list(self) -> Dict:
        """
        Get a list of projects.

        Returns:
        - The JSON response from the API.
        """
        return super(Project, self).list("projects.json")

    def get(self, project_id: int) -> Dict:
        """
        Get information on a specific project.

        Args:
        - project_id: The ID of the project to retrieve information on.

        Returns:
        - The JSON response from the API.
        """
        return super(Project, self).get(f"/projects/{project_id}.json")
