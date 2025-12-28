from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import relationship
from datetime import datetime

from __init__ import Base


# ----------------------------
# Product Table
# ----------------------------
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    available_stock = Column(Integer, nullable=False)
    price_per_unit = Column(Float, nullable=False)
    tax_percentage = Column(Float, nullable=False)

    purchase_items = relationship("PurchaseItem", back_populates="product")


# ----------------------------
# Purchase Table
# ----------------------------
class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    customer_email = Column(String, nullable=False)
    total_amount = Column(Float, nullable=False)
    paid_amount = Column(Float, nullable=False)
    balance_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship("PurchaseItem", back_populates="purchase")


# ----------------------------
# Purchase Items Table
# ----------------------------
class PurchaseItem(Base):
    __tablename__ = "purchase_items"

    id = Column(Integer, primary_key=True, index=True)
    purchase_id = Column(Integer, ForeignKey("purchases.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    tax_percentage = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    purchase = relationship("Purchase", back_populates="items")
    product = relationship("Product", back_populates="purchase_items")


# ----------------------------
# Denomination Table
# ----------------------------
class Denomination(Base):
    __tablename__ = "denominations"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer, nullable=False)
    available_count = Column(Integer, nullable=False)
