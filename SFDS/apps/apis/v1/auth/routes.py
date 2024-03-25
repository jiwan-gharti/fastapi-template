
from pydantic import EmailStr
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status, APIRouter

from apps.core.models import Users
from apps.config.db.conn import get_db
from apps.security.auth import jwt_service
from apps.core.schemas.auth import LoginResponse
from apps.core.schemas.user import UserCreateSchema

router = APIRouter(prefix='/auth')

@router.post("/login", response_model=LoginResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login route """

    user = jwt_service.authenticate_user(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    data = {
        "id": user.id,
        "email": user.email,
        "role": user.role,
    }
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "access_token": jwt_service.create_access_token(data),
        "refresh_token": jwt_service.create_refresh_token(data),
        "token_type": "Bearer"
    }



@router.post("/register")
async def get_users(
    user: UserCreateSchema,
    db: Session = Depends(get_db)
):
    """Register route """

    db_item_data = user.model_dump(exclude_unset=True)
    password = db_item_data.pop("password")
    hash_password = jwt_service.get_password_hash(password)
    db_item_data["password"] = hash_password

    obj = Users(**db_item_data)
    try:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    except IntegrityError as e:
        return {"message": "Email already exists"}, 404
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")



@router.post("/token/access_token", response_model=dict)
async def refresh_access_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """
    Get access token using refresh token

    :param refresh_token: secret refresh token
    :param db: Optional, database connection default: Depends(get_db)
    :return: access token and token type
    """

    user = jwt_service.validate_refresh_access_token(db=db, refresh_token=refresh_token)
    data = {
        "id": user.id,
        "email": user.email,
        "role": user.role,
    }
    return {
        "access_token": jwt_service.create_access_token(data),
        "token_type": "Bearer"
    }


@router.post("/reset_password", response_model=dict)
async def forget_password(
    email: EmailStr = Depends(),
    db: Session = Depends(get_db)
):
    """
        Forget password reset api

        :param email: EmailStr
        :param db: Database connection
        :return: dict, success message
    """


    user = jwt_service.get_user(db=db, email=email)

    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    # TODO: SEND FORGET PASSWORD LINK

    return {"message": "Successfully send password reset link in your mail."}



@router.post("/change_password", response_model=dict)
async def change_password(
    old_password: str,
    new_password: str,
    user: Users = Depends(jwt_service.get_current_user),
    db: Session = Depends(get_db)
):
    if not jwt_service.verify_password(old_password, user.password):
        raise HTTPException(
            status_code=404,
            detail="Incorrect Old password"
        )

    new_hash_password = jwt_service.hash_password(new_password)

    user.password = new_hash_password
    db.add(user)
    db.commit()

    return {"message":"Password changed successfully"}