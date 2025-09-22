from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_or_404(query, message="Not found"):
    obj = query.first()
    if not obj:
        raise HTTPException(status_code=404, detail=message)
    return obj

@app.get("/")
def root():
    return {"message": "Shop API with SQLAlchemy is running"}

@app.post("/products", response_model=schemas.ProductOut)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(
        name=product.name,
        quantity=product.quantity,
        price=product.price,
        category_id=product.category_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products", response_model=list[schemas.ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@app.post("/orders", response_model=schemas.OrderOut)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = models.Order(client_id=order.client_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders/{order_id}", response_model=schemas.OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code = 404, detail="Order not found")


@app.post("/orders/add_item")
def add_item(req: schemas.AddItemRequest, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == req.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    product = db.query(models.Product).filter(models.Product.id == req.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.quantity < req.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")

    order_item = (
        db.query(models.OrderItem)
        .filter(models.OrderItem.order_id == req.order_id,
                models.OrderItem.product_id == req.product_id)
        .first()
    )

    if order_item:
        order_item.quantity += req.quantity
    else:
        order_item = models.OrderItem(
            order_id=req.order_id,
            product_id=req.product_id,
            quantity=req.quantity
        )
        db.add(order_item)

    product.quantity -= req.quantity

    if product.quantity == o:
        db.commit()
        raise HTTPException(status_code=400,detail="Product out of stock, cannot add more")

    db.commit()
    db.refresh(order_item)

    return {
        "message": "Item added to order",
        "order_id": order_item.order_id,
        "product_id": order_item.product_id,
        "quantity": order_item.quantity,
        "stock_left": product.quantity
    }

@app.post("/categories", response_model=schemas.CategoryOut)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    db_category = models.Category(name=category.name, parent_id=category.parent_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@app.get("/categories", response_model=list[schemas.CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()