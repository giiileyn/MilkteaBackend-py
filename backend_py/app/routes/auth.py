from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.models.user import UserResponse
from app.crud.user import create_user
from app.utils.cloudinary_utils import upload_avatar
from app.database import users_collection
from passlib.hash import bcrypt

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    avatar: UploadFile = File(None),
):
    # Check if email already exists
    existing_user = await users_collection.find_one({"email": email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Upload avatar
    avatar_url = None
    if avatar:
        avatar_url = upload_avatar(avatar.file)

    # Hash password
    hashed_password = bcrypt.hash(password)

    user_data = {
        "name": name,
        "email": email,
        "password": hashed_password,
        "avatar": avatar_url,
    }

    created_user = await create_user(user_data)
    return created_user
