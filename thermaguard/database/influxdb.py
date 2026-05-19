"""
InfluxDB client.

Handles time-series data storage and retrieval using InfluxDB.
"""

from datetime import datetime, timedelta
from typing import List, Optional
import pandas as pd
from influxdb_client import InfluxDBClient as InfluxClient
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS
from thermaguard.config import settings
from thermaguard.logger import logger


class InfluxDBClient:
    """
    InfluxDB client for time-series sensor data.
    
    InfluxDB is ideal for this use case because:
    - Optimized for time-series data
    - High write throughput
    - Efficient time-based queries
    - Built-in downsampling and retention
    """
    
    def __init__(self):
        """Initialize InfluxDB client."""
        self.client: Optional[InfluxClient] = None
        self.write_api = None
        self.query_api = None
        self._connect()
    
    def _connect(self):
        """Establish connection to InfluxDB."""
        try:
            self.client = InfluxClient(
                url=settings.influxdb_url,
                token=settings.influxdb_token,
                org=settings.influxdb_org
            )
            self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
            self.query_api = self.client.query_api()
            logger.info("Connected to InfluxDB")
        except Exception as e:
            logger.error(f"Failed to connect to InfluxDB: {e}")
            # For development, continue without InfluxDB
            logger.warning("Running without InfluxDB - using mock storage")
    
    def write_reading(
        self,
        chamber_id: str,
        timestamp: datetime,
        temperature: float,
        sensor_id: Optional[str] = None
    ) -> bool:
        """
        Write a single sensor reading to InfluxDB.
        
        Args:
            chamber_id: Chamber identifier
            timestamp: Reading timestamp
            temperature: Temperature value
            sensor_id: Sensor identifier
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.client:
                logger.warning("InfluxDB not connected - skipping write")
                return False
            
            point = {
                "measurement": "temperature",
                "tags": {
                    "chamber_id": chamber_id,
                    "sensor_id": sensor_id or "unknown"
                },
                "fields": {
                    "temperature": temperature
                },
                "time": timestamp
            }
            
            self.write_api.write(
                bucket=settings.influxdb_bucket,
                record=point
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to write reading to InfluxDB: {e}")
            return False
    
    def query_historical_data(
        self,
        chamber_id: str,
        start_time: datetime,
        end_time: datetime
    ) -> pd.DataFrame:
        """
        Query historical temperature data for a chamber.
        
        Args:
            chamber_id: Chamber identifier
            start_time: Query start time
            end_time: Query end time
            
        Returns:
            DataFrame with historical data
        """
        try:
            if not self.client:
                logger.warning("InfluxDB not connected - returning empty DataFrame")
                return pd.DataFrame()
            
            query = f'''
                from(bucket: "{settings.influxdb_bucket}")
                  |> range(start: {start_time.isoformat()}Z, stop: {end_time.isoformat()}Z)
                  |> filter(fn: (r) => r["_measurement"] == "temperature")
                  |> filter(fn: (r) => r["chamber_id"] == "{chamber_id}")
                  |> filter(fn: (r) => r["_field"] == "temperature")
            '''
            
            result = self.query_api.query(query)
            
            # Convert to DataFrame
            records = []
            for table in result:
                for record in table.records:
                    records.append({
                        "ds": record.get_time(),
                        "y": record.get_value()
                    })
            
            df = pd.DataFrame(records)
            if not df.empty:
                df = df.sort_values("ds")
            
            return df
            
        except Exception as e:
            logger.error(f"Failed to query historical data: {e}")
            return pd.DataFrame()
    
    def query_latest_reading(
        self,
        chamber_id: str
    ) -> Optional[dict]:
        """
        Query the latest reading for a chamber.
        
        Args:
            chamber_id: Chamber identifier
            
        Returns:
            Latest reading dict or None
        """
        try:
            if not self.client:
                return None
            
            query = f'''
                from(bucket: "{settings.influxdb_bucket}")
                  |> range(start: -1h)
                  |> filter(fn: (r) => r["_measurement"] == "temperature")
                  |> filter(fn: (r) => r["chamber_id"] == "{chamber_id}")
                  |> filter(fn: (r) => r["_field"] == "temperature")
                  |> last()
            '''
            
            result = self.query_api.query(query)
            
            for table in result:
                for record in table.records:
                    return {
                        "timestamp": record.get_time(),
                        "temperature": record.get_value(),
                        "sensor_id": record.values.get("sensor_id")
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to query latest reading: {e}")
            return None
    
    def close(self):
        """Close InfluxDB connection."""
        if self.client:
            self.client.close()
            logger.info("InfluxDB connection closed")


# Global client instance
influxdb_client = InfluxDBClient()
