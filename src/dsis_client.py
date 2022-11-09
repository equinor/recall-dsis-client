from typing import Callable
import functools
import requests
import json
from requests.exceptions import HTTPError

from src.authenticate import get_token


def _authenticate(method: Callable) -> Callable:
    """
    Decorate methods in DSISClient with @_authenticate
    to always have a valid DSIS access token.
    """

    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        self = args[0]
        try:
            return method(*args, **kwargs)
        except HTTPError as e:
            if e.response.status_code == 401:
                self._update_token()
                return method(*args, **kwargs)
            raise e

    return wrapper


class DSISRecallClient:
    """
    A simple DSIS client to GET data and header of common entities in Recall.
    The data in Recall is split into projects, e.g. NORWAY_WELLDB, a project in norway.
    """

    base_url_common: str = (
        "https://gate.dsis.equinor.com/dsdataserver/dsl.svc"
        "/RecallCommonModel/500010/RecallCommonModel_OFDB_RecallProd-RecallProd"
    )
    base_url_native: str = (
        "https://gate.dsis.equinor.com/dsdataserver/dsl.svc"
        "/recall/500010/recall_RecallProd-RecallProd"
    )
    base_url: dict = {True: base_url_native, False: base_url_common}

    well: dict = {True: "WELL", False: "Well"}

    curve: dict = {True: "CURVE", False: "LogCurve"}

    log: dict = {True: "LOG", False: "WellLog"}

    def __init__(self, native: bool = False):
        """
        native=False defaults to common model client, whereas native=True creates a native model client.
        """
        self.token = get_token()
        self.native = native

    def _update_token(self):
        self.token = get_token()

    @_authenticate
    def _get_all_entities(self, project: str, entity: str, query: str = "$format=json") -> dict:
        """
        GET dictionary containing all entities at input project, with given query string
        which defaults to $format=json.
        """
        url = f"{self.base_url[self.native]}/{project}/{entity}?{query}"
        print(f"GET request to {url}")
        response = requests.get(
            url=url, verify=False, headers={"Authorization": f"Bearer {self.token}"}
        )
        print("DONE")
        json = response.json(strict=False)
        return json

    @_authenticate
    def _get_entity_header(self, project: str, entity: str, entity_id: str, query: str = "$format=json") -> dict:
        """
        GET header of entity with given id at input project.
        """
        url = f"{self.base_url[self.native]}/{project}/{entity}('{entity_id}')?{query}"
        print(f"GET request to {url}")
        response = requests.get(
            url=url, verify=False, headers={"Authorization": f"Bearer {self.token}"}
        )
        print("DONE")
        json = response.json(strict=False)
        return json

    def get_all_wells(self, project: str, query: str = "$format=json") -> dict:
        """
        GET dictionary containing all wells at input project.
        """
        return self._get_all_entities(project, self.well[self.native], query=query)

    def get_all_curves(self, project: str, query: str = "$format=json") -> dict:
        """
        GET dictionary containing all curves at input project.
        """
        return self._get_all_entities(project, self.curve[self.native], query=query)

    def get_all_logs(self, project: str, query: str = "$format=json") -> dict:
        """
        GET dictionary containing all logs at input project.
        """
        return self._get_all_entities(project, self.log[self.native], query=query)

    def get_well_header(self, project: str, well_id: str, query: str = "$format=json") -> dict:
        """
        GET header of well with given id at input project.
        """
        return self._get_entity_header(project, self.well[self.native], well_id, query=query)

    def get_curve_header(self, project: str, curve_id: str, query: str = "$format=json") -> dict:
        """
        GET header of curve with given id at input project.
        """
        return self._get_entity_header(project, self.curve[self.native], curve_id, query=query)

    def get_log_header(self, project: str, log_id: str, query: str = "$format=json") -> dict:
        """
        GET hedaer of log with given id at input project.
        """
        return self._get_entity_header(project, self.log[self.native], log_id, query=query)

    @_authenticate
    def get_all_project_names(self) -> list:
        """
        Get a list of all project names found in DSIS.
        """
        url = f"{self.base_url[self.native]}?$format=json"
        response = requests.get(
            url=url, verify=False, headers={"Authorization": f"Bearer {self.token}"}
        )
        json_response = json.loads(response.content)
        project_names = [project["ProjectName"] for project in json_response["value"]]

        return project_names
