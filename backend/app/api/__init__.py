from app.api.auth import router as auth_router
from app.api.bfi2 import router as bfi2_router
from app.api.users import router as users_router

__all__ = ["auth_router", "bfi2_router", "users_router"]
