# app/routes/order.py
from fastapi import APIRouter, HTTPException, Body 
from app.crud import order as order_crud

router = APIRouter()

@router.get("/")
async def fetch_orders():
    try:
        return await order_crud.get_all_orders()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{order_id}")
async def fetch_order(order_id: str):
    try:
        order = await order_crud.get_order_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{order_id}/status")
async def change_order_status(order_id: str, status: str = Body(..., embed=True)):
    """
    Update the status of an order.
    Expects JSON: { "status": "Completed" }
    """
    try:
        updated_order = await order_crud.update_order_status(order_id, status)
        if not updated_order:
            raise HTTPException(status_code=404, detail="Order not found")
        return {"success": True, "message": "Order status updated", "order": updated_order}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))