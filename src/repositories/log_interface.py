from abc import ABC, abstractmethod
import pandas as pd


class LogInterface(ABC):
    """
    An interface for log repositories.
    """

    @abstractmethod
    def get_dataframe(self, project: str) -> pd.DataFrame:
        """
        Get a dataframe containing header/metadata of all
        logs at given project.
        """
        pass

    @abstractmethod
    def get_header(self, project: str, log_id: str) -> dict:
        """
        Get header/metadata of the log identified by given project and id.
        """
        pass

    @abstractmethod
    def get_data(self, project: str, log_id: str) -> dict:
        """
        Get the data of the log identified by given project and id.
        """
        pass
