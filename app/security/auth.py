from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from passlib.context import CryptContext

# Secret key & algorithm for JWT
SECRET_KEY = "9eb5d957c411fc2ecd9afdb92464134685011988fbb6b4d919a6d3c723b6c49b922b914f390f79aa6b303119b5fc9b5d22536f29377b4822fa37309add6152f851f02354efd12f4f933001114f89f0ebb1a6f4f7f32bf566ed1cc20312dc791859df930e1233e10790379aa0a1a2195021e18720ded72ac5b3eb40d135a545f6072d64f6e9ab19e5a8fef11030dfb736285ff66ee32008c4f88f44043a91d1d66c576eed20ed43dbd9fc53809b778f2767d08a46137366795b184ac3b7875317b311057829b137b62cafd9d7283b2e16e8daf6a61a14f67104cc67b11132b12f2043ca7bebe47db803ea2af557061f432f6fcde41f3e50012632dfccfcc9b715"  # Change this to a strong secret in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

ENDPOINT_ACCESS_RULES = {
    "/items/": ["admin", "guest"],
    "/users/": ["admin"],
}

# Hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Generate JWT token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Decode JWT token
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return {"username": username, "role": role}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
def restrict_users_for(request: Request,user: dict=Depends(verify_token)):
    path = request.url.path
    allowed_users = ENDPOINT_ACCESS_RULES.get(path,[])
    if user["role"] not in allowed_users:
        raise HTTPException(status_code=403, detail= "Unauthorized for this path")
    return user