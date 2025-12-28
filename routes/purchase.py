from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from __init__ import get_db
from models import Purchase, Product
from schemas import PurchaseResponse, PurchaseItemResponse

router = APIRouter()


@router.get("/", response_model=list[PurchaseResponse])
def get_purchases_by_customer(
    email: str = Query(..., description="Customer email"),
    db: Session = Depends(get_db)
):
    """Retrieve purchases for a given customer email."""

    purchases = db.query(Purchase).filter(
        Purchase.customer_email == email
    ).all()

    if not purchases:
        raise HTTPException(
            status_code=404,
            detail="No purchases found for this customer"
        )

    response = []

    for purchase in purchases:
        items = []

        for item in purchase.items:
            product = db.query(Product).filter(
                Product.id == item.product_id
            ).first()

            items.append(
                PurchaseItemResponse(
                    product_id=product.product_id if product else "",
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    tax_percentage=item.tax_percentage,
                    subtotal=item.subtotal
                )
            )

        response.append(
            PurchaseResponse(
                id=purchase.id,
                customer_email=purchase.customer_email,
                total_amount=purchase.total_amount,
                paid_amount=purchase.paid_amount,
                balance_amount=purchase.balance_amount,
                created_at=purchase.created_at,
                items=items
            )
        )

    return response
