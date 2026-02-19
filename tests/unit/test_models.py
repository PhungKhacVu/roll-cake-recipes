"""
Unit tests for domain models.

This test suite validates:
- Data validation rules
- Security measures (CSV injection prevention)
- Business logic in models
"""

import pytest
from pydantic import ValidationError

from src.domain.models import (
    Recipe,
    Ingredient,
    DifficultyLevel,
    Category,
    MarketTrend,
    RecipeSearchParams,
)


class TestIngredientModel:
    """Test suite for Ingredient model."""

    def test_valid_ingredient(self):
        """Test creating a valid ingredient."""
        ingredient = Ingredient(
            name="Bột mì",
            quantity="200",
            unit="gram",
            notes="Bột mì đa dụng"
        )
        assert ingredient.name == "Bột mì"
        assert ingredient.quantity == "200"
        assert ingredient.unit == "gram"

    def test_ingredient_with_minimal_fields(self):
        """Test ingredient with only required fields."""
        ingredient = Ingredient(name="Đường")
        assert ingredient.name == "Đường"
        assert ingredient.quantity is None
        assert ingredient.unit is None

    def test_csv_injection_prevention(self):
        """Test that CSV injection attempts are blocked."""
        dangerous_inputs = ['=cmd', '+cmd', '-cmd', '@cmd', '\tcmd', '\rcmd']

        for dangerous_input in dangerous_inputs:
            with pytest.raises(ValidationError) as exc_info:
                Ingredient(name=dangerous_input)
            assert "CSV injection" in str(exc_info.value).lower() or "Invalid character" in str(exc_info.value)

    def test_whitespace_trimming(self):
        """Test that whitespace is trimmed from ingredient name."""
        ingredient = Ingredient(name="  Bột mì  ")
        assert ingredient.name == "Bột mì"


class TestRecipeModel:
    """Test suite for Recipe model."""

    def test_valid_recipe_creation(self):
        """Test creating a valid recipe with all required fields."""
        recipe = Recipe(
            recipe_id="test_chocolate_001",
            recipe_name="Chocolate Roll Cake",
            category=Category.MODERN,
            flavor_profile="Chocolate",
            difficulty_level=DifficultyLevel.MEDIUM,
            prep_time_minutes=30,
            cook_time_minutes=15,
            servings="8"
        )

        assert recipe.recipe_id == "test_chocolate_001"
        assert recipe.recipe_name == "Chocolate Roll Cake"
        assert recipe.category == "Hiện đại"
        assert recipe.difficulty_level == "Trung bình"

    def test_invalid_recipe_id_with_spaces(self):
        """Test that recipe IDs with spaces are rejected."""
        with pytest.raises(ValidationError) as exc_info:
            Recipe(
                recipe_id="invalid id with spaces",
                recipe_name="Test",
                category=Category.MODERN,
                flavor_profile="Test",
                difficulty_level=DifficultyLevel.EASY
            )
        assert "recipe_id" in str(exc_info.value).lower()

    def test_invalid_recipe_id_with_uppercase(self):
        """Test that recipe IDs with uppercase are rejected."""
        with pytest.raises(ValidationError) as exc_info:
            Recipe(
                recipe_id="InvalidID",
                recipe_name="Test",
                category=Category.MODERN,
                flavor_profile="Test",
                difficulty_level=DifficultyLevel.EASY
            )
        assert "recipe_id" in str(exc_info.value).lower()

    def test_negative_prep_time(self):
        """Test that negative prep time is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            Recipe(
                recipe_id="test_001",
                recipe_name="Test",
                category=Category.MODERN,
                flavor_profile="Test",
                difficulty_level=DifficultyLevel.EASY,
                prep_time_minutes=-10
            )
        assert "prep_time" in str(exc_info.value).lower()

    def test_excessive_prep_time(self):
        """Test that excessively long prep time is rejected."""
        with pytest.raises(ValidationError) as exc_info:
            Recipe(
                recipe_id="test_001",
                recipe_name="Test",
                category=Category.MODERN,
                flavor_profile="Test",
                difficulty_level=DifficultyLevel.EASY,
                prep_time_minutes=2000  # More than 24 hours
            )
        assert "prep_time" in str(exc_info.value).lower()

    def test_csv_injection_in_recipe_name(self):
        """Test that CSV injection in recipe name is blocked."""
        with pytest.raises(ValidationError) as exc_info:
            Recipe(
                recipe_id="test_001",
                recipe_name="=cmd|'/c calc'!A0",
                category=Category.MODERN,
                flavor_profile="Test",
                difficulty_level=DifficultyLevel.EASY
            )
        assert "Invalid character" in str(exc_info.value) or "CSV injection" in str(exc_info.value).lower()

    def test_csv_injection_in_description(self):
        """Test that CSV injection in description is blocked."""
        with pytest.raises(ValidationError) as exc_info:
            Recipe(
                recipe_id="test_001",
                recipe_name="Test",
                description="+dangerous_formula",
                category=Category.MODERN,
                flavor_profile="Test",
                difficulty_level=DifficultyLevel.EASY
            )
        assert "Invalid character" in str(exc_info.value)

    def test_invalid_url(self):
        """Test that invalid URLs are rejected."""
        with pytest.raises(ValidationError) as exc_info:
            Recipe(
                recipe_id="test_001",
                recipe_name="Test",
                category=Category.MODERN,
                flavor_profile="Test",
                difficulty_level=DifficultyLevel.EASY,
                image_url="not_a_valid_url"
            )
        assert "url" in str(exc_info.value).lower()

    def test_valid_http_url(self):
        """Test that valid HTTP URLs are accepted."""
        recipe = Recipe(
            recipe_id="test_001",
            recipe_name="Test",
            category=Category.MODERN,
            flavor_profile="Test",
            difficulty_level=DifficultyLevel.EASY,
            image_url="http://example.com/image.jpg"
        )
        assert recipe.image_url == "http://example.com/image.jpg"

    def test_valid_https_url(self):
        """Test that valid HTTPS URLs are accepted."""
        recipe = Recipe(
            recipe_id="test_001",
            recipe_name="Test",
            category=Category.MODERN,
            flavor_profile="Test",
            difficulty_level=DifficultyLevel.EASY,
            video_url="https://youtube.com/watch?v=123"
        )
        assert recipe.video_url == "https://youtube.com/watch?v=123"

    def test_calculated_total_time(self):
        """Test that total time is calculated correctly."""
        recipe = Recipe(
            recipe_id="test_001",
            recipe_name="Test",
            category=Category.MODERN,
            flavor_profile="Test",
            difficulty_level=DifficultyLevel.EASY,
            prep_time_minutes=20,
            cook_time_minutes=30
        )
        assert recipe.calculated_total_time == 50

    def test_calculated_total_time_with_missing_data(self):
        """Test total time calculation when data is missing."""
        recipe = Recipe(
            recipe_id="test_001",
            recipe_name="Test",
            category=Category.MODERN,
            flavor_profile="Test",
            difficulty_level=DifficultyLevel.EASY,
            prep_time_minutes=20
            # cook_time_minutes is missing
        )
        assert recipe.calculated_total_time is None

    def test_customer_feedback_score_range(self):
        """Test that feedback score must be between 0 and 5."""
        # Valid score
        recipe = Recipe(
            recipe_id="test_001",
            recipe_name="Test",
            category=Category.MODERN,
            flavor_profile="Test",
            difficulty_level=DifficultyLevel.EASY,
            customer_feedback_score=4.5
        )
        assert recipe.customer_feedback_score == 4.5

        # Invalid score (too high)
        with pytest.raises(ValidationError):
            Recipe(
                recipe_id="test_001",
                recipe_name="Test",
                category=Category.MODERN,
                flavor_profile="Test",
                difficulty_level=DifficultyLevel.EASY,
                customer_feedback_score=6.0
            )

        # Invalid score (negative)
        with pytest.raises(ValidationError):
            Recipe(
                recipe_id="test_001",
                recipe_name="Test",
                category=Category.MODERN,
                flavor_profile="Test",
                difficulty_level=DifficultyLevel.EASY,
                customer_feedback_score=-1.0
            )

    def test_parse_ingredients(self):
        """Test parsing of flattened ingredients string."""
        recipe = Recipe(
            recipe_id="test_001",
            recipe_name="Test",
            category=Category.MODERN,
            flavor_profile="Test",
            difficulty_level=DifficultyLevel.EASY,
            ingredients_flattened="Bột mì: 200gram (None); Đường: 100gram (None)"
        )

        ingredients = recipe.parse_ingredients()
        assert len(ingredients) == 2
        assert ingredients[0].name == "Bột mì"
        assert ingredients[1].name == "Đường"

    def test_parse_instructions(self):
        """Test parsing of flattened instructions string."""
        recipe = Recipe(
            recipe_id="test_001",
            recipe_name="Test",
            category=Category.MODERN,
            flavor_profile="Test",
            difficulty_level=DifficultyLevel.EASY,
            instructions_flattened="1. First step\n2. Second step\n3. Third step"
        )

        instructions = recipe.parse_instructions()
        assert len(instructions) == 3
        assert "First step" in instructions[0]
        assert "Second step" in instructions[1]


class TestRecipeSearchParams:
    """Test suite for RecipeSearchParams model."""

    def test_valid_search_params(self):
        """Test creating valid search parameters."""
        params = RecipeSearchParams(
            flavor="Chocolate",
            difficulty=DifficultyLevel.EASY,
            max_prep_time=30
        )
        assert params.flavor == "Chocolate"
        assert params.difficulty == "Dễ"
        assert params.max_prep_time == 30

    def test_empty_search_params(self):
        """Test that empty search params are valid."""
        params = RecipeSearchParams()
        assert params.flavor is None
        assert params.category is None
        assert params.difficulty is None

    def test_invalid_max_prep_time(self):
        """Test that negative max prep time is rejected."""
        with pytest.raises(ValidationError):
            RecipeSearchParams(max_prep_time=-10)

    def test_invalid_feedback_score(self):
        """Test that invalid feedback scores are rejected."""
        with pytest.raises(ValidationError):
            RecipeSearchParams(min_feedback_score=6.0)


class TestEnumerations:
    """Test suite for enum classes."""

    def test_difficulty_levels(self):
        """Test DifficultyLevel enum."""
        assert DifficultyLevel.EASY.value == "Dễ"
        assert DifficultyLevel.MEDIUM.value == "Trung bình"
        assert DifficultyLevel.HARD.value == "Khó"

    def test_categories(self):
        """Test Category enum."""
        assert Category.MODERN.value == "Hiện đại"
        assert Category.TRADITIONAL.value == "Truyền thống"

    def test_market_trends(self):
        """Test MarketTrend enum."""
        assert MarketTrend.HIGH.value == "Cao"
        assert MarketTrend.MEDIUM.value == "Trung bình"
        assert MarketTrend.LOW.value == "Thấp"
