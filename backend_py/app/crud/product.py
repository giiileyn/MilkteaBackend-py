from app.database import db
from bson import ObjectId

# ================================
#        CRUD PRODUCTS
# ================================

async def get_products():
    cursor = db.products.find()
    products = []
    async for p in cursor:
        p["_id"] = str(p["_id"])  # convert ObjectId to string
        # convert nested ObjectIds if any
        if "toppings" in p:
            p["toppings"] = [str(t) for t in p["toppings"]]
        products.append(p)
    return products

async def get_product(product_id: str):
    product = await db.products.find_one({"_id": ObjectId(product_id)})
    if product:
        product["_id"] = str(product["_id"])
        if "toppings" in product:
            product["toppings"] = [str(t) for t in product["toppings"]]
    return product

async def create_product(data: dict):
    result = await db.products.insert_one(data)
    new_product = await db.products.find_one({"_id": result.inserted_id})
    new_product["_id"] = str(new_product["_id"])
    if "toppings" in new_product:
        new_product["toppings"] = [str(t) for t in new_product["toppings"]]
    return new_product

async def update_product(product_id: str, data: dict):
    await db.products.update_one({"_id": ObjectId(product_id)}, {"$set": data})
    updated_product = await db.products.find_one({"_id": ObjectId(product_id)})
    if updated_product:
        updated_product["_id"] = str(updated_product["_id"])
        if "toppings" in updated_product:
            updated_product["toppings"] = [str(t) for t in updated_product["toppings"]]
    return updated_product

async def delete_product(product_id: str):
    result = await db.products.delete_one({"_id": ObjectId(product_id)})
    return result.deleted_count > 0
