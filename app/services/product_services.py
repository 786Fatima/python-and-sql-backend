from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.product import Product

def create_product(db: Session, name: str, price: float, stock: int):
    if stock < 0:
        raise HTTPException(400, "Invalid stock")

    product = Product(name=name, price=price, stock=stock)
    db.add(product)
    db.commit()
    return product
