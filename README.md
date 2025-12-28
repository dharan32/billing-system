# Billing System (FastAPI + PostgreSQL)

A FastAPI-based billing system developed as part of a technical assignment.  
The application supports product management, billing with tax calculation, cash denomination validation, invoice generation, and asynchronous invoice email delivery.

---

## Features

- Product management with configurable tax
- Billing generation with product-wise tax calculation
- Cash denomination validation for exact balance return
- Invoice generation using HTML templates
- Asynchronous invoice email delivery using SMTP
- Purchase history retrieval by customer email

---

## Tech Stack

- Python 3.11.1
- FastAPI
- PostgreSQL
- SQLAlchemy
- Jinja2 Templates
- SMTP (Gmail)
- python-dotenv

---

## High-Level Flow

1. Products are created using Product APIs
2. User opens the billing page (`/billing`)
3. User enters:
   - Customer email
   - Product ID and quantity
   - Available cash denominations
   - Paid amount
4. System:
   - Calculates tax and total amount
   - Validates product stock
   - Validates exact balance using denominations
   - Saves purchase and purchase items
   - Sends invoice email asynchronously
5. Invoice is displayed on UI and sent to the customer email

---

## API Endpoints

### Product APIs
- POST /products – Create a product
- GET /products – List all products

### Billing
- GET /billing – Billing form UI
- POST /billing/generate – Generate bill and invoice

### Purchase History
- GET /purchases?email=customer@example.com – Retrieve purchase history

---

## API Documentation (Swagger)

FastAPI automatically generates interactive API documentation.

- Swagger UI:  
  http://127.0.0.1:8000/docs

- ReDoc UI:  
  http://127.0.0.1:8000/redoc

Swagger can be used for:
- Creating and testing Product APIs
- Viewing request and response schemas
- Testing Purchase History APIs
- Validating API behavior without external tools

---

## Tax, Denomination, and Email Invoice Logic

Tax is configured at the product level and stored as `tax_percentage` in the database.  
During billing, tax is calculated per product using:

```
tax = price_per_unit × quantity × (tax_percentage / 100)
```

The subtotal for each product is calculated as:

```
subtotal = base_price + tax
```

The final bill amount is the sum of all product subtotals.

After calculating the total bill amount, the system calculates the balance amount using:

```
balance_amount = paid_amount − total_amount
```

The balance must be returned using available cash denominations.  
Supported denominations are:
- 100
- 50
- 20
- 10

The system uses a greedy algorithm to determine the denomination breakup.  
If the exact balance cannot be returned using the provided denominations, billing fails with a validation error.

Decimal or unsupported balances (₹5 / paise) are not allowed.  
The paid amount must allow exact balance using available denominations.  
This logic mimics real-world cash billing behavior.

Once the bill is successfully generated, an invoice is sent to the customer email.  
The invoice is sent as an HTML formatted email using Gmail SMTP with an App Password.  
Email sending runs asynchronously using FastAPI BackgroundTasks, ensuring the billing flow is not blocked even if email delivery fails.

---

## Project Setup

### 1. Clone Repository
```
git clone <repository-url>
cd billing_system
```

### 2. Create Virtual Environment (Python 3.11.1)
```
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate    # Windows
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/billing_db

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

Note: Use Gmail App Password, not your regular Gmail password.

---

### 5. Database Setup

- Create a PostgreSQL database named `billing_db`
- Tables are created automatically using SQLAlchemy models

---

### 6. Run the Application
```
uvicorn main:app --reload
```

Application will be available at:
http://127.0.0.1:8000

---

## Application Pages

- Billing Page  
  /billing – Create a new bill

- Bill Result Page  
  Displayed after bill generation

- Purchase History  
  /purchases?email=customer@example.com

---

