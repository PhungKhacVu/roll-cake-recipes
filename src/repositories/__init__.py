"""
Repository interfaces and implementations.
Interface Segregation Principle: Define interfaces for data access.
Dependency Inversion Principle: Depend on abstractions, not concrete implementations.
"""
from .base_repository import IRepository
from .csv_repository import CSVRecipeRepository

__all__ = ['IRepository', 'CSVRecipeRepository']
