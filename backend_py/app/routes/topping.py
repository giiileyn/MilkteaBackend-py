from fastapi import APIRouter, HTTPException
from app.crud import topping as topping_crud

router = APIRouter()

# ================================
#       GET ALL TOPPINGS
# ================================
@router.get("/")
async def get_toppings():
    return await topping_crud.get_all_toppings()

# ================================
#       GET SINGLE TOPPING
# ================================
@router.get("/{topping_id}")
async def get_topping(topping_id: str):
    topping = await topping_crud.get_topping(topping_id)
    if not topping:
        raise HTTPException(status_code=404, detail="Topping not found")
    return topping

# ================================
#       CREATE TOPPING
# ================================
@router.post("/")
async def create_topping(name: str, price: float = 0, stock: int = 0, status: str = "available"):
    data = {
        "name": name,
        "price": price,
        "stock": stock,
        "status": status
    }
    new_topping = await topping_crud.create_topping(data)
    return new_topping

# ================================
#       UPDATE TOPPING
# ================================
@router.put("/{topping_id}")
async def update_topping(topping_id: str, name: str = None, price: float = None, stock: int = None, status: str = None):
    data = {}
    if name is not None: data["name"] = name
    if price is not None: data["price"] = price
    if stock is not None: data["stock"] = stock
    if status is not None: data["status"] = status

    updated_topping = await topping_crud.update_topping(topping_id, data)
    if not updated_topping:
        raise HTTPException(status_code=404, detail="Topping not found")
    return updated_topping

# ================================
#       DELETE TOPPING
# ================================
@router.delete("/{topping_id}")
async def delete_topping(topping_id: str):
    success = await topping_crud.delete_topping(topping_id)
    if not success:
        raise HTTPException(status_code=404, detail="Topping not found")
    return {"message": "Topping deleted successfully"}
