"""
Status API routes.

Handles chamber status and health monitoring endpoints.
"""

from fastapi import APIRouter, HTTPException, status
from thermaguard.models.chamber import ChamberStatus
from thermaguard.logger import logger

router = APIRouter()


@router.get("/status/{chamber_id}", response_model=ChamberStatus)
async def get_chamber_status(chamber_id: str):
    """
    Get current status of a chamber.
    
    Args:
        chamber_id: Unique chamber identifier
        
    Returns:
        Chamber status information
    """
    try:
        logger.info(f"Retrieving status for chamber {chamber_id}")
        
        # TODO: Implement actual status retrieval in Phase 5
        # - Query latest readings
        # - Check threshold compliance
        # - Calculate health metrics
        
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Status endpoint not yet implemented - coming in Phase 5"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve chamber status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Status retrieval failed: {str(e)}"
        )


@router.get("/status")
async def get_all_chambers_status():
    """
    Get status of all chambers.
    
    Returns:
        List of all chamber statuses
    """
    try:
        logger.info("Retrieving status for all chambers")
        
        # TODO: Implement all chambers status retrieval in Phase 5
        
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="All chambers status endpoint not yet implemented - coming in Phase 5"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve all chamber statuses: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"All chambers status retrieval failed: {str(e)}"
        )
