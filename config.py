from pydantic import BaseSettings


class Settings(BaseSettings):
    user_id: str
    password: str

    class Config:
        secrets_dir = "secrets"


# Instantiate
config = Settings()
