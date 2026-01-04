from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.database import Base

class OrderItem(Base):
    __tablename__ = "OrderItems"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("Orders.id"))
    product_id = Column(Integer, ForeignKey("Products.id"))
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="items")
