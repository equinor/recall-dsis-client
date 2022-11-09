from typing import List

from src.repositories.log_interface import LogInterface
from src.repositories.get_repository import get_dsis_log_repository


def write_log_headers_to_file(attributes: List[str],
                              project: str,
                              file_path: str,
                              log_repository: LogInterface = get_dsis_log_repository()):
    """
    GET selected log attributes from all logs at input project and
    write the data to input file path as csv file.
    """
    # GET generate header chunks of all logs in input project
    log_headers = log_repository.get_dataframe(project=project)

    # Append each header chunk to input file
    with open(file_path, 'w') as file:
        file.write(",".join(attributes) + "\n")
        for dataframe in log_headers:
            # Extract desired attributes
            extract_attributes = dataframe.loc[:, attributes]
            extract_attributes.to_csv(file, mode='a', index=False, header=False)
