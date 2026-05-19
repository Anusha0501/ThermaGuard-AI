"""
Alert service.

Handles alert generation and delivery via Twilio SMS.
"""

from datetime import datetime
from typing import Optional
from twilio.rest import Client
from thermaguard.config import settings
from thermaguard.logger import logger


class AlertService:
    """
    Service for generating and sending alerts.
    
    Supports:
    - Twilio SMS alerts
    - Alert formatting
    - Alert delivery tracking
    """
    
    def __init__(self):
        """Initialize alert service."""
        self.twilio_client: Optional[Client] = None
        if settings.twilio_account_sid and settings.twilio_auth_token:
            self.twilio_client = Client(
                settings.twilio_account_sid,
                settings.twilio_auth_token
            )
            logger.info("Twilio client initialized")
        else:
            logger.warning("Twilio credentials not configured - alerts will be logged only")
    
    def format_alert_message(
        self,
        chamber_id: str,
        time_to_failure_hours: float
    ) -> str:
        """
        Format alert message according to specification.
        
        Format: "⚠️ Chamber X will exceed safe temperature in Y hours"
        
        Args:
            chamber_id: Chamber identifier
            time_to_failure_hours: Hours until failure
            
        Returns:
            Formatted alert message
        """
        return f"⚠️ Chamber {chamber_id} will exceed safe temperature in {time_to_failure_hours:.1f} hours"
    
    def send_sms_alert(
        self,
        message: str,
        to_number: Optional[str] = None
    ) -> bool:
        """
        Send SMS alert via Twilio.
        
        Args:
            message: Alert message
            to_number: Recipient phone number (uses config if not provided)
            
        Returns:
            True if sent successfully, False otherwise
        """
        if not settings.alert_enabled:
            logger.info(f"Alerts disabled - would send: {message}")
            return True
        
        if not self.twilio_client:
            logger.warning(f"Twilio not configured - logging alert: {message}")
            return True  # Log as success for development
        
        try:
            to = to_number or settings.twilio_to_number
            from_number = settings.twilio_from_number
            
            if not to or not from_number:
                logger.warning("Twilio phone numbers not configured")
                return False
            
            message_obj = self.twilio_client.messages.create(
                body=message,
                from_=from_number,
                to=to
            )
            
            logger.info(f"SMS alert sent: SID={message_obj.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send SMS alert: {e}")
            return False
    
    def send_alert(
        self,
        chamber_id: str,
        time_to_failure_hours: float,
        severity: str = "high"
    ) -> bool:
        """
        Send alert with appropriate formatting.
        
        Args:
            chamber_id: Chamber identifier
            time_to_failure_hours: Hours until failure
            severity: Alert severity level
            
        Returns:
            True if sent successfully, False otherwise
        """
        message = self.format_alert_message(chamber_id, time_to_failure_hours)
        
        logger.warning(
            f"ALERT [{severity}]: {message}"
        )
        
        return self.send_sms_alert(message)


# Global service instance
alert_service = AlertService()
