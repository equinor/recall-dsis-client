import pandas as pd
from typing import Generator

from src.repositories.log_interface import LogInterface
from src.dsis_client import DSISRecallClient


class DSISLog(LogInterface):
    """
    Implementation of LogInterface using DSIS to query Recall.
    """
    dsis_client = DSISRecallClient(native=True)

    def get_dataframe(self, project: str) -> Generator[pd.DataFrame, None, None]:
        skip = 0
        top = 100
        query = f"$format=json&$skip={skip}&$top={top}"
        response: dict = self.dsis_client.get_all_logs(project=project, query=query)
        content: list = response.get("value")
        is_more_data = len(content) > 0
        while is_more_data:
            log_headers = (_format_log_header(log) for log in content)
            yield pd.DataFrame.from_dict(log_headers)
            skip += 100
            top += 100
            query = f"$format=json&$skip={skip}&$top={top}"
            response: dict = self.dsis_client.get_all_logs(project=project, query=query)
            content: list = response.get("value")
            is_more_data = len(content) > 0

    def get_header(self, project: str, log_id: str) -> dict:
        response = self.dsis_client.get_log_header(project=project, log_id=log_id)
        return _format_log_header(response)

    def get_data(self, project: str, log_id: str) -> dict:
        raise NotImplementedError


def _format_log_header(log: dict) -> dict:
    """
    Reformat the DSIS native log response to a dict/json object.
    """
    # all header info is listed under ExtendedProperties
    header_string = log.get("ExtendedProperties")
    # extendedProperties is formatted as string key=value;key=value;key=value...
    header_list = [item for item in header_string.split(";") if "=" in item]
    header_dict = dict(map(lambda x: x.split("=", 1), header_list))
    return header_dict
