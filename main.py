import urllib3
from src.dsis_client import DSISRecallClient


if __name__ == "__main__":

    # Disable SSL warning
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Create DSIS common model client:
    common_client = DSISRecallClient(native=False)
    # Create DSIS native client:
    native_client = DSISRecallClient(native=True)
    # project
    project = "NORWAY_WELLDB"

    # GET all logs metadata in NORWAY_WELLDB
    logs_native = native_client.get_logs_list(project)
    print(logs_native[0])
