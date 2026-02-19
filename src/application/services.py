"""
Application layer - Business logic and use cases.

This module contains services that orchestrate business operations.
"""

from typing import List, Optional
from collections import Counter
import random

from src.domain.models import Recipe, RecipeSearchParams, RecipeStatistics
from src.infrastructure.repositories import RecipeRepositoryInterface


class RecipeService:
    """
    Service class for recipe business logic.

    This class implements the Service Pattern to encapsulate business logic
    and coordinate between different parts of the application.
    """

    def __init__(self, repository: RecipeRepositoryInterface):
        """
        Initialize service with repository.

        Args:
            repository: Recipe repository implementation
        """
        self.repository = repository

    def get_all_recipes(self, limit: Optional[int] = None, offset: int = 0) -> List[Recipe]:
        """
        Get all recipes with pagination support.

        Args:
            limit: Maximum number of recipes to return
            offset: Number of recipes to skip

        Returns:
            List of Recipe objects
        """
        recipes = self.repository.get_all()

        # Apply pagination
        if limit is not None:
            return recipes[offset:offset + limit]
        return recipes[offset:]

    def get_recipe_by_id(self, recipe_id: str) -> Optional[Recipe]:
        """
        Get a single recipe by ID.

        Args:
            recipe_id: Unique recipe identifier

        Returns:
            Recipe object or None if not found
        """
        return self.repository.get_by_id(recipe_id)

    def search_recipes(self, params: RecipeSearchParams) -> List[Recipe]:
        """
        Search recipes with filters.

        Args:
            params: Search parameters

        Returns:
            List of matching recipes
        """
        return self.repository.search(params)

    def get_random_recipe(self) -> Optional[Recipe]:
        """
        Get a random recipe.

        Returns:
            Random Recipe object or None if no recipes exist
        """
        recipes = self.repository.get_all()
        if not recipes:
            return None
        return random.choice(recipes)

    def get_recipes_by_flavor(self, flavor: str) -> List[Recipe]:
        """
        Get all recipes with a specific flavor profile.

        Args:
            flavor: Flavor profile to search for

        Returns:
            List of recipes with matching flavor
        """
        params = RecipeSearchParams(flavor=flavor)
        return self.repository.search(params)

    def get_recipes_by_difficulty(self, difficulty: str) -> List[Recipe]:
        """
        Get all recipes with a specific difficulty level.

        Args:
            difficulty: Difficulty level to filter by

        Returns:
            List of recipes with matching difficulty
        """
        params = RecipeSearchParams(difficulty=difficulty)
        return self.repository.search(params)

    def get_quick_recipes(self, max_minutes: float = 60) -> List[Recipe]:
        """
        Get recipes that can be completed quickly.

        Args:
            max_minutes: Maximum total time in minutes

        Returns:
            List of quick recipes
        """
        params = RecipeSearchParams(max_total_time=max_minutes)
        return self.repository.search(params)

    def get_statistics(self) -> RecipeStatistics:
        """
        Calculate statistics about the recipe collection.

        Returns:
            RecipeStatistics object with various metrics
        """
        recipes = self.repository.get_all()

        if not recipes:
            return RecipeStatistics(
                total_recipes=0,
                by_category={},
                by_difficulty={},
                by_flavor={},
                by_market_trend={},
            )

        # Count by category
        categories = Counter(r.category for r in recipes if r.category)

        # Count by difficulty
        difficulties = Counter(r.difficulty_level for r in recipes if r.difficulty_level)

        # Count by flavor
        flavors = Counter(r.flavor_profile for r in recipes if r.flavor_profile)

        # Count by market trend
        trends = Counter(r.market_trend_relevance for r in recipes if r.market_trend_relevance)

        # Calculate averages
        prep_times = [r.prep_time_minutes for r in recipes if r.prep_time_minutes is not None]
        avg_prep = sum(prep_times) / len(prep_times) if prep_times else None

        cook_times = [r.cook_time_minutes for r in recipes if r.cook_time_minutes is not None]
        avg_cook = sum(cook_times) / len(cook_times) if cook_times else None

        feedback_scores = [
            r.customer_feedback_score
            for r in recipes
            if r.customer_feedback_score is not None
        ]
        avg_feedback = sum(feedback_scores) / len(feedback_scores) if feedback_scores else None

        return RecipeStatistics(
            total_recipes=len(recipes),
            by_category=dict(categories),
            by_difficulty=dict(difficulties),
            by_flavor=dict(flavors),
            by_market_trend=dict(trends),
            avg_prep_time=round(avg_prep, 2) if avg_prep else None,
            avg_cook_time=round(avg_cook, 2) if avg_cook else None,
            avg_feedback_score=round(avg_feedback, 2) if avg_feedback else None,
        )

    def get_available_flavors(self) -> List[str]:
        """
        Get list of all available flavor profiles.

        Returns:
            Sorted list of unique flavors
        """
        return self.repository.get_unique_flavors()

    def get_available_categories(self) -> List[str]:
        """
        Get list of all available categories.

        Returns:
            Sorted list of unique categories
        """
        return self.repository.get_unique_categories()

    def get_trending_recipes(self, limit: int = 10) -> List[Recipe]:
        """
        Get recipes with high market trend relevance.

        Args:
            limit: Maximum number of recipes to return

        Returns:
            List of trending recipes
        """
        params = RecipeSearchParams(market_trend="Cao")
        recipes = self.repository.search(params)
        return recipes[:limit]

    def get_highly_rated_recipes(self, min_score: float = 4.0, limit: int = 10) -> List[Recipe]:
        """
        Get highly rated recipes.

        Args:
            min_score: Minimum feedback score
            limit: Maximum number of recipes to return

        Returns:
            List of highly rated recipes
        """
        params = RecipeSearchParams(min_feedback_score=min_score)
        recipes = self.repository.search(params)

        # Sort by score descending
        recipes.sort(
            key=lambda r: r.customer_feedback_score or 0,
            reverse=True
        )

        return recipes[:limit]
