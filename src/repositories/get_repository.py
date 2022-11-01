from src.repositories.log_interface import LogInterface
from src.repositories.dsis_log import DSISLog


def get_dsis_log_repository() -> LogInterface:
    """
    Instantiate a log repositories to get log data from Recall.
    """
    return DSISLog()
