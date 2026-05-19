"""
Ingest API routes.

Handles temperature sensor data ingestion endpoints.
"""

from fastapi import APIRouter, HTTPException, status
from thermaguard.models.sensor import SensorReading, SensorReadingBatch
from thermaguard.logger import logger

router = APIRouter()


@router.post("/ingest", response_model=dict, status_code=status.HTTP_201_CREATED)
async def ingest_reading(reading: SensorReading):
    """
    Ingest a single temperature sensor reading.
    
    Args:
        reading: Sensor reading data
        
    Returns:
        Confirmation of ingestion
    """
    try:
        logger.info(f"Ingesting reading for chamber {reading.chamber_id}")
        
        # TODO: Implement actual ingestion logic in Phase 3
        # - Store in InfluxDB
        # - Trigger real-time processing
        
        return {
            "status": "success",
            "chamber_id": reading.chamber_id,
            "timestamp": reading.timestamp.isoformat(),
            "message": "Reading ingested successfully"
        }
    except Exception as e:
        logger.error(f"Failed to ingest reading: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ingestion failed: {str(e)}"
        )


@router.post("/ingest/batch", response_model=dict, status_code=status.HTTP_201_CREATED)
async def ingest_batch(batch: SensorReadingBatch):
    """
    Ingest a batch of temperature sensor readings.
    
    Args:
        batch: Batch of sensor readings
        
    Returns:
        Confirmation of batch ingestion
    """
    try:
        logger.info(f"Ingesting batch of {len(batch.readings)} readings")
        
        # TODO: Implement actual batch ingestion logic in Phase 3
        # - Bulk insert to InfluxDB
        # - Batch processing optimization
        
        return {
            "status": "success",
            "count": len(batch.readings),
            "message": f"{len(batch.readings)} readings ingested successfully"
        }
    except Exception as e:
        logger.error(f"Failed to ingest batch: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch ingestion failed: {str(e)}"
        )
