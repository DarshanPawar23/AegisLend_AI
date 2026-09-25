import os

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from storage.mysql.connection import get_db
from storage.mysql.models.customer_session import CustomerSession

security = HTTPBearer()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    if not JWT_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="JWT configuration is missing."
        )

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    customer_id = payload.get("sub")
    session_id = payload.get("session_id")

    if not customer_id or not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication payload.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    try:
        customer_id = int(customer_id)
        session_id = int(session_id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication identity.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    statement = select(CustomerSession).where(
        CustomerSession.session_id == session_id,
        CustomerSession.customer_id == customer_id
    )

    session = db.execute(statement).scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticated session not found.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if session.session_status != "ACTIVE":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session is no longer active.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return {
        "customer_id": customer_id,
        "session_id": session_id
    }


def get_current_customer_id(
    current_user: dict = Depends(get_current_user)
):
    return current_user["customer_id"]