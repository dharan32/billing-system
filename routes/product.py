from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from __init__ import get_db
from models import Product
from schemas import ProductCreate, ProductResponse

router = APIRouter()


@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product."""

    existing_product = db.query(Product).filter(
        Product.product_id == product.product_id
    ).first()

    if existing_product:
        raise HTTPException(
            status_code=400,
            detail="Product with this Product ID already exists"
        )

    new_product = Product(
        product_id=product.product_id,
        name=product.name,
        available_stock=product.available_stock,
        price_per_unit=product.price_per_unit,
        tax_percentage=product.tax_percentage
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@router.get("/", response_model=list[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    """Retrieve all products."""
    return db.query(Product).all()
