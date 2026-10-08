from app.api.auth import router as auth_router
from app.api.student import router as student_router
from app.api.faculty import router as faculty_router
from app.api.admin import router as admin_router
from app.api.risk import router as risk_router
from app.api.placement import router as placement_router
from app.api.simulator import router as simulator_router
from app.api.campus_ai import router as ai_router

__all__ = [
    "auth_router",
    "student_router",
    "faculty_router",
    "admin_router",
    "risk_router",
    "placement_router",
    "simulator_router",
    "ai_router"
]
