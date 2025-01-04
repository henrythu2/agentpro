from typing import List, Optional
from datetime import datetime
import requests
from .models import Order, EmailVerification

class OrderAPI:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def send_verification_email(self, email: str) -> bool:
        """Send verification email using Gen3.Send.User.Verification.Email-2p"""
        response = requests.post(
            f"{self.base_url}/verification/email",
            json={"email": email},
            headers=self.headers
        )
        return response.status_code == 200

    def verify_user(self, email: str, code: str) -> bool:
        """Verify user using Gen3.Verify.User-2p"""
        response = requests.post(
            f"{self.base_url}/verify/user",
            json={"email": email, "code": code},
            headers=self.headers
        )
        return response.status_code == 200

    def list_orders(self, email: str) -> List[Order]:
        """List orders using Gen3.List.Orders-2p"""
        response = requests.get(
            f"{self.base_url}/orders",
            params={"email": email},
            headers=self.headers
        )
        if response.status_code != 200:
            return []
        
        orders_data = response.json()
        return [
            Order(
                order_id=order["id"],
                order_date=datetime.fromisoformat(order["date"]),
                items=order["items"],
                total_amount=order["total"],
                status=order["status"]
            )
            for order in orders_data
        ]

    def cancel_order(self, order_id: str, email: str) -> bool:
        """Cancel order using Gen3.Cancel.Order-2p"""
        response = requests.post(
            f"{self.base_url}/orders/{order_id}/cancel",
            json={"email": email},
            headers=self.headers
        )
        return response.status_code == 200
