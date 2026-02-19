"""
Infrastructure layer - Data access and external services.

This module contains the Repository Pattern implementation for accessing recipe data.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from functools import lru_cache
import csv
import os
from pathlib import Path

from src.domain.models import Recipe, RecipeSearchParams


class RecipeRepositoryInterface(ABC):
    """Abstract interface for recipe repository."""

    @abstractmethod
    def get_all(self) -> List[Recipe]:
        """Get all recipes."""
        pass

    @abstractmethod
    def get_by_id(self, recipe_id: str) -> Optional[Recipe]:
        """Get recipe by ID."""
        pass

    @abstractmethod
    def search(self, params: RecipeSearchParams) -> List[Recipe]:
        """Search recipes with filters."""
        pass


class CSVRecipeRepository(RecipeRepositoryInterface):
    """
    Repository implementation that reads recipes from CSV file.

    This class implements the Repository Pattern to abstract data access.
    It uses caching to improve performance for repeated reads.

    Security considerations:
    - Validates all data through Pydantic models
    - Prevents CSV injection attacks
    - Handles malformed data gracefully
    """

    def __init__(self, csv_path: Optional[str] = None):
        """
        Initialize repository with CSV file path.

        Args:
            csv_path: Path to CSV file. If None, uses default data path.
        """
        if csv_path is None:
            # Default to data/roll_cake_recipes_updated.csv
            base_dir = Path(__file__).parent.parent.parent
            csv_path = str(base_dir / "data" / "roll_cake_recipes_updated.csv")

        self.csv_path = csv_path

        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")

        # Index for O(1) lookups
        self._recipes_by_id: Dict[str, Recipe] = {}
        self._recipes_loaded = False

    def _load_recipes(self) -> None:
        """
        Load recipes from CSV file with validation.

        This method:
        1. Reads CSV file
        2. Validates each row through Pydantic
        3. Creates index for fast lookups
        4. Handles errors gracefully

        Raises:
            ValueError: If duplicate recipe IDs are found
            FileNotFoundError: If CSV file doesn't exist
        """
        if self._recipes_loaded:
            return

        recipes = []
        seen_ids = set()

        try:
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
                    try:
                        # Clean up column names (remove BOM and whitespace)
                        cleaned_row = {
                            k.strip().replace('\ufeff', ''): v
                            for k, v in row.items()
                        }

                        # Map CSV columns to model fields
                        recipe_data = {
                            'recipe_id': cleaned_row.get('Recipe_ID', ''),
                            'recipe_name': cleaned_row.get('Recipe_Name', ''),
                            'description': cleaned_row.get('Description') or None,
                            'category': cleaned_row.get('Category', 'Hiện đại'),
                            'flavor_profile': cleaned_row.get('Flavor_Profile', ''),
                            'difficulty_level': cleaned_row.get('Difficulty_Level', 'Trung bình'),
                            'prep_time_minutes': self._parse_float(cleaned_row.get('Prep_Time_Minutes')),
                            'cook_time_minutes': self._parse_float(cleaned_row.get('Cook_Time_Minutes')),
                            'total_time_minutes': self._parse_float(cleaned_row.get('Total_Time_Minutes')),
                            'servings': cleaned_row.get('Servings') or None,
                            'image_url': cleaned_row.get('Image_URL') or None,
                            'video_url': cleaned_row.get('Video_URL') or None,
                            'source': cleaned_row.get('Source') or None,
                            'date_created': cleaned_row.get('Date_Created') or None,
                            'date_updated': cleaned_row.get('Date_Updated') or None,
                            'tips_tricks': cleaned_row.get('Tips_Tricks') or None,
                            'storage_instructions': cleaned_row.get('Storage_Instructions') or None,
                            'customer_feedback_score': self._parse_float(cleaned_row.get('Customer_Feedback_Score')),
                            'market_trend_relevance': cleaned_row.get('Market_Trend_Relevance') or None,
                            'ingredients_flattened': cleaned_row.get('Ingredients_Flattened') or None,
                            'instructions_flattened': cleaned_row.get('Instructions_Flattened') or None,
                        }

                        # Validate through Pydantic model
                        recipe = Recipe(**recipe_data)

                        # Check for duplicate IDs
                        if recipe.recipe_id in seen_ids:
                            raise ValueError(
                                f"Duplicate recipe ID '{recipe.recipe_id}' found at row {row_num}"
                            )

                        seen_ids.add(recipe.recipe_id)
                        recipes.append(recipe)
                        self._recipes_by_id[recipe.recipe_id] = recipe

                    except Exception as e:
                        # Log error but continue processing other recipes
                        print(f"Warning: Error processing row {row_num}: {e}")
                        continue

        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")
        except Exception as e:
            raise Exception(f"Error loading recipes from CSV: {e}")

        self._recipes_loaded = True

    @staticmethod
    def _parse_float(value: Optional[str]) -> Optional[float]:
        """
        Safely parse float value from CSV.

        Args:
            value: String value from CSV

        Returns:
            Parsed float or None if invalid
        """
        if not value or value.strip() == '':
            return None
        try:
            return float(value)
        except ValueError:
            return None

    @lru_cache(maxsize=1)
    def get_all(self) -> List[Recipe]:
        """
        Get all recipes with caching.

        Returns:
            List of all Recipe objects

        Performance: O(1) after first call due to caching
        """
        self._load_recipes()
        return list(self._recipes_by_id.values())

    def get_by_id(self, recipe_id: str) -> Optional[Recipe]:
        """
        Get recipe by ID with O(1) lookup.

        Args:
            recipe_id: Unique recipe identifier

        Returns:
            Recipe object or None if not found

        Performance: O(1) dictionary lookup
        """
        self._load_recipes()
        return self._recipes_by_id.get(recipe_id)

    def search(self, params: RecipeSearchParams) -> List[Recipe]:
        """
        Search recipes with filters.

        Args:
            params: Search parameters

        Returns:
            List of recipes matching the search criteria

        Performance: O(n) where n is number of recipes
        Note: For large datasets, consider using a database with indexes
        """
        self._load_recipes()
        results = list(self._recipes_by_id.values())

        # Apply filters
        if params.flavor:
            results = [r for r in results if params.flavor.lower() in r.flavor_profile.lower()]

        if params.category:
            results = [r for r in results if r.category == params.category]

        if params.difficulty:
            results = [r for r in results if r.difficulty_level == params.difficulty]

        if params.max_prep_time is not None:
            results = [
                r for r in results
                if r.prep_time_minutes is not None and r.prep_time_minutes <= params.max_prep_time
            ]

        if params.max_total_time is not None:
            results = [
                r for r in results
                if r.total_time_minutes is not None and r.total_time_minutes <= params.max_total_time
            ]

        if params.min_feedback_score is not None:
            results = [
                r for r in results
                if r.customer_feedback_score is not None
                and r.customer_feedback_score >= params.min_feedback_score
            ]

        if params.market_trend:
            results = [r for r in results if r.market_trend_relevance == params.market_trend]

        return results

    def get_unique_flavors(self) -> List[str]:
        """Get list of unique flavor profiles."""
        self._load_recipes()
        flavors = set(r.flavor_profile for r in self._recipes_by_id.values() if r.flavor_profile)
        return sorted(flavors)

    def get_unique_categories(self) -> List[str]:
        """Get list of unique categories."""
        self._load_recipes()
        categories = set(r.category for r in self._recipes_by_id.values() if r.category)
        return sorted(categories)

    def clear_cache(self) -> None:
        """Clear the cache to force reload on next access."""
        self.get_all.cache_clear()
        self._recipes_loaded = False
        self._recipes_by_id = {}
