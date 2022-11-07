from abc import ABC, abstractmethod
import pandas as pd
from typing import Generator


class LogInterface(ABC):
    """
    An interface for log repositories.
    """

    @abstractmethod
    def get_dataframe(self, project: str) -> Generator[pd.DataFrame, None, None]:
        """
        Generate dataframes containing header/metadata of all logs at given project.
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
