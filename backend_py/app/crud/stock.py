from app.database import db

async def get_all_stock():
    """
    Retrieve all products with their stock counts
    """
    cursor = db.products.find({}, {"name": 1, "stock": 1})
    return [{"id": str(p["_id"]), "name": p["name"], "stock": p["stock"]} async for p in cursor]

async def get_low_stock(threshold: int = 5):
    """
    Retrieve products with stock less than or equal to threshold
    """
    cursor = db.products.find({"stock": {"$lte": threshold}}, {"name": 1, "stock": 1})
    return [{"id": str(p["_id"]), "name": p["name"], "stock": p["stock"]} async for p in cursor]

async def update_stock(product_id: str, new_stock: int):
    """
    Update stock of a product
    """
    from bson import ObjectId

    result = await db.products.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": {"stock": new_stock}}
    )
    return result.modified_count
