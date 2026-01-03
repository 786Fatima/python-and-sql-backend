from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.order_service import create_order

router = APIRouter(prefix="/orders", tags=["Orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @router.post("/create")
# def register_order(name: str, price: float, stock: int, db: Session = Depends(get_db)):
#     order = create_order(db, name, email, mobile_number, password)
#     return {"message": "Order registered successfully", "order": order}

@router.get("/")
def list_orders(
    status: OrderStatus | None = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(Order)
    if status:
        query = query.filter(Order.status == status)

    return query.offset((page - 1) * limit).limit(limit).all()
# @router.get("/get-order-by-email")
# def get_order_by_email(email: str, db: Session = Depends(get_db)):
#     order = get_order_by_email(db, email)
#     return {"order": order}   

# @router.get("/get-all-orders")
# def get_all_orders(db: Session = Depends(get_db)):
#     orders = fetch_all_orders(db)
#     return {"orders": orders}