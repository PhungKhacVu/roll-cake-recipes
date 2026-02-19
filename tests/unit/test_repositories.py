"""
Unit tests for repository layer.

This test suite validates:
- CSV loading and parsing
- Data validation
- Caching behavior
- Error handling
"""

import pytest
import tempfile
import os
from pathlib import Path

from src.infrastructure.repositories import CSVRecipeRepository
from src.domain.models import Recipe, RecipeSearchParams, DifficultyLevel


class TestCSVRecipeRepository:
    """Test suite for CSVRecipeRepository."""

    @pytest.fixture
    def sample_csv_path(self, tmp_path):
        """Create a temporary CSV file with sample data for testing."""
        csv_file = tmp_path / "test_recipes.csv"
        csv_content = """Recipe_ID,Recipe_Name,Description,Category,Flavor_Profile,Difficulty_Level,Prep_Time_Minutes,Cook_Time_Minutes,Total_Time_Minutes,Servings,Image_URL,Video_URL,Source,Date_Created,Date_Updated,Tips_Tricks,Storage_Instructions,Customer_Feedback_Score,Market_Trend_Relevance,Ingredients_Flattened,Instructions_Flattened
chocolate_roll_001,Chocolate Roll,Delicious chocolate roll,Hiện đại,Chocolate,Dễ,20,15,35,8,http://example.com/image.jpg,,Test Source,,,Tip 1,Store cold,4.5,Cao,Flour: 200g; Sugar: 100g,"1. Mix ingredients
2. Bake"
matcha_roll_002,Matcha Roll,Green tea flavor,Truyền thống,Trà xanh,Trung bình,30,20,50,6,http://example.com/image2.jpg,,Test Source 2,,,Tip 2,Store cold,4.0,Trung bình,Flour: 200g; Matcha: 20g,"1. Mix
2. Bake"
"""
        csv_file.write_text(csv_content, encoding='utf-8')
        return str(csv_file)

    @pytest.fixture
    def empty_csv_path(self, tmp_path):
        """Create an empty CSV file for testing."""
        csv_file = tmp_path / "empty.csv"
        csv_file.write_text("", encoding='utf-8')
        return str(csv_file)

    @pytest.fixture
    def malformed_csv_path(self, tmp_path):
        """Create a CSV file with malformed data."""
        csv_file = tmp_path / "malformed.csv"
        csv_content = """Recipe_ID,Recipe_Name,Category,Flavor_Profile,Difficulty_Level
invalid_id!,Test,Hiện đại,Test,Dễ
test_002,Test 2,Hiện đại,Test,Dễ
"""
        csv_file.write_text(csv_content, encoding='utf-8')
        return str(csv_file)

    def test_repository_initialization(self, sample_csv_path):
        """Test that repository initializes correctly."""
        repo = CSVRecipeRepository(sample_csv_path)
        assert repo.csv_path == sample_csv_path
        assert not repo._recipes_loaded

    def test_repository_initialization_with_nonexistent_file(self):
        """Test that repository raises error for nonexistent file."""
        with pytest.raises(FileNotFoundError):
            CSVRecipeRepository("/nonexistent/path/to/file.csv")

    def test_get_all_recipes(self, sample_csv_path):
        """Test loading all recipes from CSV."""
        repo = CSVRecipeRepository(sample_csv_path)
        recipes = repo.get_all()

        assert len(recipes) == 2
        assert all(isinstance(r, Recipe) for r in recipes)
        assert recipes[0].recipe_id == "chocolate_roll_001"
        assert recipes[1].recipe_id == "matcha_roll_002"

    def test_get_recipe_by_id(self, sample_csv_path):
        """Test retrieving recipe by ID."""
        repo = CSVRecipeRepository(sample_csv_path)

        recipe = repo.get_by_id("chocolate_roll_001")
        assert recipe is not None
        assert recipe.recipe_name == "Chocolate Roll"
        assert recipe.flavor_profile == "Chocolate"

    def test_get_nonexistent_recipe_by_id(self, sample_csv_path):
        """Test that get_by_id returns None for nonexistent recipe."""
        repo = CSVRecipeRepository(sample_csv_path)

        recipe = repo.get_by_id("nonexistent_999")
        assert recipe is None

    def test_search_by_flavor(self, sample_csv_path):
        """Test searching recipes by flavor."""
        repo = CSVRecipeRepository(sample_csv_path)
        params = RecipeSearchParams(flavor="Chocolate")

        results = repo.search(params)
        assert len(results) == 1
        assert results[0].flavor_profile == "Chocolate"

    def test_search_by_difficulty(self, sample_csv_path):
        """Test searching recipes by difficulty."""
        repo = CSVRecipeRepository(sample_csv_path)
        params = RecipeSearchParams(difficulty=DifficultyLevel.EASY)

        results = repo.search(params)
        assert len(results) == 1
        assert results[0].difficulty_level == "Dễ"

    def test_search_by_max_prep_time(self, sample_csv_path):
        """Test searching recipes by max prep time."""
        repo = CSVRecipeRepository(sample_csv_path)
        params = RecipeSearchParams(max_prep_time=25)

        results = repo.search(params)
        assert len(results) == 1
        assert results[0].prep_time_minutes <= 25

    def test_search_with_multiple_filters(self, sample_csv_path):
        """Test searching with multiple filters."""
        repo = CSVRecipeRepository(sample_csv_path)
        params = RecipeSearchParams(
            flavor="Chocolate",
            difficulty=DifficultyLevel.EASY,
            max_prep_time=30
        )

        results = repo.search(params)
        assert len(results) == 1
        assert results[0].recipe_id == "chocolate_roll_001"

    def test_search_with_min_feedback_score(self, sample_csv_path):
        """Test searching by minimum feedback score."""
        repo = CSVRecipeRepository(sample_csv_path)
        params = RecipeSearchParams(min_feedback_score=4.5)

        results = repo.search(params)
        assert len(results) == 1
        assert results[0].customer_feedback_score >= 4.5

    def test_get_unique_flavors(self, sample_csv_path):
        """Test getting list of unique flavors."""
        repo = CSVRecipeRepository(sample_csv_path)
        flavors = repo.get_unique_flavors()

        assert len(flavors) == 2
        assert "Chocolate" in flavors
        assert "Trà xanh" in flavors
        assert flavors == sorted(flavors)  # Should be sorted

    def test_get_unique_categories(self, sample_csv_path):
        """Test getting list of unique categories."""
        repo = CSVRecipeRepository(sample_csv_path)
        categories = repo.get_unique_categories()

        assert len(categories) == 2
        assert "Hiện đại" in categories
        assert "Truyền thống" in categories

    def test_caching_behavior(self, sample_csv_path):
        """Test that caching works correctly."""
        repo = CSVRecipeRepository(sample_csv_path)

        # First call should load data
        recipes1 = repo.get_all()
        assert repo._recipes_loaded

        # Second call should use cache (same object reference)
        recipes2 = repo.get_all()
        assert recipes1 is recipes2  # Should be same object from cache

    def test_cache_clearing(self, sample_csv_path):
        """Test that cache can be cleared."""
        repo = CSVRecipeRepository(sample_csv_path)

        # Load data
        repo.get_all()
        assert repo._recipes_loaded

        # Clear cache
        repo.clear_cache()
        assert not repo._recipes_loaded

        # Data should be reloaded on next access
        recipes = repo.get_all()
        assert len(recipes) == 2

    def test_empty_csv_file(self, tmp_path):
        """Test handling of CSV with only headers."""
        csv_file = tmp_path / "headers_only.csv"
        csv_file.write_text(
            "Recipe_ID,Recipe_Name,Category,Flavor_Profile,Difficulty_Level\n",
            encoding='utf-8'
        )

        repo = CSVRecipeRepository(str(csv_file))
        recipes = repo.get_all()
        assert recipes == []

    def test_malformed_row_handling(self, malformed_csv_path):
        """Test that malformed rows are skipped gracefully."""
        repo = CSVRecipeRepository(malformed_csv_path)

        # Should skip the malformed row and load only valid ones
        recipes = repo.get_all()

        # Only the valid recipe should be loaded
        assert len(recipes) == 1
        assert recipes[0].recipe_id == "test_002"

    def test_duplicate_recipe_ids(self, tmp_path):
        """Test handling of duplicate recipe IDs."""
        csv_file = tmp_path / "duplicates.csv"
        csv_content = """Recipe_ID,Recipe_Name,Category,Flavor_Profile,Difficulty_Level
test_001,Recipe 1,Hiện đại,Test,Dễ
test_001,Recipe 2,Hiện đại,Test,Dễ
"""
        csv_file.write_text(csv_content, encoding='utf-8')

        repo = CSVRecipeRepository(str(csv_file))

        # Should raise ValueError for duplicate IDs
        with pytest.raises(ValueError, match="Duplicate recipe ID"):
            repo.get_all()

    def test_unicode_handling(self, tmp_path):
        """Test that Vietnamese unicode characters are handled correctly."""
        csv_file = tmp_path / "unicode.csv"
        csv_content = """Recipe_ID,Recipe_Name,Description,Category,Flavor_Profile,Difficulty_Level
test_001,Bánh bông lan cuộn,Mô tả tiếng Việt,Hiện đại,Chocolate,Dễ
"""
        csv_file.write_text(csv_content, encoding='utf-8')

        repo = CSVRecipeRepository(str(csv_file))
        recipes = repo.get_all()

        assert len(recipes) == 1
        assert recipes[0].recipe_name == "Bánh bông lan cuộn"
        assert recipes[0].description == "Mô tả tiếng Việt"

    def test_optional_fields_handling(self, tmp_path):
        """Test that optional fields can be empty."""
        csv_file = tmp_path / "optional.csv"
        csv_content = """Recipe_ID,Recipe_Name,Category,Flavor_Profile,Difficulty_Level,Prep_Time_Minutes,Image_URL
test_001,Test Recipe,Hiện đại,Test,Dễ,,
"""
        csv_file.write_text(csv_content, encoding='utf-8')

        repo = CSVRecipeRepository(str(csv_file))
        recipes = repo.get_all()

        assert len(recipes) == 1
        assert recipes[0].prep_time_minutes is None
        assert recipes[0].image_url is None
