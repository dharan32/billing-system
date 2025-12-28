from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime


# ----------------------------
# Product Schemas
# ----------------------------
class ProductBase(BaseModel):
    product_id: str
    name: str
    available_stock: int
    price_per_unit: float
    tax_percentage: float


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode = True


# ----------------------------
# Billing Schemas
# ----------------------------
class BillingItem(BaseModel):
    product_id: str
    quantity: int


class DenominationInput(BaseModel):
    value: int
    count: int


class BillingRequest(BaseModel):
    customer_email: EmailStr
    items: List[BillingItem]
    denominations: List[DenominationInput]
    paid_amount: float


class BillingItemResponse(BaseModel):
    product_id: str
    quantity: int
    unit_price: float
    tax_percentage: float
    subtotal: float


class DenominationResponse(BaseModel):
    value: int
    count: int


class BillingResponse(BaseModel):
    customer_email: EmailStr
    total_amount: float
    paid_amount: float
    balance_amount: float
    items: List[BillingItemResponse]
    balance_denominations: List[DenominationResponse]


# ----------------------------
# Purchase History Schemas
# ----------------------------
class PurchaseItemResponse(BaseModel):
    product_id: str
    quantity: int
    unit_price: float
    tax_percentage: float
    subtotal: float


class PurchaseResponse(BaseModel):
    id: int
    customer_email: EmailStr
    total_amount: float
    paid_amount: float
    balance_amount: float
    created_at: datetime
    items: List[PurchaseItemResponse]

    class Config:
        orm_mode = True
