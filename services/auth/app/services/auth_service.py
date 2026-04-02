from sqlalchemy.orm import Session
from app.db.models import User
from app.core.security import hash_password, verify_password, create_token

def create_user(db: Session, email: str, password: str):
    existing_user = db.query(User).filter(User.email == email).first()
    
    if existing_user:
        return None

    user = User(
        email=email,
        password_hash=hash_password(password)
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password_hash):
        return None

    token = create_token({"user_id": str(user.user_id)})
    return token