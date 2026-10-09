from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import verify_password, hash_password, create_access_token, decode_access_token
from app.models.user import User
from app.models.student import Student
from app.models.faculty import Faculty
from app.schemas.auth import LoginRequest, TokenResponse, UserRegisterRequest, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate authentication credentials or token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User account is inactive or not found")
    return user

def require_role(allowed_roles: List[str]):
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: Requires role in {allowed_roles}, your role is {current_user.role}"
            )
        return current_user
    return role_checker

@router.post("/login", response_model=TokenResponse)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.username.lower().strip()).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    student_id = user.student_profile.id if user.student_profile else None
    faculty_id = user.faculty_profile.id if user.faculty_profile else None

    token_data = {
        "sub": str(user.id),
        "role": user.role,
        "email": user.email,
        "name": user.name
    }
    access_token = create_access_token(token_data)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        role=user.role,
        name=user.name,
        email=user.email,
        user_id=user.id,
        student_id=student_id,
        faculty_id=faculty_id
    )

@router.post("/register", response_model=UserResponse)
def register(request: UserRegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == request.email.lower().strip()).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    new_user = User(
        email=request.email.lower().strip(),
        hashed_password=hash_password(request.password),
        name=request.name.strip(),
        role=request.role.lower().strip()
    )
    db.add(new_user)
    db.flush()

    if new_user.role == "student":
        roll = request.roll_number or f"21CSE{100 + new_user.id}"
        student = Student(
            user_id=new_user.id,
            roll_number=roll,
            department=request.department or "Computer Science & Engineering",
            year=request.year or 4,
            semester=request.semester or 7,
            section=request.section or "A",
            cgpa=request.cgpa,
            backlogs=request.backlogs
        )
        db.add(student)
    elif new_user.role == "faculty":
        emp_id = f"FAC{200 + new_user.id}"
        faculty = Faculty(
            user_id=new_user.id,
            employee_id=emp_id,
            department=request.department or "Computer Science & Engineering",
            designation="Assistant Professor"
        )
        db.add(faculty)

    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
        "student_id": current_user.student_profile.id if current_user.student_profile else None,
        "faculty_id": current_user.faculty_profile.id if current_user.faculty_profile else None
    }
