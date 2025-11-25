# D:\Bsit-ns-4a\milkTea\backend\backend_py\app\crud\dashboard.py
from app.database import db

async def get_dashboard_stats():
    users_count = await db.users.count_documents({})
    orders_count = await db.orders.count_documents({})
    products_count = await db.products.count_documents({})

    return {
        "users": users_count,
        "orders": orders_count,
        "products": products_count,
        "topProducts": []  # Optional: add top-selling products later
    }

async def get_low_stock():
    cursor = db.products.find({"stock": {"$lte": 5}}, {"name": 1, "stock": 1})
    return [p async for p in cursor]
