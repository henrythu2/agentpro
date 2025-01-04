import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from src.tasks.order_cancellation.models import EmailVerification, Order, OrderCancellationRequest
from src.tasks.order_cancellation.api import OrderAPI
from src.tasks.order_cancellation.workflow_manager import OrderCancellationWorkflow

@pytest.fixture
def mock_api():
    return Mock(spec=OrderAPI)

@pytest.fixture
def workflow(mock_api):
    return OrderCancellationWorkflow(mock_api)

@pytest.fixture
def sample_order():
    return Order(
        order_id="123",
        order_date=datetime.now(),
        items=["Item 1", "Item 2"],
        total_amount=99.99,
        status="Active"
    )

class TestEmailValidation:
    @pytest.mark.parametrize("email,expected", [
        ("valid@example.com", True),
        ("invalid.email", False),
        ("", False),
        ("test@test@test.com", False),
        ("test@.com", False),
    ])
    def test_email_validation(self, workflow, email, expected):
        assert workflow.validate_email(email) == expected

class TestVerificationFlow:
    def test_successful_verification_flow(self, workflow, mock_api):
        mock_api.send_verification_email.return_value = True
        mock_api.verify_user.return_value = True
        
        # Test email verification initiation
        success, message = workflow.initiate_email_verification("test@example.com")
        assert success
        assert "successfully" in message
        mock_api.send_verification_email.assert_called_once()
        
        # Test verification code
        success, message = workflow.verify_user_code("test@example.com", "123456")
        assert success
        assert "verified successfully" in message
        mock_api.verify_user.assert_called_once()

    def test_failed_verification_flow(self, workflow, mock_api):
        mock_api.send_verification_email.return_value = False
        
        success, message = workflow.initiate_email_verification("test@example.com")
        assert not success
        assert "Failed" in message

class TestOrderManagement:
    def test_order_display_format(self, sample_order):
        display = sample_order.to_user_display()
        assert "Order from" in display
        assert str(sample_order.total_amount) in display
        assert "order_id" not in display  # Ensure order_id is not exposed
        
    def test_list_orders(self, workflow, mock_api):
        mock_orders = [
            Order(
                order_id="123",
                order_date=datetime.now(),
                items=["Item 1"],
                total_amount=99.99,
                status="Active"
            )
        ]
        mock_api.list_orders.return_value = mock_orders
        
        orders = workflow.get_user_orders("test@example.com")
        assert len(orders) == 1
        assert isinstance(orders[0], Order)
        mock_api.list_orders.assert_called_once()

    def test_order_cancellation(self, workflow, mock_api, sample_order):
        mock_api.cancel_order.return_value = True
        
        # Create cancellation request
        request = workflow.prepare_order_cancellation(sample_order, "test@example.com")
        assert isinstance(request, OrderCancellationRequest)
        assert request.order == sample_order
        
        # Test unconfirmed cancellation
        success, message = workflow.execute_cancellation(request)
        assert not success
        assert "not confirmed" in message
        
        # Test confirmed cancellation
        request.confirmed = True
        success, message = workflow.execute_cancellation(request)
        assert success
        assert "cancelled successfully" in message
        mock_api.cancel_order.assert_called_once_with(sample_order.order_id, "test@example.com")

class TestErrorHandling:
    def test_invalid_email_handling(self, workflow, mock_api):
        success, message = workflow.initiate_email_verification("invalid.email")
        assert not success
        assert "Invalid email format" in message
        mock_api.send_verification_email.assert_not_called()

    def test_failed_verification_code(self, workflow, mock_api):
        mock_api.verify_user.return_value = False
        
        success, message = workflow.verify_user_code("test@example.com", "wrong_code")
        assert not success
        assert "Invalid verification code" in message

    def test_failed_order_cancellation(self, workflow, mock_api, sample_order):
        mock_api.cancel_order.return_value = False
        
        request = OrderCancellationRequest(
            order=sample_order,
            user_email="test@example.com",
            confirmed=True
        )
        
        success, message = workflow.execute_cancellation(request)
        assert not success
        assert "Failed to cancel order" in message
