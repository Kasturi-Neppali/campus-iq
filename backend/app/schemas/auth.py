from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    name: str
    email: str
    user_id: int
    student_id: Optional[int] = None
    faculty_id: Optional[int] = None

class UserRegisterRequest(BaseModel):
    email: str
    password: str
    name: str
    role: str  # "student", "faculty", "admin"
    roll_number: Optional[str] = None
    department: Optional[str] = "Computer Science & Engineering"
    year: Optional[int] = 4
    semester: Optional[int] = 7
    section: Optional[str] = "A"

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True
