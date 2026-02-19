"""
Formatting utilities.
DRY Principle: Reusable formatting functions.
KISS Principle: Simple, focused formatting functions.
"""
from typing import Dict, Any
from ..models import Recipe


def format_time(minutes: float) -> str:
    """
    Format time in minutes to human-readable format.
    DRY: Reusable across the application.
    """
    if minutes < 60:
        return f"{int(minutes)} phút"
    
    hours = int(minutes // 60)
    remaining_minutes = int(minutes % 60)
    
    if remaining_minutes == 0:
        return f"{hours} giờ"
    
    return f"{hours} giờ {remaining_minutes} phút"


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Format percentage value.
    DRY: Reusable percentage formatting.
    """
    return f"{value:.{decimals}f}%"


def format_recipe_summary(recipe: Recipe) -> str:
    """
    Format recipe as a summary string.
    KISS: Simple, readable output.
    """
    lines = [
        f"ID: {recipe.recipe_id}",
        f"Tên: {recipe.name}",
        f"Mô tả: {recipe.description}",
        f"Danh mục: {recipe.category}",
        f"Hương vị: {recipe.flavor_profile}",
        f"Độ khó: {recipe.difficulty_level}",
    ]
    
    if recipe.total_time_minutes:
        lines.append(f"Thời gian: {format_time(recipe.total_time_minutes)}")
    
    if recipe.servings:
        lines.append(f"Khẩu phần: {recipe.servings}")
    
    if recipe.ingredients:
        lines.append(f"Số nguyên liệu: {len(recipe.ingredients)}")
    
    if recipe.market_trend_relevance:
        lines.append(f"Xu hướng: {recipe.market_trend_relevance}")
    
    return "\n".join(lines)


def format_analysis_report(analysis_data: Dict[str, Any]) -> str:
    """
    Format analysis data as a readable report.
    KISS: Simple report generation.
    """
    lines = [
        "=" * 60,
        "BÁO CÁO PHÂN TÍCH CÔNG THỨC BÁNH",
        "=" * 60,
        "",
        f"Tổng số công thức: {analysis_data.get('total_recipes', 0)}",
        ""
    ]
    
    # Flavor distribution
    if 'flavor_counts' in analysis_data:
        lines.append("PHÂN BỐ HƯƠNG VỊ:")
        for flavor, count in analysis_data['flavor_counts'].items():
            lines.append(f"  - {flavor}: {count} công thức")
        lines.append("")
    
    # Difficulty distribution
    if 'difficulty_counts' in analysis_data:
        lines.append("PHÂN BỐ ĐỘ KHÓ:")
        for difficulty, count in analysis_data['difficulty_counts'].items():
            lines.append(f"  - {difficulty}: {count} công thức")
        lines.append("")
    
    # Time statistics
    if 'time_statistics' in analysis_data:
        stats = analysis_data['time_statistics']
        lines.append("THỐNG KÊ THỜI GIAN:")
        if stats.get('avg_prep_time'):
            lines.append(f"  - Thời gian chuẩn bị TB: {format_time(stats['avg_prep_time'])}")
        if stats.get('avg_cook_time'):
            lines.append(f"  - Thời gian nấu TB: {format_time(stats['avg_cook_time'])}")
        if stats.get('avg_total_time'):
            lines.append(f"  - Tổng thời gian TB: {format_time(stats['avg_total_time'])}")
        lines.append("")
    
    # Top ingredients
    if 'top_ingredients' in analysis_data:
        lines.append("NGUYÊN LIỆU PHỔ BIẾN NHẤT:")
        for ingredient, count in analysis_data['top_ingredients'][:5]:
            lines.append(f"  - {ingredient}: {count} lần")
        lines.append("")
    
    lines.append("=" * 60)
    
    return "\n".join(lines)
