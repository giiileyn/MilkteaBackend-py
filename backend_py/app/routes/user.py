from fastapi import APIRouter, HTTPException, Form, UploadFile, File, Form
from bson import ObjectId
from bson.errors import InvalidId
from app.crud import user as user_crud
from app.database import db
import shutil, os, uuid
from passlib.context import CryptContext

router = APIRouter()
UPLOAD_FOLDER = "./uploads"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
MAX_BCRYPT_LENGTH = 72  

@router.get("/", summary="Get all users")
async def fetch_users():
    try:
        users = await user_crud.get_all_users()
        return {"success": True, "data": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}", summary="Get user by ID")
async def fetch_user(user_id: str):
    try:
        user = await user_crud.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"success": True, "data": user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========================
# DELETE USER ENDPOINT
# ========================
@router.delete("/{user_id}", summary="Delete user by ID")
async def delete_user(user_id: str):
    try:
        # Validate ObjectId
        try:
            obj_id = ObjectId(user_id)
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid user ID format")

        # Delete user
        result = await db.users.delete_one({"_id": obj_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")

        return {"success": True, "message": f"User {user_id} deleted successfully"}

    except Exception as e:
        print("Delete user error:", e)  # prints error to console for debugging
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{user_id}", summary="Update user by ID")
async def update_user(
    user_id: str,
    name: str = Form(...),
    email: str = Form(...),
    avatar: UploadFile | None = File(None)
):
    try:
        try:
            obj_id = ObjectId(user_id)
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid user ID")

        update_data = {"name": name, "email": email}

        # Handle avatar upload
        if avatar:
            file_ext = avatar.filename.split(".")[-1]
            unique_name = f"{uuid.uuid4()}.{file_ext}"
            file_path = os.path.join(UPLOAD_FOLDER, unique_name)

            with open(file_path, "wb") as f:
                shutil.copyfileobj(avatar.file, f)

            update_data["avatar"] = f"/uploads/{unique_name}"

        # Update user in DB
        result = await db.users.update_one({"_id": obj_id}, {"$set": update_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="User not found")

        # Return updated user
        user = await db.users.find_one({"_id": obj_id})
        user["id"] = str(user["_id"])
        user.pop("_id", None)
        return {"success": True, "data": user}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# ==============================
# Change Password Endpoint
# ==============================
@router.patch("/{user_id}/password", summary="Change user password")
async def change_password(
    user_id: str,
    current_password: str = Form(...),
    new_password: str = Form(...)
):
    try:
        # Truncate passwords to avoid bcrypt error
        current_password = current_password[:MAX_BCRYPT_LENGTH]
        new_password = new_password[:MAX_BCRYPT_LENGTH]

        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Verify current password
        if not pwd_context.verify(current_password, user["password"]):
            raise HTTPException(status_code=400, detail="Current password is incorrect")

        # Hash new password
        hashed_password = pwd_context.hash(new_password)

        # Update user password in DB
        await db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"password": hashed_password}})

        return {"success": True, "message": "Password updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))