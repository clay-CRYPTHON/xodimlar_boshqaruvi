from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT

def require_role(required_role: str):
    def role_required(Authorize: AuthJWT = Depends()):
        Authorize.jwt_required()
        user_role = Authorize.get_raw_jwt().get("role")
        if user_role != required_role:
            raise HTTPException(status_code=403, detail="You do not have the required permissions")
    return role_required
