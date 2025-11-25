from fastapi import APIRouter
from app.crud import countProduct as count_crud

router = APIRouter()

@router.get("/categories/count")
async def category_product_count():
    """
    Returns categories with the total number of products in each
    """
    try:
        data = await count_crud.get_category_product_counts()
        return data
    except Exception as e:
        return {"error": str(e)}
