from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Order, OrderItem, OrderStatus, PaymentStatus
from app.schemas import OrderCreate, Order as OrderSchema, PaymentInitiate, PaymentResponse
from app.books.crud import check_book_stock, update_book_stock, get_book
from app.orders.payments import initiate_paystack_payment, verify_paystack_payment
from app.auth.utils import get_current_active_user
import uuid

router = APIRouter(prefix="/orders", tags=["orders"])

def create_order(db: Session, order: OrderCreate, user_id: int) -> Order:
    """Create a new order"""
    total_amount = 0.0
    order_items = []
    
    # Validate and calculate total
    for item in order.order_items:
        book = get_book(db, item.book_id)
        if not book or not book.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {item.book_id} not found"
            )
        
        if not check_book_stock(db, item.book_id, item.quantity):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for book: {book.title}"
            )
        
        item_total = book.price * item.quantity
        total_amount += item_total
        
        order_items.append({
            "book_id": item.book_id,
            "quantity": item.quantity,
            "price": book.price
        })
    
    # Create order
    db_order = Order(
        user_id=user_id,
        total_amount=total_amount,
        payment_reference=f"ORD_{uuid.uuid4().hex[:10].upper()}"
    )
    
    db.add(db_order)
    db.flush()  # Get the order ID
    
    # Create order items and update stock
    for item_data in order_items:
        order_item = OrderItem(
            order_id=db_order.id,
            **item_data
        )
        db.add(order_item)
        
        # Update book stock
        update_book_stock(db, item_data["book_id"], -item_data["quantity"])
    
    db.commit()
    db.refresh(db_order)
    
    return db_order

@router.post("/", response_model=OrderSchema)
def create_new_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new order"""
    if not order.order_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order must contain at least one item"
        )
    
    return create_order(db=db, order=order, user_id=current_user.id)

@router.get("/", response_model=List[OrderSchema])
def read_user_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get user's orders"""
    orders = db.query(Order).filter(
        Order.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return orders

@router.get("/{order_id}", response_model=OrderSchema)
def read_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific order"""
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return order

@router.post("/payment/initiate", response_model=PaymentResponse)
def initiate_payment(
    payment_data: PaymentInitiate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Initiate payment for an order"""
    # Verify order belongs to user
    order = db.query(Order).filter(
        Order.id == payment_data.order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    if order.payment_status == PaymentStatus.SUCCESS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order already paid"
        )
    
    if payment_data.amount != order.total_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment amount doesn't match order total"
        )
    
    try:
        return initiate_paystack_payment(db, payment_data, order)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Payment initiation failed: {str(e)}"
        )

@router.post("/payment/verify")
def verify_payment(
    reference: str,
    db: Session = Depends(get_db)
):
    """Verify payment (callback from Paystack)"""
    try:
        result = verify_paystack_payment(db, reference)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Payment verification failed: {str(e)}"
        )
