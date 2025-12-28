from fastapi import APIRouter, Depends, Request, Form, HTTPException, BackgroundTasks
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List

from __init__ import get_db
from models import Product, Purchase, PurchaseItem
from services.billing_service import calculate_bill
from services.denomination_service import calculate_balance_denominations
from services.email_service import send_invoice_email

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("")
def show_billing_page(request: Request):
    """Render billing form page."""
    return templates.TemplateResponse(
        "billing_form.html",
        {"request": request}
    )


@router.post("/generate")
def generate_bill(
    request: Request,
    background_tasks: BackgroundTasks,

    customer_email: str = Form(...),

    product_id: List[str] = Form(...),
    quantity: List[int] = Form(...),

    denom_100: int = Form(0),
    denom_50: int = Form(0),
    denom_20: int = Form(0),
    denom_10: int = Form(0),

    paid_amount: float = Form(...),

    db: Session = Depends(get_db)
):
    """Generate bill, save purchase, calculate balance, and send invoice email."""

    if len(product_id) != len(quantity):
        raise HTTPException(
            status_code=400,
            detail="Product IDs and quantities count mismatch"
        )


    items = []
    for i in range(len(product_id)):
        items.append({
            "product_id": product_id[i],
            "quantity": quantity[i]
        })

    billing_request = {
        "customer_email": customer_email,
        "items": items,
        "denominations": [
            {"value": 100, "count": denom_100},
            {"value": 50, "count": denom_50},
            {"value": 20, "count": denom_20},
            {"value": 10, "count": denom_10},
        ],
        "paid_amount": paid_amount
    }

    bill_data = calculate_bill(billing_request, db)

    purchase = Purchase(
        customer_email=bill_data["customer_email"],
        total_amount=bill_data["total_amount"],
        paid_amount=bill_data["paid_amount"],
        balance_amount=bill_data["balance_amount"]
    )
    db.add(purchase)
    db.commit()
    db.refresh(purchase)

    for item in bill_data["items"]:
        product = db.query(Product).filter(
            Product.product_id == item["product_id"]
        ).first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product ID {item['product_id']} not found"
            )

        purchase_item = PurchaseItem(
            purchase_id=purchase.id,
            product_id=product.id,
            quantity=item["quantity"],
            unit_price=item["unit_price"],
            tax_percentage=item["tax_percentage"],
            subtotal=item["subtotal"]
        )
        db.add(purchase_item)

    db.commit()

    balance_denominations = calculate_balance_denominations(
        bill_data["balance_amount"],
        billing_request["denominations"]
    )

    send_invoice_email(
        background_tasks=background_tasks,
        to_email=bill_data["customer_email"],
        subject="Your Invoice",
        bill=bill_data
    )

    return templates.TemplateResponse(
        "bill_result.html",
        {
            "request": request,
            "bill": bill_data,
            "balance_denominations": balance_denominations
        }
    )
