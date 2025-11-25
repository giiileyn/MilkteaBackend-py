from fastapi import APIRouter, HTTPException
from app.crud import product as product_crud


router = APIRouter(prefix="/api/products", tags=["products"])

# GET ALL PRODUCTS
@router.get("/")
async def fetch_products():
    return await product_crud.get_products()

# GET SINGLE PRODUCT
@router.get("/{product_id}")
async def fetch_product(product_id: str):
    product = await product_crud.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# CREATE PRODUCT
@router.post("/")
async def create_product(data: dict):
    return await product_crud.create_product(data)

# UPDATE PRODUCT
@router.put("/{product_id}")
async def update_product(product_id: str, data: dict):
    updated_product = await product_crud.update_product(product_id, data)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

# DELETE PRODUCT
@router.delete("/{product_id}")
async def delete_product(product_id: str):
    success = await product_crud.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
