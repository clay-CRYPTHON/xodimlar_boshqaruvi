from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from app.routers.auth import auth_router
from app.routers.employees import employees_router

app = FastAPI()
app.include_router(
    auth_router,
    prefix="/auth",
)
app.include_router(
    employees_router,
    prefix="/employees",
)

class Settings(BaseModel):
    authjwt_secret_key: str = '17cb375a51388e9d5efa64c3cc84afd3f90c993e3f3dde5850e9bd6429da6fad'
    authjwt_access_token_expires: int = 15  # minutlarda
    authjwt_refresh_token_expires: int = 1440  # minutlarda

@AuthJWT.load_config
def get_config():
    return Settings()


@app.get('/')
async def root():
    return {"message": "Hi, This is 'Xodimlar Boshqaruvi' project"}