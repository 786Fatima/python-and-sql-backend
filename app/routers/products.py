from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.product_service import create_product

router = APIRouter(prefix="/products", tags=["Products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create")
def register_product(name: str, price: float, stock: int, db: Session = Depends(get_db)):
    product = create_product(db, name, email, mobile_number, password)
    return {"message": "Product registered successfully", "product": product}

# @router.get("/get-product-by-email")
# def get_product_by_email(email: str, db: Session = Depends(get_db)):
#     product = get_product_by_email(db, email)
#     return {"product": product}   

# @router.get("/get-all-products")
# def get_all_products(db: Session = Depends(get_db)):
#     products = fetch_all_products(db)
#     return {"products": products}