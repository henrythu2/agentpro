import re
from typing import List, Optional, Tuple
from datetime import datetime
from .models import EmailVerification, Order, OrderCancellationRequest
from .api import OrderAPI

class OrderCancellationWorkflow:
    def __init__(self, api: OrderAPI):
        self.api = api
        self._email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        return bool(self._email_regex.match(email))

    def initiate_email_verification(self, email: str) -> Tuple[bool, str]:
        """Start email verification process"""
        if not self.validate_email(email):
            return False, "Invalid email format"
        
        if not self.api.send_verification_email(email):
            return False, "Failed to send verification email"
        
        return True, "Verification email sent successfully"

    def verify_user_code(self, email: str, code: str) -> Tuple[bool, str]:
        """Verify user's verification code"""
        if not self.api.verify_user(email, code):
            return False, "Invalid verification code"
        return True, "User verified successfully"

    def get_user_orders(self, email: str) -> List[Order]:
        """Get list of user's orders"""
        return self.api.list_orders(email)

    def prepare_order_cancellation(self, order: Order, email: str) -> OrderCancellationRequest: 
        """Prepare order cancellation request"""
        return OrderCancellationRequest(
            order=order,
            user_email=email,
            confirmation_timestamp=datetime.now()
        )

    def execute_cancellation(self, request: OrderCancellationRequest) -> Tuple[bool, str]:
        """Execute order cancellation"""
        if not request.confirmed:
            return False, "Cancellation not confirmed by user"
        
        if not self.api.cancel_order(request.order.order_id, request.user_email):
            return False, "Failed to cancel order"
        
        return True, "Order cancelled successfully"
