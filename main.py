import urllib3

from src.use_cases.logs import write_log_headers_to_file


if __name__ == "__main__":
    """
    DEMO:
    Get all log headers in NORWAY_WELLDB as pandas dataframe 
    and write a subset of attributes to a csv file
    """

    # Disable SSL warning
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Select a project:
    project = "NORWAY_WELLDB"

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

    write_log_headers_to_file(attributes=attributes, project=project, file_path="data/test.csv")
