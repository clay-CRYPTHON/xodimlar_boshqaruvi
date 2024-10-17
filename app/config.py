from pydantic import BaseSettings

class Settings(BaseSettings):
    authjwt_secret_key: str = '17cb375a51388e9d5efa64c3cc84afd3f90c993e3f3dde5850e9bd6429da6fad'
    DATABASE_URL: str = "postgresql://postgres:abbossetdarov@localhost:5432/xodimlar-boshqaruvi_db"
    authjwt_access_token_expires: int = 15  # Access token muddati minutlarda
    authjwt_refresh_token_expires: int = 1440  # Refresh token muddati minutlarda

    class Config:
        env_file = ".env"