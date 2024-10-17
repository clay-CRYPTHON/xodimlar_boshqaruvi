from fastapi import Depends, APIRouter, HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from sqlalchemy.orm import Session

from app.models import User
from app.database import get_db
from app.schemas import UserCreate, UserLogin, ResetPasswordSchema, EmailSchema

from werkzeug.security import generate_password_hash, check_password_hash

from jose import jwt

from datetime import datetime, timedelta

auth_router = APIRouter()

SECRET_KEY = "d8293e6ec99b89a93d391656362776bac14baeda92051fc78e448f29f0ef5b14"
ALGORITHM = "HS256"

conf = ConnectionConfig(
    MAIL_USERNAME='your-email@gmail.com',
    MAIL_PASSWORD='your-password',
    MAIL_FROM='your-email@gmail.com',
    MAIL_PORT=587,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_FROM_NAME='Xodimlar-Boshqaruvi',
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)

# Example of sending email
message = MessageSchema(
    subject="Hello",
    recipients=["recipient@example.com"],
    body="This is a test email",
    subtype="html"
)


@auth_router.post('/register/')
async def register(user: UserCreate, db:Session = Depends(get_db)):
    user_exists = db.query(User).filter(User.email == user.email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail='Email already registered')

    hashed_password = generate_password_hash(user.password)

    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role,  # Bu yerda .value olib tashlandi
        department=user.department,
        position=user.position,
        status=user.status,  # Bu yerda ham .value olib tashlandi
        employment_type=user.employment_type,  # Bu yerda ham
        is_active=user.is_active
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "status": True,
        "code": 201,
        "message": "User created successfully",
        "data": {
            'id': new_user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "role": user.role,  # Bu yerda .value olib tashlandi
            "department": user.department,
            "position": user.position,
            "status": user.status,  # Bu yerda ham .value olib tashlandi
            "employment_type": user.employment_type,  # Bu yerda ham
            "is_active": user.is_active
        }
    }



@auth_router.post('/login/')
async def login(user: UserLogin, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not check_password_hash(db_user.hashed_password, user.password):
        raise HTTPException(status_code=400, detail='Incorrect email or password')

    # Token yaratish - RoleEnum qiymatini string formatiga o'tkazamiz
    access_token = Authorize.create_access_token(
        subject=db_user.email,
        expires_time=timedelta(minutes=15),  # Qo'lda qiymat berish mumkin
        user_claims={"role": db_user.role.value}  # Enum qiymatini string formatiga o'tkazish
    )
    refresh_token = Authorize.create_refresh_token(
        subject=db_user.email,
        expires_time=timedelta(minutes=1440),
        user_claims={"role": db_user.role.value}
    )

    token = {
        'access_token': access_token,
        'refresh_token': refresh_token,
    }
    response = {
        "status": True,
        "code": 200,
        "message": "You are now logged in",
        "token": token
    }
    return response


@auth_router.post('/refresh')
async def refresh_token(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user, expires_time=timedelta(minutes=10080))
    token = {
        'access_token': new_access_token,
    }
    response = {
        "status": True,
        "code": 200,
        "message": "You refreshed your access token",
        'token': token
    }
    return response


@auth_router.post('/password-reset-request')
async def password_reset_request(user: EmailSchema, db: Session = Depends(get_db)):
    user_email = user.email
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail='Email not found')

    reset_token = jwt.encode({
        "sub": user.email,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }, SECRET_KEY, algorithm=ALGORITHM)

    reset_link = f"http://localhost:8000/auth/password/reset/{reset_token}"

    # Print reset link to terminal
    print(f"Password reset link: {reset_link}")

    # Return the reset link as a response for testing
    return {"message": f"Password reset link (printed in terminal): {reset_link}"}


@auth_router.post("/password/reset/{token}")
async def password_reset_confirm(token: str, reset_data: ResetPasswordSchema, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail='Invalid token')
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail='Token expired')
    except jwt.JWTError:
        raise HTTPException(status_code=400, detail='Invalid token')

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail='Email not found')

    if reset_data.new_password != reset_data.confirm_password:
        raise HTTPException(status_code=400, detail='Passwords do not match')

    user.hashed_password = generate_password_hash(reset_data.new_password)
    db.commit()

    return {"message": "Password updated successfully"}


@auth_router.post('/logout/')
async def logout(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()

        response = {
            "status": True,
            "code": 200,
            "message": "You are now logged out",
        }
        return response
    except Exception as e:
        raise HTTPException(status_code=401, detail="Not authorized")