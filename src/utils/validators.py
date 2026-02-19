"""
Validation utilities.
Single Responsibility: Data validation only.
"""
from typing import Dict, List, Any


def validate_recipe_data(data: Dict[str, Any]) -> tuple[bool, List[str]]:
    """
    Validate recipe data.
    Returns (is_valid, error_messages).
    """
    errors = []
    
    # Required fields
    required_fields = ['recipe_id', 'name', 'category', 'flavor_profile', 'difficulty_level']
    for field in required_fields:
        if not data.get(field):
            errors.append(f"Missing required field: {field}")
    
    # Validate difficulty level
    valid_difficulties = ['Dễ', 'Easy', 'Trung bình', 'Medium', 'Khó', 'Hard']
    if data.get('difficulty_level') and data['difficulty_level'] not in valid_difficulties:
        errors.append(f"Invalid difficulty level: {data['difficulty_level']}")
    
    # Validate numeric fields
    numeric_fields = ['prep_time_minutes', 'cook_time_minutes', 'total_time_minutes']
    for field in numeric_fields:
        value = data.get(field)
        if value is not None:
            try:
                float_value = float(value)
                if float_value < 0:
                    errors.append(f"{field} cannot be negative")
            except (ValueError, TypeError):
                errors.append(f"{field} must be a number")
    
    return len(errors) == 0, errors


def validate_ingredient_data(data: Dict[str, Any]) -> tuple[bool, List[str]]:
    """
    Validate ingredient data.
    Returns (is_valid, error_messages).
    """
    errors = []
    
    if not data.get('name'):
        errors.append("Ingredient name is required")
    
    quantity = data.get('quantity')
    if quantity is not None:
        try:
            float_value = float(quantity)
            if float_value < 0:
                errors.append("Quantity cannot be negative")
        except (ValueError, TypeError):
            errors.append("Quantity must be a number")
    
    return len(errors) == 0, errors
