from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import SessionLocal
from app.schemas.order import OrderCreate, OrderUpdateStatus, OrderStatusEnum
from app.services.order_services import create_order, get_all_orders, get_order_by_id, update_order_status, delete_order, get_orders_summary

router = APIRouter(prefix="/orders", tags=["Orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create")
def create_new_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    return create_order(db, order)


@router.get("/get-all-orders")
def list_orders(
    status: Optional[OrderStatusEnum] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return get_all_orders(db, status, skip, limit)


@router.get("/get-order-by-id/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    return get_order_by_id(db, order_id)


@router.put("/update-order-status/{order_id}")
def update_status(
    order_id: int,
    status: OrderUpdateStatus,
    db: Session = Depends(get_db)
):
    return update_order_status(db, order_id, status)


@router.delete("/delete-order/{order_id}")
def delete_existing_order(order_id: int, db: Session = Depends(get_db)):
    return delete_order(db, order_id)

@router.get("/final-summary")
def orders_summary(db: Session = Depends(get_db)):
    return get_orders_summary(db)