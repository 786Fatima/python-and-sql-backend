from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from sqlalchemy import func
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.user import User
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderUpdateStatus


def create_order(db: Session, order: OrderCreate):
    # check user exists or not
    user = db.query(User).filter(User.id == order.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )

    db_order = Order(user_id=order.user_id)
    db.add(db_order)
    db.flush() 

    for item in order.items:
        # check produjct available or not
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {item.product_id} does not exist"
            )

        # check stock availability
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for product {product.name}"
            )

        product.stock -= item.quantity

        db_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=product.price
        )
        db.add(db_item)

    db.commit()
    db.refresh(db_order)
    return db_order


def get_all_orders(db: Session, status_filter=None, skip: int = 0, limit: int = 10):
    query = db.query(Order)
    
    if status_filter:
        query = query.filter(Order.status == status_filter)
    
    orders = (
        query
        .options(joinedload(Order.items))
        .order_by(Order.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    response = []

    for order in orders:
        items = []
        total_amount = 0

        for item in order.items:
            item_total = item.quantity * item.price
            total_amount += item_total

            items.append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": item.price,
                "item_total": item_total
            })

        response.append({
            "order_id": order.id,
            "user_id": order.user_id,
            "status": order.status.value,
            "created_at": order.created_at,
            "item_count": len(order.items),
            "total_amount": total_amount,
            "items": items
        })

    return response
    
    
def get_order_by_id(db: Session, order_id: int):

    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .options(joinedload(Order.items))
        .order_by(Order.created_at.desc())
        .first()
    )
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
        
    items = []
    total_amount = 0

    for item in order.items:
        item_total = item.quantity * item.price
        total_amount += item_total

        items.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price": item.price,
            "item_total": item_total
        })

    response = {
        "order_id": order.id,
        "user_id": order.user_id,
        "status": order.status.value,
        "created_at": order.created_at,
        "item_count": len(order.items),
        "total_amount": total_amount,
        "items": items
    }

    return response   


def update_order_status(db: Session, order_id: int, status_data: OrderUpdateStatus):
    order = db.query(Order).filter(Order.id == order_id).first()
    order.status = OrderStatus(status_data.status)
    db.commit()
    db.refresh(order)
    return order


def delete_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}


def get_orders_summary(db: Session):
    rows = (
        db.query(
            Order.id.label("order_id"),
            Order.user_id,
            Order.status,
            func.count(OrderItem.id).label("item_count"),
            func.coalesce(
                func.sum(OrderItem.quantity * OrderItem.price),
                0
            ).label("total_amount"),
            Order.created_at
        )
        .outerjoin(OrderItem, OrderItem.order_id == Order.id)
        .group_by(Order.id, Order.user_id, Order.status, Order.created_at)
        .order_by(Order.created_at.desc())
        .all()
    )

    return [
        {
            "order_id": row.order_id,
            "user_id": row.user_id,
            "status": row.status.value if hasattr(row.status, "value") else row.status,
            "item_count": row.item_count,
            "total_amount": float(row.total_amount),
            "created_at": row.created_at,
        }
        for row in rows
    ]
