from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class EmailVerification:
    email: str
    verification_code: Optional[str] = None
    verified: bool = False
    verification_timestamp: Optional[datetime] = None

@dataclass
class Order:
    order_id: str  # Internal use only
    order_date: datetime
    items: List[str]
    total_amount: float
    status: str

    def to_user_display(self) -> str:
        """Convert order to user-friendly display format without exposing order_id"""
        items_str = ", ".join(self.items)
        return (
            f"Order from {self.order_date.strftime('%Y-%m-%d %H:%M')}\n"
            f"Items: {items_str}\n"
            f"Total: ${self.total_amount:.2f}\n"
            f"Status: {self.status}"
        )

@dataclass
class OrderCancellationRequest:
    order: Order
    user_email: str
    confirmation_timestamp: Optional[datetime] = None
    confirmed: bool = False
