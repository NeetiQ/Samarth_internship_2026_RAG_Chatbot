from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from jose import jwt
from datetime import datetime, timedelta

from sqlalchemy import create_engine, text

# =====================
# NEON DB
# =====================
DATABASE_URL = "postgresql://neondb_owner:npg_1U8ZTzsqBNuQ@ep-silent-grass-atrorq50-pooler.c-9.us-east-1.aws.neon.tech/neondb?sslmode=require"

engine = create_engine(DATABASE_URL)

# =====================
# JWT CONFIG
# =====================
SECRET_KEY = "super_secret_key_123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# =====================
# APP
# =====================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================
# MODELS
# =====================
class AuthRequest(BaseModel):
    email: str
    password: str

# =====================
# TOKEN
# =====================
def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=1)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# =====================
# REGISTER API (FIXED)
# =====================
@app.post("/register")
def register(user: AuthRequest):

    with engine.begin() as conn:

        # check if user exists
        check = conn.execute(
            text("SELECT * FROM users WHERE email = :email"),
            {"email": user.email}
        ).fetchone()

        if check:
            raise HTTPException(status_code=400, detail="User already exists")

        # insert user
        conn.execute(
            text("""
                INSERT INTO users (email, password_hash)
                VALUES (:email, :password)
            """),
            {"email": user.email, "password": user.password}
        )

    return {"message": "User registered successfully"}

# =====================
# LOGIN API
# =====================
@app.post("/login")
def login(user: AuthRequest):

    with engine.connect() as conn:

        db_user = conn.execute(
            text("SELECT * FROM users WHERE email = :email"),
            {"email": user.email}
        ).fetchone()

        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        if db_user.password_hash != user.password:
            raise HTTPException(status_code=401, detail="Wrong password")

        token = create_token({"sub": user.email})

        return {
            "access_token": token,
            "token_type": "bearer"
        }

# =====================
# TEST ROUTE
# =====================
@app.get("/")
def root():
    return {"message": "Backend running"}
