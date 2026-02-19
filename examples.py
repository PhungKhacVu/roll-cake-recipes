#!/usr/bin/env python3
"""
Example usage of the Roll Cake Recipes system.
Demonstrates how to use the modular architecture.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.repositories import CSVRecipeRepository
from src.services import RecipeService
from src.analytics import RecipeAnalyzer
from src.config import Config
from src.utils import format_recipe_summary, format_analysis_report


def example_basic_usage():
    """Example: Basic usage of the system."""
    print("=" * 60)
    print("EXAMPLE 1: Basic Usage")
    print("=" * 60)
    
    # Step 1: Create repository (Data Access Layer)
    repository = CSVRecipeRepository(str(Config.DEFAULT_CSV_FILE))
    
    # Step 2: Create service (Business Logic Layer)
    service = RecipeService(repository)
    
    # Step 3: Get data
    recipes = service.get_all_recipes()
    print(f"\nTotal recipes: {len(recipes)}")
    
    # Show first recipe
    if recipes:
        print("\nFirst recipe:")
        print(format_recipe_summary(recipes[0]))


def example_search_and_filter():
    """Example: Search and filter recipes."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Search and Filter")
    print("=" * 60)
    
    repository = CSVRecipeRepository(str(Config.DEFAULT_CSV_FILE))
    service = RecipeService(repository)
    
    # Search by flavor
    chocolate_recipes = service.get_recipes_by_flavor("Chocolate")
    print(f"\nChocolate recipes: {len(chocolate_recipes)}")
    
    # Get easy recipes
    easy_recipes = service.get_easy_recipes()
    print(f"Easy recipes: {len(easy_recipes)}")
    
    # Get trending recipes
    trending = service.get_trending_recipes()
    print(f"Trending recipes: {len(trending)}")
    
    # Search with multiple criteria
    results = service.search_recipes(
        flavor="Trái cây",
        difficulty="Trung bình"
    )
    print(f"\nFruit recipes with medium difficulty: {len(results)}")


def example_analytics():
    """Example: Use analytics module."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Analytics")
    print("=" * 60)
    
    repository = CSVRecipeRepository(str(Config.DEFAULT_CSV_FILE))
    service = RecipeService(repository)
    recipes = service.get_all_recipes()
    
    # Create analyzer
    analyzer = RecipeAnalyzer(recipes)
    
    # Get statistics
    print("\nFlavor distribution:")
    flavor_counts = analyzer.count_by_flavor()
    for flavor, count in list(flavor_counts.items())[:5]:
        print(f"  {flavor}: {count}")
    
    print("\nDifficulty distribution:")
    diff_counts = analyzer.count_by_difficulty()
    for difficulty, count in diff_counts.items():
        print(f"  {difficulty}: {count}")
    
    print("\nTime statistics:")
    time_stats = analyzer.get_time_statistics()
    print(f"  Average prep time: {time_stats['avg_prep_time']:.1f} minutes")
    print(f"  Average cook time: {time_stats['avg_cook_time']:.1f} minutes")
    print(f"  Average total time: {time_stats['avg_total_time']:.1f} minutes")
    
    print("\nTop 5 ingredients:")
    top_ingredients = analyzer.get_most_common_ingredients(5)
    for ingredient, count in top_ingredients:
        print(f"  {ingredient}: {count}")


def example_generate_report():
    """Example: Generate comprehensive report."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Generate Report")
    print("=" * 60)
    
    repository = CSVRecipeRepository(str(Config.DEFAULT_CSV_FILE))
    service = RecipeService(repository)
    recipes = service.get_all_recipes()
    
    analyzer = RecipeAnalyzer(recipes)
    
    # Generate and display report
    report_data = analyzer.generate_summary_report()
    report = format_analysis_report(report_data)
    print("\n" + report)


def example_extensibility():
    """Example: Demonstrate extensibility (Open/Closed Principle)."""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Extensibility")
    print("=" * 60)
    
    # The architecture is extensible:
    # 1. Can easily add new repository implementations (e.g., DatabaseRepository)
    # 2. Can add new services without modifying existing ones
    # 3. Can add new analyzers or analysis methods
    
    print("\nArchitecture benefits:")
    print("  ✓ Easy to add new data sources (JSON, Database, API)")
    print("  ✓ Business logic separated from data access")
    print("  ✓ Reusable analytics components")
    print("  ✓ Simple to test each component independently")
    print("  ✓ Follows SOLID principles")


def main():
    """Run all examples."""
    try:
        example_basic_usage()
        example_search_and_filter()
        example_analytics()
        example_generate_report()
        example_extensibility()
        
        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
        
    except FileNotFoundError:
        print(f"\nError: CSV file not found at {Config.DEFAULT_CSV_FILE}")
        print("Please ensure the data file exists.")
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
