from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Product


def calculate_bill(billing_request: dict, db: Session):
    """Calculate bill amount, tax, and balance based on purchase details."""

    items_data = []
    total_amount = 0.0

    for item in billing_request["items"]:
        product = db.query(Product).filter(
            Product.product_id == item["product_id"]
        ).first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product ID {item['product_id']} not found"
            )

        if item["quantity"] > product.available_stock:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for Product ID {item['product_id']}"
            )

        price = product.price_per_unit * item["quantity"]
        tax = price * (product.tax_percentage / 100)
        subtotal = price + tax

        items_data.append({
            "product_id": product.product_id,
            "quantity": item["quantity"],
            "unit_price": product.price_per_unit,
            "tax_percentage": product.tax_percentage,
            "subtotal": subtotal
        })

        total_amount += subtotal

    paid_amount = billing_request["paid_amount"]

    if paid_amount < total_amount:
        raise HTTPException(
            status_code=400,
            detail="Paid amount is less than total bill amount"
        )

    balance_amount = paid_amount - total_amount

    return {
        "customer_email": billing_request["customer_email"],
        "items": items_data,
        "total_amount": total_amount,
        "paid_amount": paid_amount,
        "balance_amount": balance_amount
    }
