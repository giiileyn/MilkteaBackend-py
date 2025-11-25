from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os, shutil, uuid
from dotenv import load_dotenv
from typing import Optional

# Load environment variables first
load_dotenv()

# FastAPI app instance
app = FastAPI()

# Database connection
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "milktea")

client = AsyncIOMotorClient(MONGODB_URI)
db = client[DB_NAME]

# Create uploads folder
UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Serve uploaded images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

origins = [
    "https://milkteafrontend.onrender.com",  # your frontend URL
    "http://localhost:5173",                 # for local development (Vite default)
]

# CORS Settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Import routers AFTER creating the app
from app.routes.product import router as products_router
from app.routes.category import router as category_router
from app.routes.order import router as orders_router
from app.routes import topping
from app.routes import stock as stock_router
from app.routes import user as user_router
from app.crud import product as product_crud
from app.crud import category as category_crud
from app.routes import countProduct as countProduct_router


# Register routers
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(category_router, prefix="/categories", tags=["Categories"])
app.include_router(orders_router, prefix="/orders", tags=["Orders"])
app.include_router(topping.router, prefix="/toppings", tags=["Toppings"])
app.include_router(stock_router.router, prefix="/stock", tags=["Stock"])
app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(countProduct_router.router, prefix="/count", tags=["Count"])





@app.get("/")
def root():
    return {"message": "MilkTea Backend Running"}



# ================================
#     ADMIN DASHBOARD STATS
# ================================
@app.get("/api/dashboard/stats")
async def get_dashboard_stats():
    orders_count = await db.orders.count_documents({})
    users_count = await db.users.count_documents({}) if "users" in await db.list_collection_names() else 0
    products_count = await db.products.count_documents({})

    # Top selling products pipeline
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

    # Total revenue
    pipeline_revenue = [{"$group": {"_id": None, "totalRevenue": {"$sum": "$totalPrice"}}}]
    revenue_cursor = db.orders.aggregate(pipeline_revenue)
    revenue_data = [r async for r in revenue_cursor]
    total_revenue = revenue_data[0]["totalRevenue"] if revenue_data else 0

    # Recent orders (latest 5)
    recent_orders_cursor = db.orders.find().sort("createdAt", -1).limit(5)
    recent_orders = []
    async for o in recent_orders_cursor:
        o["_id"] = str(o["_id"])
        user = await db.users.find_one({"_id": o["user"]}, {"name": 1})
        o["customerName"] = user["name"] if user else "Unknown"
        recent_orders.append({
            "orderId": o["_id"],
            "customerName": o["customerName"],
            "totalPrice": o["totalPrice"],
            "status": o["status"],
            "createdAt": o["createdAt"]
        })

    return {
        "orders": orders_count,
        "users": users_count,
        "products": products_count,
        "totalRevenue": total_revenue,
        "topProducts": top_products,
        "recentOrders": recent_orders
    }

# ================================
#     LOW STOCK PRODUCTS
# ================================
@app.get("/api/dashboard/low-stock")
async def get_low_stock():
    cursor = db.products.find({"stock": {"$lte": 5}}, {"name": 1, "stock": 1})
    low_stock = [{"name": p["name"], "quantity": p["stock"]} async for p in cursor]
    return low_stock


# ================================
#     GET CATEGORIES
# ================================
@app.get("/api/categories")
async def get_categories():
    cursor = db.categories.find({}, {"_id": 1, "name": 1})
    categories = [{"id": str(c["_id"]), "name": c["name"]} async for c in cursor]
    return categories


