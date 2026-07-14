from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import computed_field
from pydantic_core import MultiHostUrl

class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file=".env",env_ignore_empty=True,extra="ignore")
    ENVIRONMENT:str="developmemnt"
    PROJECT_NAME:str
    LOG_LEVEL:str="INFO"
    POSTGRES_USER:str
    POSTGRES_PASSWORD:str
    POSTGRES_DB:str
    POSTGRES_HOST:str
    POSTGRES_PORT:int
    SECRET_KEY:str
    ALGORITHM:str="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES:int=60
    @computed_field
    @property
    def DATABASE_URL(self)->str:
        return str(MultiHostUrl.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB

        ))
settings=Settings()