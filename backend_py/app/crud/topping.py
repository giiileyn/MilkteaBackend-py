from app.database import db
from bson import ObjectId

# ================================
#      CRUD OPERATIONS - TOPPING
# ================================

async def get_all_toppings():
    cursor = db.toppings.find()  # <-- use correct collection name
    toppings = []
    async for t in cursor:
        t["_id"] = str(t["_id"])
        toppings.append(t)
    return toppings

async def get_topping(topping_id: str):
    topping = await db.toppings.find_one({"_id": ObjectId(topping_id)})
    if topping:
        topping["_id"] = str(topping["_id"])
    return topping

async def create_topping(data: dict):
    result = await db.toppings.insert_one(data)
    new_topping = await db.toppings.find_one({"_id": result.inserted_id})
    new_topping["_id"] = str(new_topping["_id"])
    return new_topping

async def update_topping(topping_id: str, data: dict):
    await db.toppings.update_one({"_id": ObjectId(topping_id)}, {"$set": data})
    updated_topping = await db.toppings.find_one({"_id": ObjectId(topping_id)})
    if updated_topping:
        updated_topping["_id"] = str(updated_topping["_id"])
    return updated_topping

async def delete_topping(topping_id: str):
    result = await db.toppings.delete_one({"_id": ObjectId(topping_id)})
    return result.deleted_count > 0

