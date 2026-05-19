"""
Tests for synthetic data generator.
"""

import pytest
import pandas as pd
from datetime import datetime
from thermaguard.data.generator import SyntheticDataGenerator


def test_generator_initialization():
    """Test that generator initializes correctly."""
    generator = SyntheticDataGenerator()
    assert generator.base_temp == -15.0
    assert generator.temp_std == 1.5


def test_normal_data_generation():
    """Test normal data generation."""
    generator = SyntheticDataGenerator()
    start_time = datetime(2024, 1, 1, 0, 0, 0)
    
    df = generator.generate_normal_data(start_time, duration_days=1)
    
    assert len(df) == 1440  # 24 hours * 60 minutes
    assert 'timestamp' in df.columns
    assert 'temperature' in df.columns
    assert df['temperature'].min() < -20  # Should have some variation
    assert df['temperature'].max() > -10


def test_gradual_failure():
    """Test gradual failure addition."""
    generator = SyntheticDataGenerator()
    start_time = datetime(2024, 1, 1, 0, 0, 0)
    
    df = generator.generate_normal_data(start_time, duration_days=1)
    original_mean = df['temperature'].mean()
    
    df_with_failure = generator.add_gradual_failure(
        df, start_index=1000, duration_hours=4, failure_rate=0.5
    )
    
    # Temperature should increase after failure start
    assert df_with_failure['temperature'].iloc[-1] > original_mean


def test_sudden_spike():
    """Test sudden spike addition."""
    generator = SyntheticDataGenerator()
    start_time = datetime(2024, 1, 1, 0, 0, 0)
    
    df = generator.generate_normal_data(start_time, duration_days=1)
    original_max = df['temperature'].max()
    
    df_with_spike = generator.add_sudden_spike(
        df, start_index=1000, duration_minutes=30, spike_magnitude=10.0
    )
    
    # Maximum temperature should increase
    assert df_with_spike['temperature'].max() > original_max


def test_complete_dataset():
    """Test complete dataset generation."""
    generator = SyntheticDataGenerator()
    start_time = datetime(2024, 1, 1, 0, 0, 0)
    
    datasets = generator.generate_complete_dataset(
        chamber_id="test",
        start_time=start_time,
        duration_days=7,
        num_chambers=3,
        failure_probability=1.0  # Force failures
    )
    
    assert len(datasets) == 3
    for df in datasets:
        assert 'chamber_id' in df.columns
        assert len(df) == 7 * 24 * 60  # 7 days of 1-min data
