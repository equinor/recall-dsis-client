from typing import Callable
import functools
import requests
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
    A simple DSIS client to GET data and metadata of common entities in Recall.
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
    def _get_entities_list(self, project: str, entity: str, query: str = "$format=json") -> dict:
        """
        GET list of all entities at input project, with given query string
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
    def _get_entity_metadata(self, project: str, entity: str, entity_id: str, query: str = "$format=json") -> dict:
        """
        GET metadata of entity with given id at input project.
        """
        url = f"{self.base_url[self.native]}/{project}/{entity}('{entity_id}')?{query}"
        print(f"GET request to {url}")
        response = requests.get(
            url=url, verify=False, headers={"Authorization": f"Bearer {self.token}"}
        )
        print("DONE")
        json = response.json(strict=False)
        return json

    def get_wells_list(self, project: str, query: str = "$format=json") -> dict:
        """
        GET list of all wells at input project.
        """
        return self._get_entities_list(project, self.well[self.native], query=query)

    def get_curves_list(self, project: str, query: str = "$format=json") -> dict:
        """
        GET list of all curves at input project.
        """
        return self._get_entities_list(project, self.curve[self.native], query=query)

    def get_logs_list(self, project: str, query: str = "$format=json") -> dict:
        """
        GET list of all logs at input project.
        """
        return self._get_entities_list(project, self.log[self.native], query=query)

    def get_well_metadata(self, project: str, well_id: str, query: str = "$format=json") -> dict:
        """
        GET metadata of well with given id at input project.
        """
        return self._get_entity_metadata(project, self.well[self.native], well_id, query=query)

    def get_curve_metadata(self, project: str, curve_id: str, query: str = "$format=json") -> dict:
        """
        GET metadata of curve with given id at input project.
        """
        return self._get_entity_metadata(project, self.curve[self.native], curve_id, query=query)

    def get_log_metadata(self, project: str, log_id: str, query: str = "$format=json") -> dict:
        """
        GET metadata of log with given id at input project.
        """
        return self._get_entity_metadata(project, self.log[self.native], log_id, query=query)
