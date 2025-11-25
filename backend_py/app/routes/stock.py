from fastapi import APIRouter, HTTPException
from app.crud import stock as stock_crud

router = APIRouter()

@router.get("/", summary="Get all products with stock count")
async def get_stock():
    return await stock_crud.get_all_stock()

@router.get("/low", summary="Get products with low stock")
async def low_stock(threshold: int = 5):
    return await stock_crud.get_low_stock(threshold)

@router.put("/{product_id}", summary="Update stock for a product")
async def update_stock(product_id: str, new_stock: int):
    updated_count = await stock_crud.update_stock(product_id, new_stock)
    if updated_count == 0:
        raise HTTPException(status_code=404, detail="Product not found or stock unchanged")
    return {"message": "Stock updated successfully"}
