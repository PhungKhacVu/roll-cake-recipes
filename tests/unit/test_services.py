"""
Unit tests for application services.

This test suite validates business logic in the service layer.
"""

import pytest
from unittest.mock import Mock

from src.application.services import RecipeService
from src.domain.models import Recipe, RecipeSearchParams, DifficultyLevel, Category


class TestRecipeService:
    """Test suite for RecipeService."""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository for testing."""
        mock_repo = Mock()

        # Sample test data
        mock_recipes = [
            Recipe(
                recipe_id="chocolate_001",
                recipe_name="Chocolate Roll",
                category=Category.MODERN,
                flavor_profile="Chocolate",
                difficulty_level=DifficultyLevel.EASY,
                prep_time_minutes=20,
                cook_time_minutes=15,
                total_time_minutes=35,
                customer_feedback_score=4.5,
                market_trend_relevance="Cao"
            ),
            Recipe(
                recipe_id="matcha_002",
                recipe_name="Matcha Roll",
                category=Category.TRADITIONAL,
                flavor_profile="Trà xanh",
                difficulty_level=DifficultyLevel.MEDIUM,
                prep_time_minutes=30,
                cook_time_minutes=20,
                total_time_minutes=50,
                customer_feedback_score=4.8,
                market_trend_relevance="Cao"
            ),
            Recipe(
                recipe_id="vanilla_003",
                recipe_name="Vanilla Roll",
                category=Category.MODERN,
                flavor_profile="Vanilla",
                difficulty_level=DifficultyLevel.EASY,
                prep_time_minutes=25,
                cook_time_minutes=15,
                total_time_minutes=40,
                customer_feedback_score=3.5,
                market_trend_relevance="Thấp"
            ),
        ]

        mock_repo.get_all.return_value = mock_recipes
        mock_repo.get_by_id.return_value = mock_recipes[0]
        mock_repo.search.return_value = [mock_recipes[0]]
        mock_repo.get_unique_flavors.return_value = ["Chocolate", "Trà xanh", "Vanilla"]
        mock_repo.get_unique_categories.return_value = ["Hiện đại", "Truyền thống"]

        return mock_repo

    @pytest.fixture
    def service(self, mock_repository):
        """Create service instance with mock repository."""
        return RecipeService(mock_repository)

    def test_get_all_recipes(self, service, mock_repository):
        """Test getting all recipes."""
        recipes = service.get_all_recipes()

        assert len(recipes) == 3
        mock_repository.get_all.assert_called_once()

    def test_get_all_recipes_with_pagination(self, service, mock_repository):
        """Test pagination of recipes."""
        recipes = service.get_all_recipes(limit=2, offset=1)

        # Should return recipes[1:3]
        assert len(recipes) == 2
        mock_repository.get_all.assert_called_once()

    def test_get_recipe_by_id(self, service, mock_repository):
        """Test getting recipe by ID."""
        recipe = service.get_recipe_by_id("chocolate_001")

        assert recipe is not None
        assert recipe.recipe_id == "chocolate_001"
        mock_repository.get_by_id.assert_called_once_with("chocolate_001")

    def test_search_recipes(self, service, mock_repository):
        """Test searching recipes."""
        params = RecipeSearchParams(flavor="Chocolate")
        results = service.search_recipes(params)

        assert len(results) == 1
        mock_repository.search.assert_called_once_with(params)

    def test_get_random_recipe(self, service, mock_repository):
        """Test getting random recipe."""
        recipe = service.get_random_recipe()

        assert recipe is not None
        assert isinstance(recipe, Recipe)
        mock_repository.get_all.assert_called_once()

    def test_get_random_recipe_empty_db(self, service):
        """Test getting random recipe when no recipes exist."""
        service.repository.get_all.return_value = []

        recipe = service.get_random_recipe()
        assert recipe is None

    def test_get_recipes_by_flavor(self, service, mock_repository):
        """Test getting recipes by flavor."""
        recipes = service.get_recipes_by_flavor("Chocolate")

        assert len(recipes) == 1
        # Verify search was called with correct params
        call_args = mock_repository.search.call_args
        assert call_args[0][0].flavor == "Chocolate"

    def test_get_recipes_by_difficulty(self, service, mock_repository):
        """Test getting recipes by difficulty."""
        recipes = service.get_recipes_by_difficulty("Dễ")

        assert len(recipes) == 1
        call_args = mock_repository.search.call_args
        assert call_args[0][0].difficulty == "Dễ"

    def test_get_quick_recipes(self, service, mock_repository):
        """Test getting quick recipes."""
        recipes = service.get_quick_recipes(max_minutes=45)

        assert len(recipes) == 1
        call_args = mock_repository.search.call_args
        assert call_args[0][0].max_total_time == 45

    def test_get_statistics(self, service):
        """Test calculating statistics."""
        stats = service.get_statistics()

        assert stats.total_recipes == 3
        assert stats.by_category == {"Hiện đại": 2, "Truyền thống": 1}
        assert stats.by_difficulty == {"Dễ": 2, "Trung bình": 1}
        assert stats.by_flavor == {"Chocolate": 1, "Trà xanh": 1, "Vanilla": 1}
        assert stats.avg_prep_time == 25.0  # (20 + 30 + 25) / 3
        assert stats.avg_cook_time == pytest.approx(16.67, rel=0.01)  # (15 + 20 + 15) / 3
        assert stats.avg_feedback_score == pytest.approx(4.27, rel=0.01)  # (4.5 + 4.8 + 3.5) / 3

    def test_get_statistics_empty_db(self, service):
        """Test statistics when no recipes exist."""
        service.repository.get_all.return_value = []

        stats = service.get_statistics()

        assert stats.total_recipes == 0
        assert stats.by_category == {}
        assert stats.by_difficulty == {}

    def test_get_available_flavors(self, service, mock_repository):
        """Test getting available flavors."""
        flavors = service.get_available_flavors()

        assert len(flavors) == 3
        assert "Chocolate" in flavors
        mock_repository.get_unique_flavors.assert_called_once()

    def test_get_available_categories(self, service, mock_repository):
        """Test getting available categories."""
        categories = service.get_available_categories()

        assert len(categories) == 2
        assert "Hiện đại" in categories
        mock_repository.get_unique_categories.assert_called_once()

    def test_get_trending_recipes(self, service):
        """Test getting trending recipes."""
        recipes = service.get_trending_recipes(limit=5)

        assert len(recipes) <= 5
        # Verify search was called with market_trend filter
        call_args = service.repository.search.call_args
        assert call_args[0][0].market_trend == "Cao"

    def test_get_highly_rated_recipes(self, service):
        """Test getting highly rated recipes."""
        # Mock repository to return sorted recipes
        service.repository.search.return_value = [
            Recipe(
                recipe_id="high_001",
                recipe_name="High Rating",
                category=Category.MODERN,
                flavor_profile="Test",
                difficulty_level=DifficultyLevel.EASY,
                customer_feedback_score=4.8
            ),
            Recipe(
                recipe_id="medium_002",
                recipe_name="Medium Rating",
                category=Category.MODERN,
                flavor_profile="Test",
                difficulty_level=DifficultyLevel.EASY,
                customer_feedback_score=4.2
            ),
        ]

        recipes = service.get_highly_rated_recipes(min_score=4.0, limit=5)

        assert len(recipes) <= 5
        # Verify recipes are sorted by score
        if len(recipes) >= 2:
            assert recipes[0].customer_feedback_score >= recipes[1].customer_feedback_score
