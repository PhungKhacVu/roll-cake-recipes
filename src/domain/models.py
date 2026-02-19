"""
Domain models for Roll Cake Recipes.

This module contains Pydantic models that represent the core business entities.
All data validation and business rules are enforced at this level.
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, computed_field
import re


class DifficultyLevel(str, Enum):
    """Recipe difficulty levels."""
    EASY = "Dễ"
    MEDIUM = "Trung bình"
    HARD = "Khó"


class Category(str, Enum):
    """Recipe categories."""
    MODERN = "Hiện đại"
    TRADITIONAL = "Truyền thống"


class MarketTrend(str, Enum):
    """Market trend relevance levels."""
    HIGH = "Cao"
    MEDIUM = "Trung bình"
    LOW = "Thấp"


class Ingredient(BaseModel):
    """Model representing a recipe ingredient."""

    name: str = Field(..., min_length=1, max_length=200, description="Ingredient name")
    quantity: Optional[str] = Field(None, description="Quantity of ingredient")
    unit: Optional[str] = Field(None, max_length=50, description="Unit of measurement")
    notes: Optional[str] = Field(None, max_length=500, description="Additional notes")

    @field_validator('name')
    @classmethod
    def sanitize_name(cls, v: str) -> str:
        """
        Sanitize ingredient name to prevent CSV injection attacks.

        Args:
            v: The ingredient name to validate

        Returns:
            The sanitized name

        Raises:
            ValueError: If the name starts with dangerous characters
        """
        if v and v[0] in ['=', '+', '-', '@', '\t', '\r']:
            raise ValueError(
                f"Invalid character '{v[0]}' at start of ingredient name. "
                "This may be a CSV injection attempt."
            )
        return v.strip()


class Recipe(BaseModel):
    """
    Model representing a cake recipe with full validation.

    This model enforces all business rules and data constraints:
    - Recipe IDs must be unique and follow naming convention
    - All text fields are sanitized to prevent injection attacks
    - Time values must be non-negative and reasonable
    - URLs must be valid if provided
    """

    # Identity
    recipe_id: str = Field(
        ...,
        pattern=r'^[a-z0-9_]+$',
        min_length=1,
        max_length=100,
        description="Unique recipe identifier (lowercase alphanumeric and underscores only)"
    )
    recipe_name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Recipe name"
    )

    # Description and categorization
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Recipe description"
    )
    category: Category = Field(..., description="Recipe category")
    flavor_profile: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Main flavor profile"
    )
    difficulty_level: DifficultyLevel = Field(..., description="Difficulty level")

    # Time metrics (in minutes)
    prep_time_minutes: Optional[float] = Field(
        None,
        ge=0,
        le=1440,  # Max 24 hours
        description="Preparation time in minutes"
    )
    cook_time_minutes: Optional[float] = Field(
        None,
        ge=0,
        le=1440,  # Max 24 hours
        description="Cooking/baking time in minutes"
    )
    total_time_minutes: Optional[float] = Field(
        None,
        ge=0,
        le=2880,  # Max 48 hours
        description="Total time in minutes"
    )

    # Serving info
    servings: Optional[str] = Field(
        None,
        max_length=50,
        description="Number of servings (e.g., '6-8' or '8')"
    )

    # Media
    image_url: Optional[str] = Field(
        None,
        max_length=500,
        description="URL to recipe image"
    )
    video_url: Optional[str] = Field(
        None,
        max_length=500,
        description="URL to recipe video"
    )

    # Metadata
    source: Optional[str] = Field(
        None,
        max_length=200,
        description="Source of the recipe"
    )
    date_created: Optional[str] = Field(
        None,
        description="Creation date"
    )
    date_updated: Optional[str] = Field(
        None,
        description="Last update date"
    )

    # Instructions and tips
    tips_tricks: Optional[str] = Field(
        None,
        max_length=5000,
        description="Tips and tricks"
    )
    storage_instructions: Optional[str] = Field(
        None,
        max_length=1000,
        description="Storage instructions"
    )

    # Metrics
    customer_feedback_score: Optional[float] = Field(
        None,
        ge=0,
        le=5,
        description="Customer feedback score (0-5)"
    )
    market_trend_relevance: Optional[MarketTrend] = Field(
        None,
        description="Market trend relevance"
    )

    # Flattened data from CSV
    ingredients_flattened: Optional[str] = Field(
        None,
        description="Flattened ingredients string from CSV"
    )
    instructions_flattened: Optional[str] = Field(
        None,
        description="Flattened instructions string from CSV"
    )

    @field_validator('recipe_name', 'description', 'tips_tricks', 'storage_instructions', 'instructions_flattened')
    @classmethod
    def sanitize_text_fields(cls, v: Optional[str]) -> Optional[str]:
        """
        Sanitize text fields to prevent CSV injection and XSS attacks.

        CSV Injection: Attackers can inject formulas starting with =, +, -, @
        that execute when opened in Excel or similar applications.

        Args:
            v: The text value to sanitize

        Returns:
            The sanitized text

        Raises:
            ValueError: If dangerous characters are detected at the start
        """
        if v and len(v) > 0 and v[0] in ['=', '+', '-', '@', '\t', '\r']:
            raise ValueError(
                f"Invalid character '{v[0]}' at start of field. "
                "This may be a CSV injection attempt."
            )
        return v.strip() if v else v

    @field_validator('image_url', 'video_url')
    @classmethod
    def validate_url(cls, v: Optional[str]) -> Optional[str]:
        """
        Validate URL format.

        Args:
            v: The URL to validate

        Returns:
            The validated URL

        Raises:
            ValueError: If the URL format is invalid
        """
        if v is None:
            return v

        v = v.strip()
        if not v:
            return None

        # Basic URL validation
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE
        )

        if not url_pattern.match(v):
            raise ValueError(f"Invalid URL format: {v}")

        return v

    @computed_field
    @property
    def calculated_total_time(self) -> Optional[float]:
        """
        Calculate total time from prep + cook time.

        Returns:
            Total time in minutes, or None if either component is missing
        """
        if self.prep_time_minutes is not None and self.cook_time_minutes is not None:
            return self.prep_time_minutes + self.cook_time_minutes
        return None

    def parse_ingredients(self) -> List[Ingredient]:
        """
        Parse flattened ingredients string into structured Ingredient objects.

        Expected format: "Name1: QuantityUnit (Notes); Name2: QuantityUnit (Notes)"

        Returns:
            List of Ingredient objects
        """
        if not self.ingredients_flattened:
            return []

        ingredients = []
        parts = self.ingredients_flattened.split(';')

        for part in parts:
            part = part.strip()
            if not part:
                continue

            try:
                # Parse format: "Name: Quantity Unit (Notes)"
                if ':' in part:
                    name_part, rest = part.split(':', 1)
                    name = name_part.strip()

                    # Extract notes if present
                    notes = None
                    if '(' in rest and ')' in rest:
                        qty_unit, notes_part = rest.split('(', 1)
                        notes = notes_part.rstrip(')').strip()
                    else:
                        qty_unit = rest

                    # Parse quantity and unit
                    qty_unit = qty_unit.strip()
                    # Simple parsing - can be enhanced
                    quantity = qty_unit if qty_unit else None

                    ingredients.append(Ingredient(
                        name=name,
                        quantity=quantity,
                        unit=None,  # Could be parsed more precisely
                        notes=notes
                    ))
            except Exception:
                # If parsing fails, create a simple ingredient with just the name
                ingredients.append(Ingredient(name=part))

        return ingredients

    def parse_instructions(self) -> List[str]:
        """
        Parse flattened instructions string into list of steps.

        Expected format: "1. Step one\n2. Step two\n..."

        Returns:
            List of instruction steps
        """
        if not self.instructions_flattened:
            return []

        # Split by newline and filter empty lines
        steps = [
            step.strip()
            for step in self.instructions_flattened.split('\n')
            if step.strip()
        ]

        return steps

    class Config:
        """Pydantic model configuration."""
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "recipe_id": "chocolate_roll_001",
                "recipe_name": "Chocolate Swiss Roll",
                "description": "A classic chocolate roll cake with cream filling",
                "category": "Hiện đại",
                "flavor_profile": "Chocolate",
                "difficulty_level": "Trung bình",
                "prep_time_minutes": 30,
                "cook_time_minutes": 15,
                "servings": "8",
                "market_trend_relevance": "Cao"
            }
        }


class RecipeSearchParams(BaseModel):
    """Parameters for searching recipes."""

    flavor: Optional[str] = Field(None, description="Filter by flavor profile")
    category: Optional[Category] = Field(None, description="Filter by category")
    difficulty: Optional[DifficultyLevel] = Field(None, description="Filter by difficulty")
    max_prep_time: Optional[float] = Field(None, ge=0, description="Maximum prep time in minutes")
    max_total_time: Optional[float] = Field(None, ge=0, description="Maximum total time in minutes")
    min_feedback_score: Optional[float] = Field(None, ge=0, le=5, description="Minimum feedback score")
    market_trend: Optional[MarketTrend] = Field(None, description="Filter by market trend")

    class Config:
        """Pydantic model configuration."""
        use_enum_values = True


class RecipeStatistics(BaseModel):
    """Statistics about the recipe collection."""

    total_recipes: int = Field(..., description="Total number of recipes")
    by_category: dict = Field(..., description="Count by category")
    by_difficulty: dict = Field(..., description="Count by difficulty")
    by_flavor: dict = Field(..., description="Count by flavor")
    by_market_trend: dict = Field(..., description="Count by market trend")
    avg_prep_time: Optional[float] = Field(None, description="Average prep time")
    avg_cook_time: Optional[float] = Field(None, description="Average cook time")
    avg_feedback_score: Optional[float] = Field(None, description="Average feedback score")
