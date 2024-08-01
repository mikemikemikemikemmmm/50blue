from fastapi import APIRouter
from .drink import router as drink_router
from .order import router as order_router
# from .store import router as store_router
from .topping import router as topping_router
from .user import router as user_router
router = APIRouter(prefix="/crud") 
router.include_router(drink_router)
router.include_router(order_router)
# router.include_router(store_router)
router.include_router(topping_router)
router.include_router(user_router)