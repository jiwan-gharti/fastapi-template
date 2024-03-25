from datetime import timedelta, datetime, timezone

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt
from starlette import status

from apps.config import settings
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from apps.config.db.conn import get_db
from apps.core.models import Users


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class JWTSecurity(object):
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.SECRET_KEY = settings.SECRET_KEY
        self.ALGORITHM = settings.ALGORITHM
        self.ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.REFRESH_TOKEN_TIME_IN_MINUTES = settings.REFRESH_TOKEN_TIME_IN_MINUTES


        # self.db: Session = get_db()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)


    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def get_user(self, email: str, db: Session):
        return db.query(Users).filter(Users.email == email ).first()

    def authenticate_user(self, email: str, password: str, db: Session):
        user = self.get_user(email=email, db=db)

        if not user:
            return False

        if not self.verify_password(password, user.password):
            return False

        return user

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt


    def create_refresh_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        to_encode.update({"token": "refresh"})
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def get_current_user(self,db: Session, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email: str = payload.get("email")
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = self.get_user(email=email, db=db)
        if user is None:
            raise credentials_exception
        return user

    def validate_refresh_access_token(self, db: Session, refresh_token: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email: str = payload.get("email")
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        try:
            refresh_token = payload.get("token")
            if not refresh_token:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        user = self.get_user(email=email, db=db)

        if user is None:
            raise credentials_exception

        return user


jwt_service = JWTSecurity()


