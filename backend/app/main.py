from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from jose import jwt
from datetime import datetime, timedelta

from sqlalchemy import create_engine, text

# =====================
# DATABASE
# =====================
DATABASE_URL = "postgresql://neondb_owner:npg_1U8ZTzsqBNuQ@ep-silent-grass-atrorq50-pooler.c-9.us-east-1.aws.neon.tech/neondb?sslmode=require"

engine = create_engine(DATABASE_URL)

# =====================
# JWT
# =====================
SECRET_KEY = "super_secret_key_123"
ALGORITHM = "HS256"

# =====================
# FASTAPI
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
# MODEL
# =====================
class AuthRequest(BaseModel):
    email: str
    password: str

# =====================
# JWT TOKEN
# =====================
def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(hours=1)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# =====================
# REGISTER
# =====================
@app.post("/register")
def register(user: AuthRequest):

    with engine.begin() as conn:

        existing = conn.execute(
            text("""
            SELECT id
            FROM app_users
            WHERE email=:email
            """),
            {"email": user.email}
        ).fetchone()

        if existing:
            raise HTTPException(status_code=400, detail="User already exists")

        conn.execute(
            text("""
            INSERT INTO app_users
            (email, hashed_password, is_active, is_superuser)
            VALUES
            (:email, :password, true, false)
            """),
            {
                "email": user.email,
                "password": user.password
            }
        )

    return {"message": "Signup Successful"}

# =====================
# LOGIN
# =====================
@app.post("/login")
def login(user: AuthRequest):

    with engine.connect() as conn:

        db_user = conn.execute(
            text("""
            SELECT *
            FROM app_users
            WHERE email=:email
            """),
            {"email": user.email}
        ).fetchone()

        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        if db_user.hashed_password != user.password:
            raise HTTPException(status_code=401, detail="Incorrect password")

        token = create_token({"sub": user.email})

        return {
            "access_token": token,
            "token_type": "bearer"
        }

# =====================
# TEST
# =====================
@app.get("/")
def root():
    return {"message": "Backend Running Successfully"}