from fastapi import APIRouter,Depends

from .crud.root import router as crud_router
from .auth import router as auth_router
from .v1.root import router as v1_router

router = APIRouter() 
router.include_router(crud_router)
router.include_router(auth_router)
router.include_router(v1_router)

@router.get("/")
def root(): 
    return "health_check"