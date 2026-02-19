"""
Recipe service for business logic operations.
Single Responsibility Principle: Handles recipe-related business logic.
Dependency Inversion Principle: Depends on IRepository abstraction.
"""
from typing import List, Optional, Dict, Any
from ..models import Recipe
from ..repositories import IRepository


class RecipeService:
    """
    Service for managing recipe business logic.
    Depends on IRepository interface, not concrete implementation.
    """
    
    def __init__(self, repository: IRepository):
        """Initialize service with a repository."""
        self.repository = repository
    
    def get_all_recipes(self) -> List[Recipe]:
        """Get all recipes."""
        return self.repository.get_all()
    
    def get_recipe_by_id(self, recipe_id: str) -> Optional[Recipe]:
        """Get a specific recipe by ID."""
        return self.repository.get_by_id(recipe_id)
    
    def search_recipes(
        self,
        flavor: Optional[str] = None,
        difficulty: Optional[str] = None,
        category: Optional[str] = None,
        max_time: Optional[float] = None
    ) -> List[Recipe]:
        """
        Search recipes by various criteria.
        Business logic: combine multiple filters.
        """
        criteria = {}
        
        if flavor:
            criteria['flavor_profile'] = flavor
        if difficulty:
            criteria['difficulty_level'] = difficulty
        if category:
            criteria['category'] = category
        
        recipes = self.repository.filter(criteria)
        
        # Additional filtering by time (not handled in repository)
        if max_time is not None:
            recipes = [r for r in recipes if r.get_total_time() <= max_time]
        
        return recipes
    
    def get_easy_recipes(self) -> List[Recipe]:
        """Get all easy recipes."""
        return [r for r in self.get_all_recipes() if r.is_easy()]
    
    def get_trending_recipes(self) -> List[Recipe]:
        """Get recipes that are trending in the market."""
        return [r for r in self.get_all_recipes() if r.is_trending()]
    
    def get_recipes_by_flavor(self, flavor: str) -> List[Recipe]:
        """Get recipes by flavor profile."""
        return self.repository.filter({'flavor_profile': flavor})
    
    def get_quick_recipes(self, max_minutes: float = 60) -> List[Recipe]:
        """Get recipes that can be made quickly."""
        return [
            r for r in self.get_all_recipes()
            if r.get_total_time() <= max_minutes
        ]
    
    def get_recipe_count(self) -> int:
        """Get total number of recipes."""
        return self.repository.count()
    
    def get_unique_flavors(self) -> List[str]:
        """Get list of unique flavor profiles."""
        recipes = self.get_all_recipes()
        flavors = set(r.flavor_profile for r in recipes if r.flavor_profile)
        return sorted(flavors)
    
    def get_unique_categories(self) -> List[str]:
        """Get list of unique categories."""
        recipes = self.get_all_recipes()
        categories = set(r.category for r in recipes if r.category)
        return sorted(categories)
    
    def get_recipes_summary(self) -> Dict[str, Any]:
        """Get a summary of all recipes."""
        recipes = self.get_all_recipes()
        
        return {
            'total_recipes': len(recipes),
            'unique_flavors': len(self.get_unique_flavors()),
            'unique_categories': len(self.get_unique_categories()),
            'easy_recipes': len(self.get_easy_recipes()),
            'trending_recipes': len(self.get_trending_recipes())
        }
