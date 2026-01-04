from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Order, OrderItem, Product

def create_order(db: Session, user_id: int, items: list):
    order = Order(user_id=user_id)
    db.add(order)
    db.flush()

    for item in items:
        product = db.query(Product).get(item["product_id"])
        if not product or product.stock < item["quantity"]:
            raise HTTPException(400, "Invalid stock or product")

        product.stock -= item["quantity"]

        db_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item["quantity"],
            price_at_purchase=product.price
        )
        db.add(db_item)

    db.commit()
    return order
