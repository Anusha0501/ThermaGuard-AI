"""
API route modules.

Contains all API route handlers organized by functionality.
"""

from thermaguard.api.routes import ingest, forecast, alerts, status

__all__ = ["ingest", "forecast", "alerts", "status"]
