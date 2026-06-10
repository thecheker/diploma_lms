# Файл: backend/app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Role
from app.schemas import UserRegister, UserLogin, UserOut, Token
from app.auth import hash_password, verify_password, create_access_token

# 🔥 Префикс /auth — итоговый путь: /api/auth/login
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(400, detail=f"Email '{user.email}' уже зарегистрирован")
    
    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password),
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(401, detail="Неверный email или пароль")
    
    role_value = db_user.role.value if hasattr(db_user.role, 'value') else str(db_user.role)
    token = create_access_token(data={"sub": db_user.id}, role=role_value)
    
    return {"access_token": token, "token_type": "bearer"}
