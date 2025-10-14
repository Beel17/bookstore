import uuid
import requests
from typing import Optional
from sqlalchemy.orm import Session
from app.models import Order, Payment, PaymentStatus
from app.schemas import PaymentInitiate, PaymentResponse
from app.config import settings

def generate_payment_reference() -> str:
    """Generate a unique payment reference"""
    return f"PAY_{uuid.uuid4().hex[:10].upper()}"

def initiate_paystack_payment(
    db: Session, 
    payment_data: PaymentInitiate,
    order: Order
) -> PaymentResponse:
    """Initiate payment with Paystack"""
    if not settings.PAYSTACK_SECRET_KEY:
        raise Exception("Paystack secret key not configured")
    
    # Generate payment reference
    reference = generate_payment_reference()
    
    # Prepare Paystack payload
    payload = {
        "email": payment_data.email,
        "amount": int(payment_data.amount * 100),  # Convert to kobo
        "reference": reference,
        "callback_url": payment_data.callback_url or "http://localhost:8000/orders/payment/callback",
        "metadata": {
            "order_id": order.id,
            "user_id": order.user_id
        }
    }
    
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    
    # Make request to Paystack
    response = requests.post(
        "https://api.paystack.co/transaction/initialize",
        json=payload,
        headers=headers
    )
    
    if response.status_code != 200:
        raise Exception(f"Paystack API error: {response.text}")
    
    paystack_response = response.json()
    
    if not paystack_response.get("status"):
        raise Exception(f"Paystack error: {paystack_response.get('message')}")
    
    data = paystack_response["data"]
    
    # Store payment record
    payment = Payment(
        order_id=order.id,
        reference=reference,
        amount=payment_data.amount,
        status=PaymentStatus.PENDING,
        paystack_reference=data.get("reference"),
        gateway_response=response.text
    )
    
    db.add(payment)
    db.commit()
    
    return PaymentResponse(
        authorization_url=data["authorization_url"],
        access_code=data["access_code"],
        reference=reference
    )

def verify_paystack_payment(db: Session, reference: str) -> dict:
    """Verify payment with Paystack"""
    if not settings.PAYSTACK_SECRET_KEY:
        raise Exception("Paystack secret key not configured")
    
    # Get payment record
    payment = db.query(Payment).filter(Payment.reference == reference).first()
    if not payment:
        raise Exception("Payment record not found")
    
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    
    # Verify with Paystack
    response = requests.get(
        f"https://api.paystack.co/transaction/verify/{payment.paystack_reference}",
        headers=headers
    )
    
    if response.status_code != 200:
        raise Exception(f"Paystack API error: {response.text}")
    
    paystack_response = response.json()
    
    if not paystack_response.get("status"):
        raise Exception(f"Paystack error: {paystack_response.get('message')}")
    
    data = paystack_response["data"]
    
    # Update payment status
    if data["status"] == "success":
        payment.status = PaymentStatus.SUCCESS
        payment.gateway_response = response.text
        
        # Update order status
        order = db.query(Order).filter(Order.id == payment.order_id).first()
        if order:
            order.payment_status = PaymentStatus.SUCCESS
            order.payment_reference = reference
    else:
        payment.status = PaymentStatus.FAILED
        payment.gateway_response = response.text
    
    db.commit()
    
    return {
        "status": payment.status,
        "amount": payment.amount,
        "reference": payment.reference,
        "gateway_response": data
    }
