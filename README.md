# Recall DSIS client

## Python environment
Setup Python venv:
```
python3 -m venv venv
```
Activate venv:
```
source venv/bin/activate
```
Install Poetry:
```
pip install poetry
```
Install dependencies:
```
poetry install
```

## Authenticate
Setup secrets folder:
```
mkdir -p secrets && cp -a secrets.template/. secrets/
```

Type Equinor username and password into `secrets/user_id`
and `secrets/password` to automatically authenticate all DSIS
requests.