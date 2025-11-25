from fastapi import APIRouter
from app.database import users_collection

router = APIRouter()

@router.get("/dashboard/users-count")
async def get_users_count():
    count = await users_collection.count_documents({})
    return {"users_count": count}
