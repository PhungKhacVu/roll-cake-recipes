"""
CSV-based repository implementation.
Single Responsibility Principle: Handles CSV data access only.
"""
import csv
from typing import List, Optional, Dict, Any
from datetime import datetime
from ..models import Recipe, Ingredient
from .base_repository import IRepository


class CSVRecipeRepository(IRepository):
    """
    Repository for accessing recipe data from CSV files.
    Implements IRepository interface.
    """
    
    def __init__(self, csv_file_path: str):
        """Initialize repository with CSV file path."""
        self.csv_file_path = csv_file_path
        self._recipes_cache: Optional[List[Recipe]] = None
    
    def _load_recipes(self) -> List[Recipe]:
        """Load recipes from CSV file."""
        if self._recipes_cache is not None:
            return self._recipes_cache
        
        recipes = []
        with open(self.csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                recipe = self._parse_recipe_row(row)
                recipes.append(recipe)
        
        self._recipes_cache = recipes
        return recipes
    
    def _parse_recipe_row(self, row: Dict[str, str]) -> Recipe:
        """Parse a CSV row into a Recipe object."""
        # Parse ingredients
        ingredients = self._parse_ingredients(row.get('Ingredients_Flattened', ''))
        
        # Parse instructions
        instructions = self._parse_instructions(row.get('Instructions_Flattened', ''))
        
        # Parse dates
        date_created = self._parse_date(row.get('Date_Created'))
        date_updated = self._parse_date(row.get('Date_Updated'))
        
        # Parse numeric fields
        prep_time = self._parse_float(row.get('Prep_Time_Minutes'))
        cook_time = self._parse_float(row.get('Cook_Time_Minutes'))
        total_time = self._parse_float(row.get('Total_Time_Minutes'))
        feedback_score = self._parse_float(row.get('Customer_Feedback_Score'))
        
        return Recipe(
            recipe_id=row.get('Recipe_ID', ''),
            name=row.get('Recipe_Name', ''),
            description=row.get('Description', ''),
            category=row.get('Category', ''),
            flavor_profile=row.get('Flavor_Profile', ''),
            difficulty_level=row.get('Difficulty_Level', ''),
            prep_time_minutes=prep_time,
            cook_time_minutes=cook_time,
            total_time_minutes=total_time,
            servings=row.get('Servings'),
            image_url=row.get('Image_URL'),
            video_url=row.get('Video_URL'),
            source=row.get('Source'),
            date_created=date_created,
            date_updated=date_updated,
            ingredients=ingredients,
            instructions=instructions,
            tips_tricks=row.get('Tips_Tricks'),
            storage_instructions=row.get('Storage_Instructions'),
            customer_feedback_score=feedback_score,
            market_trend_relevance=row.get('Market_Trend_Relevance')
        )
    
    def _parse_ingredients(self, ingredients_str: str) -> List[Ingredient]:
        """Parse ingredients from flattened string format."""
        if not ingredients_str:
            return []
        
        ingredients = []
        # Format: "Name1: Quantity1Unit1 (Notes1); Name2: Quantity2Unit2 (Notes2)"
        parts = ingredients_str.split(';')
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            try:
                # Split by colon to separate name from quantity/unit
                if ':' in part:
                    name, rest = part.split(':', 1)
                    name = name.strip()
                    rest = rest.strip()
                    
                    # Extract notes if present
                    notes = None
                    if '(' in rest and ')' in rest:
                        rest, notes_part = rest.rsplit('(', 1)
                        notes = notes_part.rstrip(')')
                        rest = rest.strip()
                    
                    # Try to parse quantity and unit
                    quantity = None
                    unit = None
                    parts_rest = rest.split(None, 1)  # Split on whitespace
                    if len(parts_rest) >= 1:
                        try:
                            quantity = float(parts_rest[0].replace(',', '.'))
                            if len(parts_rest) > 1:
                                unit = parts_rest[1]
                        except ValueError:
                            # If can't parse as number, treat all as unit
                            unit = rest if rest != 'None' else None
                    
                    ingredients.append(Ingredient(
                        name=name,
                        quantity=quantity,
                        unit=unit,
                        notes=notes
                    ))
            except Exception:
                # If parsing fails, just skip this ingredient
                continue
        
        return ingredients
    
    def _parse_instructions(self, instructions_str: str) -> List[str]:
        """Parse instructions from flattened string format."""
        if not instructions_str:
            return []
        
        # Split by newline and filter empty lines
        instructions = [line.strip() for line in instructions_str.split('\n') if line.strip()]
        return instructions
    
    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse date string to datetime object."""
        if not date_str or date_str == '':
            return None
        
        try:
            return datetime.fromisoformat(date_str)
        except (ValueError, AttributeError):
            return None
    
    def _parse_float(self, value: Optional[str]) -> Optional[float]:
        """Parse string to float."""
        if not value or value == '':
            return None
        
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    def get_all(self) -> List[Recipe]:
        """Get all recipes."""
        return self._load_recipes()
    
    def get_by_id(self, recipe_id: str) -> Optional[Recipe]:
        """Get recipe by ID."""
        recipes = self._load_recipes()
        for recipe in recipes:
            if recipe.recipe_id == recipe_id:
                return recipe
        return None
    
    def filter(self, criteria: Dict[str, Any]) -> List[Recipe]:
        """
        Filter recipes by criteria.
        Supports filtering by: category, flavor_profile, difficulty_level, etc.
        """
        recipes = self._load_recipes()
        filtered = recipes
        
        for key, value in criteria.items():
            if value is None:
                continue
            
            filtered = [
                recipe for recipe in filtered
                if self._matches_criteria(recipe, key, value)
            ]
        
        return filtered
    
    def _matches_criteria(self, recipe: Recipe, key: str, value: Any) -> bool:
        """Check if recipe matches a specific criterion."""
        recipe_value = getattr(recipe, key, None)
        
        if recipe_value is None:
            return False
        
        # Case-insensitive string comparison
        if isinstance(value, str) and isinstance(recipe_value, str):
            return value.lower() in recipe_value.lower()
        
        return recipe_value == value
    
    def count(self) -> int:
        """Count total recipes."""
        return len(self._load_recipes())
    
    def clear_cache(self):
        """Clear the recipes cache to force reload."""
        self._recipes_cache = None
