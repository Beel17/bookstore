from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional
from datetime import datetime
from app.models import UserRole, OrderStatus, PaymentStatus

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str
    admin_code: Optional[str] = None
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Book Schemas
class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    price: float
    stock_quantity: int
    isbn: Optional[str] = None
    image_url: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    isbn: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None

class Book(BookBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Order Schemas
class OrderItemBase(BaseModel):
    book_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    price: float
    book: Book
    
    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    order_items: List[OrderItemCreate]

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    user_id: int
    total_amount: float
    status: OrderStatus
    payment_status: PaymentStatus
    payment_reference: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    order_items: List[OrderItem]
    
    class Config:
        from_attributes = True

# Payment Schemas
class PaymentInitiate(BaseModel):
    order_id: int
    amount: float
    email: EmailStr
    callback_url: Optional[str] = None

class PaymentVerify(BaseModel):
    reference: str

class Payment(BaseModel):
    id: int
    order_id: int
    reference: str
    amount: float
    status: PaymentStatus
    paystack_reference: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Response Schemas
class MessageResponse(BaseModel):
    message: str

class PaymentResponse(BaseModel):
    authorization_url: str
    access_code: str
    reference: str
