#!/usr/bin/env python3
"""
Script to generate synthetic temperature data for testing.

Usage:
    python scripts/generate_data.py
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from thermaguard.data.generator import generate_sample_data
from thermaguard.logger import logger


def main():
    """Main function to generate sample data."""
    logger.info("Starting synthetic data generation...")
    
    try:
        saved_files = generate_sample_data()
        logger.info(f"Successfully generated {len(saved_files)} data files")
        for filepath in saved_files:
            logger.info(f"  - {filepath}")
        
        return 0
    except Exception as e:
        logger.error(f"Failed to generate data: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
