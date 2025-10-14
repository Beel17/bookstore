from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine
from app import models
from app.auth.routes import router as auth_router
from app.books.routes import router as books_router
from app.orders.routes import router as orders_router

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Bookstore API",
    description="A complete bookstore management system with authentication and payments",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(auth_router)
app.include_router(books_router)
app.include_router(orders_router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Bookstore API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "environment": settings.ENVIRONMENT}

# Template routes for frontend
@app.get("/index")
async def index_page(request: Request):
    """Home page showing all books"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
async def login_page(request: Request):
    """Login page"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/admin")
async def admin_page(request: Request):
    """Admin panel for book management"""
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get("/checkout/{order_id}")
async def checkout_page(request: Request, order_id: int):
    """Checkout page for order payment"""
    return templates.TemplateResponse("checkout.html", {
        "request": request, 
        "order_id": order_id
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=settings.ENVIRONMENT == "development"
    )
