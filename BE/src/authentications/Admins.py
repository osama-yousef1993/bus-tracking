from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from hash import HashHelper

app = FastAPI()

fake_users_db = {
    "admin_user": {
        "username": "admin_user",
        "hashed_password": HashHelper.hash_password("adminpass"),
        "role": "admin",
    },
    "student_user": {
        "username": "student_user",
        "hashed_password": HashHelper.hash_password("studentpass"),
        "role": "student",
    },
    "driver_user": {
        "username": "driver_user",
        "hashed_password": HashHelper.hash_password("driverpass"),
        "role": "driver",
    },
}

# not sure about these settings
SECRET_KEY = "your-jwt-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# class withing a function for the auth user/ a cfucntion instead of depends calls tpye instead of depends and depeds


# getting users from the database
def get_user(db, username: str):
    user = db.get(username)
    if user:
        return user


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not HashHelper.verify_password(password, user["hashed_password"]):
        return False
    return user


# creatin JWT token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = {"username": username}
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data["username"])
    if user is None:
        raise credentials_exception
    return user


async def get_current_user_role(current_user: dict = Depends(get_current_user)):
    return current_user["role"]


@app.get("/secure-data")
async def secure_data(role: str = Depends(get_current_user_role)):
    if role == "admin":
        return {"message": "Hello Admin!"}
    elif role == "student":
        return {"message": "Hello Student!"}
    elif role == "driver":
        return {"message": "Hello Driver!"}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have sufficient privileges",
        )


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
