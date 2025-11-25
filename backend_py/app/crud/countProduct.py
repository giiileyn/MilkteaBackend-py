from app.database import db
from bson import ObjectId

async def get_category_product_counts():
    """
    Returns a list of categories with their respective total product count
    """
    # Get all categories
    cursor = db.categories.find({}, {"_id": 1, "name": 1})
    categories = [{"id": str(c["_id"]), "name": c["name"]} async for c in cursor]

    # For each category, count products
    result = []
    for cat in categories:
        count = await db.products.count_documents({"category": cat["name"]})
        result.append({
            "id": cat["id"],
            "name": cat["name"],
            "total_products": count
        })

    return result
