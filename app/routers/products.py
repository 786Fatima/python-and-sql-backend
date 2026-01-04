from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app.schemas.product import ProductCreate, ProductUpdate

from app.services.product_services import create_product, get_all_products, get_product_by_id, update_product, delete_product


router = APIRouter(prefix="/products", tags=["Products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create")
def create_new_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    return create_product(db, product)


@router.get("/get-all-products")
def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return get_all_products(db, skip=skip, limit=limit)


@router.get("/get-product-by-id/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    return get_product_by_id(db, product_id)


@router.put("/update-product/{product_id}")
def update_existing_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db)
):
    return update_product(db, product_id, product)


@router.delete("/update-product/{product_id}")
def delete_existing_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    return delete_product(db, product_id)
