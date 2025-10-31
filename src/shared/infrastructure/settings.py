from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Configs existentes
    AUTH0_DOMAIN: str
    AUTH0_CLIENT_ID: str
    AUTH0_CLIENT_SECRET: str
    AUTH0_AUDIENCE: str
    AUTH0_ALGORITHMS: str
    DATABASE_URL: str

    culqi_public_key: str | None = None
    culqi_private_key: str | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"  
        

settings = Settings()
