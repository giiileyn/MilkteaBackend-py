from app.database import db

async def get_dashboard_stats():
    orders_count = await db.orders.count_documents({})
    users_count = await db.users.count_documents({})
    products_count = await db.products.count_documents({})

    pipeline = [
        {"$unwind": "$products"},
        {"$group": {"_id": "$products.productId", "totalSold": {"$sum": "$products.quantity"}}},
        {"$sort": {"totalSold": -1}},
        {"$limit": 5},
        {"$lookup": {
            "from": "products",
            "localField": "_id",
            "foreignField": "_id",
            "as": "product"
        }},
        {"$unwind": "$product"},
        {"$project": {"name": "$product.name", "quantity": "$totalSold"}}
    ]

    top_products_cursor = db.orders.aggregate(pipeline)
    top_products = [p async for p in top_products_cursor]

    if top_products:
        max_qty = max(p["quantity"] for p in top_products)
        for p in top_products:
            p["percentage"] = int((p["quantity"] / max_qty) * 100)

    return {
        "orders": orders_count,
        "users": users_count,
        "products": products_count,
        "topProducts": top_products
    }

async def get_low_stock():
    cursor = db.products.find({"stock": {"$lte": 5}}, {"name": 1, "stock": 1})
    return [p async for p in cursor]
