import requests, hmac, hashlib
from decimal import Decimal
from typing import Optional, Any
from flask import request

from . import PaymentProcessor
from ..exceptions import SignatureError
from ..types import PaymentProcessorResponse, PaymentStatus, PaymentWebhookData, TransferWebhookData
from ....enums import TransferStatus

class PaystackProcessor(PaymentProcessor):
    """
    Handles payments via Paystack API.
    """
    reference_prefix = "pst_"
    supported_currencies = {"NGN", "USD", "GHS"}
    
    def initialize_payment(self, amount: float | Decimal, currency: str, customer_data: dict, redirect_url: Optional[str] = None) -> PaymentProcessorResponse:
        """
        Initialize payment with Paystack.
        
        Args:
            amount: Payment amount
            currency: Payment currency code
            customer_data: Customer information (email, name)
            
        Returns:
            PaymentProcessorResponse: Standardized payment response
        """
        url = "https://api.paystack.co/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "email": customer_data["email"],
            "amount": int(float(amount) * 100),  # Paystack expects amount in kobo
            "currency": currency,
            "reference": self.reference,
            "callback_url": redirect_url
        }

        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()
        
        payment_response = PaymentProcessorResponse(
            status="success" if response_data["status"] else "error",
            message=response_data.get("message", ""),
            payment_id=response_data.get("data", {}).get("reference"),
            authorization_url=response_data.get("data", {}).get("authorization_url"),
            reference = self.reference,
        )
        return payment_response
    
    def verify_payment(self, payment_reference: str) -> dict[str, Any]:
        """
        Verify payment status with Paystack.
        
        Args:
            payment_reference: Payment reference to verify
            
        Returns:
            dict: Verification response with standardized status
        """
        url = f"https://api.paystack.co/transaction/verify/{payment_reference}"
        
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        response_data = response.json()
        data = response_data.get("data", {})
        
        status_mapping = {
            "success": PaymentStatus.COMPLETED,
            "failed": PaymentStatus.FAILED,
            "pending": PaymentStatus.PENDING,
            "abandoned": PaymentStatus.FAILED
        }
        
        return {
            "status": status_mapping.get(data.get("status", ""), PaymentStatus.PENDING),
            "amount": Decimal(str(data.get("amount", 0))) / 100,  # Convert from kobo
            "currency": data.get("currency", ""),
            "provider_reference": str(data.get("id")),
            "metadata": data,
            "raw_data":response_data
        }
    
    def verify_webhook_signature(self, payload: dict = None, signature: str | None = None) -> bool:
        """
        Verify Paystack webhook signature.
        
        Args:
            payload: Webhook request body (unused, kept for interface consistency)
            signature: Signature from webhook header (unused, extracted from request)
            
        Returns:
            bool: True if signature is valid
            
        Raises:
            SignatureError: If signature is missing or invalid
        """
        signature = request.headers.get('x-paystack-signature') # Get signature from the request headers
        if not signature:
            raise SignatureError("Missing webhook signature")
        
        secret_key = self.secret_key # Get secret key from settings
        
        # Create hash using the secret key and the data
        hash = hmac.new(
            secret_key.encode(),
            msg=request.data,
            digestmod=hashlib.sha512
        )
        
        
        # Verify the signature
        if not hmac.compare_digest(hash.hexdigest(), signature):
            raise SignatureError(f'Invalid Paystack signature')
        
        
        return True
    
    def parse_webhook_event(self, payload: dict) -> PaymentWebhookData | TransferWebhookData:
        """
        Parse Paystack webhook payload into standard format based on event type.
        
        Args:
            payload: Raw webhook data
            
        Returns:
            PaymentWebhookData or TransferWebhookData based on event type
        """
        event = payload.get("event", "")
        
        if event.startswith("charge."):
            return self._parse_payment_webhook(payload)
        elif event.startswith("transfer."):
            return self._parse_transfer_webhook(payload)
        else:
            raise ValueError(f"Unsupported webhook event: {event}")

    
    def _parse_payment_webhook(self, payload: dict) -> PaymentWebhookData:
        """Parse payment-specific webhook data."""
        event = payload.get("event")
        data = payload.get("data", {})
        transaction_status = data.get("status", "").lower()
        
        payment_status = self._determine_payment_status(event, transaction_status)
        
        parsed_data = PaymentWebhookData(
            event_type="payment",
            status=payment_status,
            reference=data.get("reference", ""),
            provider_reference=str(data.get("id", "")),
            amount=Decimal(str(data.get("amount", 0))) / 100,
            currency=data.get("currency", ""),
            raw_data=payload,
            gateway_response=data.get("gateway_response"),
            customer_code=data.get("customer", {}).get("customer_code")
        )
        
        return parsed_data
    
    def _parse_transfer_webhook(self, payload: dict) -> TransferWebhookData:
        """Parse transfer-specific webhook data."""
        event = payload.get("event")
        data = payload.get("data", {})
        
        transfer_status = self._determine_transfer_status(event, data.get("status"))
        
        parsed_data = TransferWebhookData(
            event_type="transfer",
            status=transfer_status,
            reference=data.get("reference", ""),
            provider_reference=str(data.get("id", "")),
            amount=Decimal(str(data.get("amount", 0))) / 100,
            currency=data.get("currency", ""),
            raw_data=payload
        )
        return parsed_data
    
    def _determine_payment_status(self, event: str, transaction_status: str) -> PaymentStatus:
        """Determine payment status from event and transaction status."""
        status_mapping = {
            "success": PaymentStatus.COMPLETED,
            "failed": PaymentStatus.FAILED,
            "abandoned": PaymentStatus.ABANDONED,
            "reversed": PaymentStatus.REVERSED,
            "pending": PaymentStatus.PENDING
        }
        return status_mapping.get(transaction_status, PaymentStatus.PENDING)
    
    def _determine_transfer_status(self, event: str, status: str) -> TransferStatus:
        """Determine transfer status from event and status."""
        status_mapping = {
            "success": TransferStatus.COMPLETED,
            "failed": TransferStatus.FAILED,
            "pending": TransferStatus.PENDING,
            "reversed": TransferStatus.REVERSED
        }
        return status_mapping.get(status, TransferStatus.PENDING)