import urllib3

from src.repositories.log_interface import LogInterface
from src.repositories.get_repository import get_dsis_log_repository


if __name__ == "__main__":
    """
    DEMO:
    Get all log headers in NORWAY_WELLDB as pandas dataframe and extract:
    - a subset of attributes
    - STAT logs
    """

    # Disable SSL warning
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Inject implementation of log repository, used to export Recall log data:
    log_repository: LogInterface = get_dsis_log_repository()

    # GET dataframe with header of all logs in project  NORWAY_WELLDB
    log_headers = log_repository.get_dataframe(project="NORWAY_WELLDB")

    # Only include listed attributes in each header
    attributes = ["SOURCE FILE NAME",
                  "SOURCE FILE DIR",
                  "DATE LOGGED",
                  "NAME",
                  "LOGGING CONTRACTOR",
                  "DATA TYPE",
                  "LOG SERVICE",
                  "LOG ACTIVITY",
                  "LOG TYPE",
                  "LOG JOB",
                  "LOG RUN",
                  "LOG PASS",
                  "CASING SIZE MANUAL",
                  "LOG SECTION SIZE",
                  "STATION NUMBER",
                  "STATION DEPTH",
                  "MFC CORRECTION",
                  "DATE STAMP"]

    extract_attributes = log_headers.loc[:, attributes]

    # Finally, only include logs whose name contains "STAT"
    filtered_log_headers = extract_attributes.loc[extract_attributes["NAME"].str.contains("STAT")]

    # Print first three log entries:
    print(filtered_log_headers.loc[0:3, :])
