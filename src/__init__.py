"""
Main package initialization.
"""
from .models import Recipe, Ingredient
from .repositories import IRepository, CSVRecipeRepository
from .services import RecipeService
from .analytics import RecipeAnalyzer
from .config import Config

__version__ = '1.0.0'

__all__ = [
    'Recipe',
    'Ingredient',
    'IRepository',
    'CSVRecipeRepository',
    'RecipeService',
    'RecipeAnalyzer',
    'Config'
]
