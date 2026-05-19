"""
Prophet forecasting service.

Handles time-series forecasting using Facebook Prophet.
"""

from datetime import datetime, timedelta
from typing import Optional
import pandas as pd
from prophet import Prophet
from thermaguard.logger import logger


class ForecastingService:
    """
    Service for temperature forecasting using Prophet.
    
    Prophet is excellent for time-series with:
    - Strong seasonality (daily, weekly patterns)
    - Holiday effects
    - Trend changes
    - Outlier handling
    """
    
    def __init__(self):
        """Initialize forecasting service."""
        self.models: dict = {}  # Cache trained models per chamber
        logger.info("Forecasting service initialized")
    
    def train_model(
        self,
        chamber_id: str,
        historical_data: pd.DataFrame,
        forecast_horizon_hours: int = 6
    ) -> Prophet:
        """
        Train a Prophet model for a chamber.
        
        Args:
            chamber_id: Chamber identifier
            historical_data: DataFrame with 'ds' (datetime) and 'y' (temperature) columns
            forecast_horizon_hours: Hours to forecast ahead
            
        Returns:
            Trained Prophet model
        """
        try:
            logger.info(f"Training Prophet model for chamber {chamber_id}")
            
            # Initialize Prophet with appropriate parameters for cold-chain data
            model = Prophet(
                yearly_seasonality=False,  # No yearly seasonality for short-term monitoring
                weekly_seasonality=True,    # Weekly patterns (e.g., maintenance schedules)
                daily_seasonality=True,     # Daily patterns (e.g., day/night cycles)
                changepoint_prior_scale=0.05,  # Conservative trend changes
                seasonality_prior_scale=10.0,  # Strong seasonality
                holidays_prior_scale=10.0,     # Strong holiday effects
                interval_width=0.95,      # 95% confidence intervals
            )
            
            # Add custom seasonality for cold-chain specific patterns
            model.add_seasonality(
                name='hourly',
                period=1/24,  # Hourly pattern
                fourier_order=5,
            )
            
            # Fit model
            model.fit(historical_data)
            
            # Cache model
            self.models[chamber_id] = model
            
            logger.info(f"Model trained successfully for chamber {chamber_id}")
            return model
            
        except Exception as e:
            logger.error(f"Failed to train model for chamber {chamber_id}: {e}")
            raise
    
    def generate_forecast(
        self,
        chamber_id: str,
        model: Prophet,
        forecast_horizon_hours: int = 6
    ) -> pd.DataFrame:
        """
        Generate forecast using trained model.
        
        Args:
            chamber_id: Chamber identifier
            model: Trained Prophet model
            forecast_horizon_hours: Hours to forecast ahead
            
        Returns:
            DataFrame with forecast data
        """
        try:
            logger.info(f"Generating {forecast_horizon_hours}h forecast for chamber {chamber_id}")
            
            # Create future dataframe
            future = model.make_future_dataframe(
                periods=forecast_horizon_hours * 60,  # Convert to minutes
                freq='1min',  # 1-minute intervals
                include_history=False
            )
            
            # Generate forecast
            forecast = model.predict(future)
            
            logger.info(f"Forecast generated for chamber {chamber_id}")
            return forecast
            
        except Exception as e:
            logger.error(f"Failed to generate forecast for chamber {chamber_id}: {e}")
            raise
    
    def get_model(self, chamber_id: str) -> Optional[Prophet]:
        """
        Get cached model for a chamber.
        
        Args:
            chamber_id: Chamber identifier
            
        Returns:
            Cached Prophet model or None
        """
        return self.models.get(chamber_id)


# Global service instance
forecasting_service = ForecastingService()
