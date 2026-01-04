from fastapi import FastAPI
from app.routers import users, products, orders
from app.database import engine, Base

app = FastAPI(title="Ecommerce API")

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)

@app.get("/")
def root():
    return {"status": "FastAPI + SQL Server connected"}

