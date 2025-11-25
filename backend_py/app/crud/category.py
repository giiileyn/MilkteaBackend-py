from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

# Create a category
async def create_category(db: AsyncIOMotorDatabase, category_data: dict):
    result = await db.categories.insert_one(category_data)
    category = await db.categories.find_one({"_id": result.inserted_id})
    category["id"] = str(category["_id"])
    return category

# Get all categories
async def get_categories(db: AsyncIOMotorDatabase):
    cursor = db.categories.find({})
    categories = [{"id": str(c["_id"]), "name": c["name"], "description": c.get("description", "")} async for c in cursor]
    return categories

# Get category by ID
async def get_category(db: AsyncIOMotorDatabase, category_id: str):
    category = await db.categories.find_one({"_id": ObjectId(category_id)})
    if category:
        category["id"] = str(category["_id"])
    return category

# Update category
async def update_category(db: AsyncIOMotorDatabase, category_id: str, update_data: dict):
    await db.categories.update_one({"_id": ObjectId(category_id)}, {"$set": update_data})
    updated = await get_category(db, category_id)
    return updated

# Delete category
async def delete_category(db: AsyncIOMotorDatabase, category_id: str):
    result = await db.categories.delete_one({"_id": ObjectId(category_id)})
    return result.deleted_count
