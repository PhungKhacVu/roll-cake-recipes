"""
API layer - HTTP endpoints using FastAPI.

This module provides RESTful API endpoints for accessing recipe data.
"""

from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from src.domain.models import Recipe, RecipeSearchParams, RecipeStatistics
from src.application.services import RecipeService
from src.infrastructure.repositories import CSVRecipeRepository


# Initialize FastAPI app
app = FastAPI(
    title="Roll Cake Recipes API",
    description="API for accessing Vietnamese roll cake recipes database",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["GET"],  # Only allow GET for this read-only API
    allow_headers=["*"],
)

# Initialize repository and service
repository = CSVRecipeRepository()
recipe_service = RecipeService(repository)


@app.get("/", tags=["Root"])
@limiter.limit("100/minute")
async def root():
    """
    Root endpoint with API information.

    Returns:
        Welcome message and API information
    """
    return {
        "message": "Welcome to Roll Cake Recipes API",
        "version": "1.0.0",
        "documentation": "/api/docs",
        "endpoints": {
            "recipes": "/api/v1/recipes",
            "search": "/api/v1/recipes/search",
            "statistics": "/api/v1/stats"
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring.

    Returns:
        Health status
    """
    return {"status": "healthy", "service": "roll-cake-recipes-api"}


@app.get("/api/v1/recipes", response_model=List[Recipe], tags=["Recipes"])
@limiter.limit("100/minute")
async def get_recipes(
    limit: Optional[int] = Query(None, ge=1, le=100, description="Maximum number of recipes to return"),
    offset: int = Query(0, ge=0, description="Number of recipes to skip")
):
    """
    Get all recipes with pagination.

    Args:
        limit: Maximum number of recipes to return (1-100)
        offset: Number of recipes to skip for pagination

    Returns:
        List of Recipe objects

    Example:
        GET /api/v1/recipes?limit=10&offset=0
    """
    recipes = recipe_service.get_all_recipes(limit=limit, offset=offset)
    return recipes


@app.get("/api/v1/recipes/{recipe_id}", response_model=Recipe, tags=["Recipes"])
@limiter.limit("100/minute")
async def get_recipe(
    recipe_id: str = Path(..., description="Unique recipe identifier")
):
    """
    Get a specific recipe by ID.

    Args:
        recipe_id: Unique recipe identifier

    Returns:
        Recipe object

    Raises:
        HTTPException: 404 if recipe not found

    Example:
        GET /api/v1/recipes/japanese_fruit_roll_cake_001
    """
    recipe = recipe_service.get_recipe_by_id(recipe_id)

    if recipe is None:
        raise HTTPException(
            status_code=404,
            detail=f"Recipe with ID '{recipe_id}' not found"
        )

    return recipe


@app.get("/api/v1/recipes/search/filter", response_model=List[Recipe], tags=["Search"])
@limiter.limit("100/minute")
async def search_recipes(
    flavor: Optional[str] = Query(None, description="Filter by flavor profile"),
    category: Optional[str] = Query(None, description="Filter by category"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty level"),
    max_prep_time: Optional[float] = Query(None, ge=0, description="Maximum prep time in minutes"),
    max_total_time: Optional[float] = Query(None, ge=0, description="Maximum total time in minutes"),
    min_feedback_score: Optional[float] = Query(None, ge=0, le=5, description="Minimum feedback score"),
    market_trend: Optional[str] = Query(None, description="Filter by market trend")
):
    """
    Search recipes with multiple filters.

    All filters are optional and can be combined.

    Args:
        flavor: Filter by flavor profile (partial match)
        category: Filter by category (exact match)
        difficulty: Filter by difficulty level
        max_prep_time: Maximum preparation time in minutes
        max_total_time: Maximum total time in minutes
        min_feedback_score: Minimum customer feedback score
        market_trend: Filter by market trend relevance

    Returns:
        List of recipes matching the filters

    Example:
        GET /api/v1/recipes/search/filter?flavor=Chocolate&difficulty=Dễ
    """
    params = RecipeSearchParams(
        flavor=flavor,
        category=category,
        difficulty=difficulty,
        max_prep_time=max_prep_time,
        max_total_time=max_total_time,
        min_feedback_score=min_feedback_score,
        market_trend=market_trend
    )

    recipes = recipe_service.search_recipes(params)
    return recipes


@app.get("/api/v1/recipes/random/one", response_model=Recipe, tags=["Recipes"])
@limiter.limit("100/minute")
async def get_random_recipe():
    """
    Get a random recipe.

    Returns:
        Random Recipe object

    Raises:
        HTTPException: 404 if no recipes available

    Example:
        GET /api/v1/recipes/random/one
    """
    recipe = recipe_service.get_random_recipe()

    if recipe is None:
        raise HTTPException(
            status_code=404,
            detail="No recipes available"
        )

    return recipe


@app.get("/api/v1/flavors", response_model=List[str], tags=["Metadata"])
@limiter.limit("100/minute")
async def get_flavors():
    """
    Get list of all available flavor profiles.

    Returns:
        Sorted list of unique flavor profiles

    Example:
        GET /api/v1/flavors
    """
    return recipe_service.get_available_flavors()


@app.get("/api/v1/categories", response_model=List[str], tags=["Metadata"])
@limiter.limit("100/minute")
async def get_categories():
    """
    Get list of all available categories.

    Returns:
        Sorted list of unique categories

    Example:
        GET /api/v1/categories
    """
    return recipe_service.get_available_categories()


@app.get("/api/v1/stats", response_model=RecipeStatistics, tags=["Statistics"])
@limiter.limit("100/minute")
async def get_statistics():
    """
    Get statistics about the recipe collection.

    Returns:
        RecipeStatistics object with various metrics including:
        - Total number of recipes
        - Distribution by category, difficulty, flavor, market trend
        - Average prep time, cook time, and feedback score

    Example:
        GET /api/v1/stats
    """
    return recipe_service.get_statistics()


@app.get("/api/v1/trending", response_model=List[Recipe], tags=["Curated"])
@limiter.limit("100/minute")
async def get_trending_recipes(
    limit: int = Query(10, ge=1, le=50, description="Number of recipes to return")
):
    """
    Get trending recipes (high market relevance).

    Args:
        limit: Maximum number of recipes to return (1-50)

    Returns:
        List of trending recipes

    Example:
        GET /api/v1/trending?limit=10
    """
    return recipe_service.get_trending_recipes(limit=limit)


@app.get("/api/v1/top-rated", response_model=List[Recipe], tags=["Curated"])
@limiter.limit("100/minute")
async def get_top_rated_recipes(
    min_score: float = Query(4.0, ge=0, le=5, description="Minimum feedback score"),
    limit: int = Query(10, ge=1, le=50, description="Number of recipes to return")
):
    """
    Get highly rated recipes.

    Args:
        min_score: Minimum feedback score (0-5)
        limit: Maximum number of recipes to return (1-50)

    Returns:
        List of highly rated recipes sorted by score

    Example:
        GET /api/v1/top-rated?min_score=4.5&limit=5
    """
    return recipe_service.get_highly_rated_recipes(min_score=min_score, limit=limit)


@app.get("/api/v1/quick-recipes", response_model=List[Recipe], tags=["Curated"])
@limiter.limit("100/minute")
async def get_quick_recipes(
    max_minutes: float = Query(60, ge=0, description="Maximum total time in minutes")
):
    """
    Get quick recipes that can be completed within specified time.

    Args:
        max_minutes: Maximum total time in minutes

    Returns:
        List of quick recipes

    Example:
        GET /api/v1/quick-recipes?max_minutes=45
    """
    return recipe_service.get_quick_recipes(max_minutes=max_minutes)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
