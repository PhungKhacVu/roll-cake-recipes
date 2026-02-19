"""
Recipe analyzer for data analysis and statistics.
Single Responsibility Principle: Handles only analytics and statistics.
DRY Principle: Reusable analysis methods to avoid code duplication.
"""
from typing import List, Dict, Any
from collections import Counter
from ..models import Recipe


class RecipeAnalyzer:
    """
    Analyzer for recipe data statistics and insights.
    Provides reusable analysis methods.
    """
    
    def __init__(self, recipes: List[Recipe]):
        """Initialize analyzer with recipe data."""
        self.recipes = recipes
    
    def count_by_field(self, field_name: str) -> Dict[str, int]:
        """
        Generic method to count recipes by any field.
        DRY: Reusable for different fields.
        """
        values = []
        for recipe in self.recipes:
            value = getattr(recipe, field_name, None)
            if value:
                values.append(value)
        
        return dict(Counter(values))
    
    def count_by_flavor(self) -> Dict[str, int]:
        """Count recipes by flavor profile."""
        return self.count_by_field('flavor_profile')
    
    def count_by_difficulty(self) -> Dict[str, int]:
        """Count recipes by difficulty level."""
        return self.count_by_field('difficulty_level')
    
    def count_by_category(self) -> Dict[str, int]:
        """Count recipes by category."""
        return self.count_by_field('category')
    
    def count_by_trend_relevance(self) -> Dict[str, int]:
        """Count recipes by market trend relevance."""
        return self.count_by_field('market_trend_relevance')
    
    def get_average_time(self, time_field: str = 'total_time_minutes') -> float:
        """
        Get average time for a specific time field.
        DRY: Reusable for different time fields.
        """
        times = [
            getattr(recipe, time_field)
            for recipe in self.recipes
            if getattr(recipe, time_field, None) is not None
        ]
        
        if not times:
            return 0.0
        
        return sum(times) / len(times)
    
    def get_average_prep_time(self) -> float:
        """Get average preparation time."""
        return self.get_average_time('prep_time_minutes')
    
    def get_average_cook_time(self) -> float:
        """Get average cooking time."""
        return self.get_average_time('cook_time_minutes')
    
    def get_average_total_time(self) -> float:
        """Get average total time."""
        return self.get_average_time('total_time_minutes')
    
    def get_time_statistics(self) -> Dict[str, float]:
        """Get comprehensive time statistics."""
        return {
            'avg_prep_time': self.get_average_prep_time(),
            'avg_cook_time': self.get_average_cook_time(),
            'avg_total_time': self.get_average_total_time()
        }
    
    def get_most_common_ingredients(self, top_n: int = 10) -> List[tuple]:
        """
        Get most common ingredients across all recipes.
        Returns list of (ingredient_name, count) tuples.
        """
        ingredient_names = []
        
        for recipe in self.recipes:
            for ingredient in recipe.ingredients:
                ingredient_names.append(ingredient.name)
        
        counter = Counter(ingredient_names)
        return counter.most_common(top_n)
    
    def get_flavor_distribution(self) -> Dict[str, float]:
        """
        Get flavor distribution as percentages.
        """
        flavor_counts = self.count_by_flavor()
        total = sum(flavor_counts.values())
        
        if total == 0:
            return {}
        
        return {
            flavor: (count / total) * 100
            for flavor, count in flavor_counts.items()
        }
    
    def get_difficulty_distribution(self) -> Dict[str, float]:
        """
        Get difficulty distribution as percentages.
        """
        difficulty_counts = self.count_by_difficulty()
        total = sum(difficulty_counts.values())
        
        if total == 0:
            return {}
        
        return {
            difficulty: (count / total) * 100
            for difficulty, count in difficulty_counts.items()
        }
    
    def generate_summary_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive summary report.
        Combines multiple analysis methods.
        """
        return {
            'total_recipes': len(self.recipes),
            'flavor_counts': self.count_by_flavor(),
            'difficulty_counts': self.count_by_difficulty(),
            'category_counts': self.count_by_category(),
            'time_statistics': self.get_time_statistics(),
            'flavor_distribution': self.get_flavor_distribution(),
            'difficulty_distribution': self.get_difficulty_distribution(),
            'top_ingredients': self.get_most_common_ingredients(10)
        }
    
    def filter_by_criteria(self, **criteria) -> List[Recipe]:
        """
        Filter recipes by multiple criteria.
        DRY: Reusable filtering logic.
        """
        filtered = self.recipes
        
        for key, value in criteria.items():
            if value is not None:
                filtered = [
                    recipe for recipe in filtered
                    if getattr(recipe, key, None) == value
                ]
        
        return filtered
