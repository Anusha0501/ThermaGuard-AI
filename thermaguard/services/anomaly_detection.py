"""
Anomaly detection service.

Handles early detection of temperature anomalies using statistical methods.
"""

from datetime import datetime, timedelta
from typing import List, Optional, Tuple
import numpy as np
import pandas as pd
from thermaguard.config import settings
from thermaguard.logger import logger


class AnomalyDetectionService:
    """
    Service for detecting temperature anomalies.
    
    Uses multiple detection strategies:
    1. Threshold-based: Check if forecast exceeds safe temperature range
    2. Statistical: Detect deviations from expected patterns
    3. Trend-based: Identify concerning temperature trends
    """
    
    def __init__(self):
        """Initialize anomaly detection service."""
        self.alert_cooldowns: dict = {}  # Track alert cooldowns per chamber
        logger.info("Anomaly detection service initialized")
    
    def detect_threshold_breach(
        self,
        forecast_df: pd.DataFrame,
        safe_temp_min: float,
        safe_temp_max: float
    ) -> Optional[Tuple[datetime, float]]:
        """
        Detect if forecast will breach safe temperature thresholds.
        
        Args:
            forecast_df: Prophet forecast DataFrame
            safe_temp_min: Minimum safe temperature
            safe_temp_max: Maximum safe temperature
            
        Returns:
            Tuple of (breach_time, predicted_temp) or None if no breach
        """
        try:
            # Check upper bound breach (too warm - dangerous for frozen goods)
            upper_breach = forecast_df[forecast_df['yhat_upper'] > safe_temp_max]
            if not upper_breach.empty:
                first_breach = upper_breach.iloc[0]
                return (first_breach['ds'], first_breach['yhat'])
            
            # Check lower bound breach (too cold - equipment failure)
            lower_breach = forecast_df[forecast_df['yhat_lower'] < safe_temp_min]
            if not lower_breach.empty:
                first_breach = lower_breach.iloc[0]
                return (first_breach['ds'], first_breach['yhat'])
            
            return None
            
        except Exception as e:
            logger.error(f"Failed threshold breach detection: {e}")
            raise
    
    def detect_statistical_anomaly(
        self,
        current_temp: float,
        historical_temps: List[float],
        threshold_std: float = 2.5
    ) -> bool:
        """
        Detect if current temperature is statistically anomalous.
        
        Uses Z-score based detection:
        - Z-score > threshold_std indicates anomaly
        - Threshold of 2.5 captures ~99% of normal data (assuming normal distribution)
        
        Args:
            current_temp: Current temperature reading
            historical_temps: List of recent historical temperatures
            threshold_std: Standard deviation threshold
            
        Returns:
            True if anomalous, False otherwise
        """
        try:
            if len(historical_temps) < 10:
                return False  # Not enough data
            
            mean_temp = np.mean(historical_temps)
            std_temp = np.std(historical_temps)
            
            if std_temp == 0:
                return False  # No variance in data
            
            z_score = abs(current_temp - mean_temp) / std_temp
            
            is_anomaly = z_score > threshold_std
            
            if is_anomaly:
                logger.warning(
                    f"Statistical anomaly detected: temp={current_temp}, "
                    f"mean={mean_temp:.2f}, std={std_temp:.2f}, z-score={z_score:.2f}"
                )
            
            return is_anomaly
            
        except Exception as e:
            logger.error(f"Failed statistical anomaly detection: {e}")
            raise
    
    def detect_trend_anomaly(
        self,
        historical_temps: List[float],
        window_size: int = 30
    ) -> Optional[str]:
        """
        Detect concerning temperature trends.
        
        Args:
            historical_temps: List of historical temperatures
            window_size: Size of rolling window for trend calculation
            
        Returns:
            Trend direction ('increasing', 'decreasing') or None
        """
        try:
            if len(historical_temps) < window_size * 2:
                return None  # Not enough data
            
            # Calculate trend using linear regression on recent window
            recent_temps = historical_temps[-window_size:]
            x = np.arange(len(recent_temps))
            y = np.array(recent_temps)
            
            # Simple linear regression
            slope = np.polyfit(x, y, 1)[0]
            
            # Determine if trend is concerning
            if slope > 0.1:  # Increasing temperature (warming up - bad for frozen goods)
                return "increasing"
            elif slope < -0.1:  # Decreasing temperature (cooling down - potential equipment issue)
                return "decreasing"
            
            return None
            
        except Exception as e:
            logger.error(f"Failed trend anomaly detection: {e}")
            raise
    
    def calculate_time_to_failure(
        self,
        breach_time: datetime,
        current_time: datetime
    ) -> float:
        """
        Calculate hours until predicted failure.
        
        Args:
            breach_time: Predicted time of threshold breach
            current_time: Current timestamp
            
        Returns:
            Hours until failure
        """
        time_delta = breach_time - current_time
        return time_delta.total_seconds() / 3600  # Convert to hours
    
    def check_alert_cooldown(self, chamber_id: str) -> bool:
        """
        Check if chamber is in alert cooldown period.
        
        Args:
            chamber_id: Chamber identifier
            
        Returns:
            True if in cooldown, False otherwise
        """
        if chamber_id not in self.alert_cooldowns:
            return False
        
        cooldown_end = self.alert_cooldowns[chamber_id]
        if datetime.now() > cooldown_end:
            del self.alert_cooldowns[chamber_id]
            return False
        
        return True
    
    def set_alert_cooldown(self, chamber_id: str):
        """
        Set alert cooldown for a chamber.
        
        Args:
            chamber_id: Chamber identifier
        """
        cooldown_end = datetime.now() + timedelta(minutes=settings.alert_cooldown_minutes)
        self.alert_cooldowns[chamber_id] = cooldown_end
        logger.info(f"Alert cooldown set for chamber {chamber_id} until {cooldown_end}")


# Global service instance
anomaly_detection_service = AnomalyDetectionService()
