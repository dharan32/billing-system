from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse


from routes.product import router as product_router
from routes.billing import router as billing_router
from routes.purchase import router as purchase_router

app = FastAPI(
    title="Billing System",
    description="Billing System using FastAPI and PostgreSQL",
    version="1.0.0"
)


# Static files (CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates (HTML pages)
templates = Jinja2Templates(directory="templates")

# Register routes
app.include_router(product_router, prefix="/products", tags=["Products"])
app.include_router(billing_router, prefix="/billing", tags=["Billing"])
app.include_router(purchase_router, prefix="/purchases", tags=["Purchases"])


# @app.get("/")
# def root():
#     return {
#         "message": "Billing System API is running"
#     }

@app.get("/")
def redirect_to_billing():
    return RedirectResponse(url="/billing")
