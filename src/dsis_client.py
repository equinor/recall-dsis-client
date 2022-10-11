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
    """

    base_url_common: str = (
        "https://dsdata01.qa.dsis.equinor.com:8443/dsdataserver/dsl.svc"
        "/RecallCommonModel/500010/RecallCommonModel_OFDB_RecallProd-RecallProd"
    )
    base_url_native: str = (
        "https://dsdata01.qa.dsis.equinor.com:8443/dsdataserver/dsl.svc"
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
    def _get_entities_list(self, project: str, entity: str) -> list:
        """
        GET list of all entities at input project.
        """
        url = f"{self.base_url[self.native]}/{project}/{entity}?$format=json"
        print(f"GET request to {url}")
        response = requests.get(
            url=url, verify=False, headers={"Authorization": f"Bearer {self.token}"}
        )
        print("DONE")
        json = response.json(strict=False)
        return json.get("value")

    @_authenticate
    def _get_entity_metadata(self, project: str, entity: str, entity_id: str) -> list:
        """
        GET metadata of entity with given id at input project.
        """
        url = f"{self.base_url[self.native]}/{project}/{entity}('{entity_id}')?$format=json"
        print(f"GET request to {url}")
        response = requests.get(
            url=url, verify=False, headers={"Authorization": f"Bearer {self.token}"}
        )
        print("DONE")
        json = response.json(strict=False)
        return json

    @_authenticate
    def get_example(self):
        """
        GET metadata of entity with given id at input project.
        """
        url = (
            "https://dsdata01.qa.dsis.equinor.com:8443/dsdataserver/dsl.svc/recall/500010/"
            "recall_RecallProd-RecallProd/NORWAY_WELLDB/WELL('2/1')?$format=json&$expand=LOG"
        )
        print(f"GET request to {url}")
        response = requests.get(
            url=url, verify=False, headers={"Authorization": f"Bearer {self.token}"}
        )
        print("DONE")
        json = response.json(strict=False)
        return json

    def get_wells_list(self, project: str) -> list:
        """
        GET list of all wells at input project.
        """
        return self._get_entities_list(project, self.well[self.native])

    def get_curves_list(self, project: str) -> list:
        """
        GET list of all curves at input project.
        """
        return self._get_entities_list(project, self.curve[self.native])

    def get_logs_list(self, project: str) -> list:
        """
        GET list of all logs at input project.
        """
        return self._get_entities_list(project, self.log[self.native])

    def get_well_metadata(self, project: str, well_id: str) -> list:
        """
        GET metadata of well with given id at input project.
        """
        return self._get_entity_metadata(project, self.well[self.native], well_id)

    def get_curve_metadata(self, project: str, curve_id: str) -> list:
        """
        GET metadata of curve with given id at input project.
        """
        return self._get_entity_metadata(project, self.curve[self.native], curve_id)

    def get_log_metadata(self, project: str, log_id: str) -> list:
        """
        GET metadata of log with given id at input project.
        """
        return self._get_entity_metadata(project, self.log[self.native], log_id)
