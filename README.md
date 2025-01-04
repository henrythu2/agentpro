# Agent Pro - Order Cancellation Workflow

This project implements an automated order cancellation workflow with email verification and user confirmation steps.

## Project Structure

```
src/
  ├── tasks/
  │   └── order_cancellation/  # Order cancellation task implementation
  ├── api/                     # API integration layer
  └── utils/                   # Utility functions and helpers
tests/                         # Test suite
```

## Setup

1. Install dependencies:
```bash
# Python dependencies
pip install -r requirements.txt

# Node.js dependencies (if needed)
npm install
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Development

To run tests:
```bash
python -m pytest
```

## API Integration Points

The system integrates with the following API endpoints:
- Email Verification: `@{Gen3.Send.User.Verification.Email-2p}`
- User Verification: `@{Gen3.Verify.User-2p}`
- Order Listing: `@{Gen3.List.Orders-2p}`
- Order Cancellation: `@{Gen3.Cancel.Order-2p}`
