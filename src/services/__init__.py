"""
Service layer for business logic.
Single Responsibility Principle: Each service handles specific business operations.
"""
from .recipe_service import RecipeService

__all__ = ['RecipeService']
