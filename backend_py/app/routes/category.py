from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.crud import category as category_crud
from main import db  # import the db instance from main.py

router = APIRouter(prefix="/api/categories", tags=["categories"])

@router.get("/", response_model=List[dict])
async def list_categories():
    return await category_crud.get_categories(db)

@router.post("/")
async def create_category(name: str, description: str = ""):
    category_data = {"name": name, "description": description}
    category = await category_crud.create_category(db, category_data)
    return {"message": "Category created successfully", "category": category}

@router.get("/{category_id}")
async def get_category(category_id: str):
    category = await category_crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}")
async def update_category(category_id: str, name: str = None, description: str = None):
    update_data = {}
    if name is not None:
        update_data["name"] = name
    if description is not None:
        update_data["description"] = description
    updated = await category_crud.update_category(db, category_id, update_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category updated successfully", "category": updated}

@router.delete("/{category_id}")
async def delete_category(category_id: str):
    deleted_count = await category_crud.delete_category(db, category_id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}
