"""
Recipe domain model.
Single Responsibility Principle: Represents a recipe with its properties and behaviors.
"""
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from .ingredient import Ingredient


@dataclass
class Recipe:
    """Represents a roll cake recipe."""
    
    recipe_id: str
    name: str
    description: str
    category: str
    flavor_profile: str
    difficulty_level: str
    prep_time_minutes: Optional[float] = None
    cook_time_minutes: Optional[float] = None
    total_time_minutes: Optional[float] = None
    servings: Optional[str] = None
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    source: Optional[str] = None
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None
    ingredients: List[Ingredient] = field(default_factory=list)
    instructions: List[str] = field(default_factory=list)
    tips_tricks: Optional[str] = None
    storage_instructions: Optional[str] = None
    customer_feedback_score: Optional[float] = None
    market_trend_relevance: Optional[str] = None
    
    def __post_init__(self):
        """Validate and process recipe data after initialization."""
        if self.prep_time_minutes and self.cook_time_minutes and not self.total_time_minutes:
            self.total_time_minutes = self.prep_time_minutes + self.cook_time_minutes
    
    def get_total_time(self) -> float:
        """Get total time in minutes."""
        return self.total_time_minutes or 0
    
    def is_easy(self) -> bool:
        """Check if recipe is easy difficulty."""
        return self.difficulty_level.lower() in ['dễ', 'easy']
    
    def is_trending(self) -> bool:
        """Check if recipe is highly relevant to market trends."""
        return self.market_trend_relevance and self.market_trend_relevance.lower() in ['cao', 'high']
    
    def to_dict(self) -> dict:
        """Convert recipe to dictionary."""
        return {
            'recipe_id': self.recipe_id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'flavor_profile': self.flavor_profile,
            'difficulty_level': self.difficulty_level,
            'prep_time_minutes': self.prep_time_minutes,
            'cook_time_minutes': self.cook_time_minutes,
            'total_time_minutes': self.total_time_minutes,
            'servings': self.servings,
            'image_url': self.image_url,
            'video_url': self.video_url,
            'source': self.source,
            'date_created': self.date_created.isoformat() if self.date_created else None,
            'date_updated': self.date_updated.isoformat() if self.date_updated else None,
            'ingredients': [ing.to_dict() for ing in self.ingredients],
            'instructions': self.instructions,
            'tips_tricks': self.tips_tricks,
            'storage_instructions': self.storage_instructions,
            'customer_feedback_score': self.customer_feedback_score,
            'market_trend_relevance': self.market_trend_relevance
        }
    
    def __str__(self) -> str:
        """String representation of recipe."""
        return f"{self.name} ({self.flavor_profile}, {self.difficulty_level})"
