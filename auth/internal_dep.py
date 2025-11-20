# app/auth/internal_dep.py (en cada microservicio)
import os, jwt
from fastapi import Header, HTTPException

PUBLIC_KEY_PATH = os.getenv("PUBLIC_KEY_PATH", "secrets/bff_public.pem" )

with open(PUBLIC_KEY_PATH, "rb") as f:
    PUBLIC_KEY = f.read()


async def get_internal_principal(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing internal token")
    token = authorization.split(" ", 1)[1]
    try:
        decoded = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            options={"require": ["exp", "iat"]}
        )
        return decoded  # {"iss","sub","iat","exp"}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid internal token")
