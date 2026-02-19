"""
Configuration management.
Single Responsibility: Handles application configuration.
"""
import os
from pathlib import Path


class Config:
    """
    Application configuration.
    KISS Principle: Simple configuration management.
    """
    
    # Base paths
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DATA_DIR = BASE_DIR / 'data'
    SRC_DIR = BASE_DIR / 'src'
    
    # CSV file paths
    DEFAULT_CSV_FILE = BASE_DIR / 'roll_cake_recipes_updated.csv'
    LEGACY_CSV_FILE = BASE_DIR / 'roll_cake_recipes.csv'
    
    # Output paths
    OUTPUT_DIR = BASE_DIR / 'output'
    
    @classmethod
    def get_csv_path(cls, filename: str = None) -> str:
        """Get path to CSV file."""
        if filename:
            return str(cls.BASE_DIR / filename)
        return str(cls.DEFAULT_CSV_FILE)
    
    @classmethod
    def ensure_output_dir(cls):
        """Ensure output directory exists."""
        cls.OUTPUT_DIR.mkdir(exist_ok=True)
        return cls.OUTPUT_DIR
