#!/usr/bin/env python3
"""
Simple CLI for Roll Cake Recipes Management.
KISS Principle: Keep It Simple, Stupid - straightforward interface.
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


def print_menu():
    """Display main menu."""
    print("\n" + "=" * 60)
    print("HỆ THỐNG QUẢN LÝ CÔNG THỨC BÁNH BÔNG LAN CUỘN")
    print("=" * 60)
    print("1. Xem tất cả công thức")
    print("2. Tìm kiếm công thức theo ID")
    print("3. Lọc công thức theo hương vị")
    print("4. Lọc công thức theo độ khó")
    print("5. Xem công thức dễ làm")
    print("6. Xem công thức đang xu hướng")
    print("7. Xem báo cáo phân tích")
    print("8. Xem tóm tắt hệ thống")
    print("0. Thoát")
    print("=" * 60)


def display_recipes(recipes, title="DANH SÁCH CÔNG THỨC"):
    """Display list of recipes."""
    print(f"\n{title}")
    print("-" * 60)
    
    if not recipes:
        print("Không tìm thấy công thức nào.")
        return
    
    for i, recipe in enumerate(recipes, 1):
        print(f"\n{i}. {recipe.name}")
        print(f"   Hương vị: {recipe.flavor_profile} | Độ khó: {recipe.difficulty_level}")
        if recipe.total_time_minutes:
            print(f"   Thời gian: {recipe.total_time_minutes} phút")
    
    print(f"\nTổng cộng: {len(recipes)} công thức")


def main():
    """
    Main CLI application.
    KISS: Simple command-line interface.
    """
    # Initialize components
    try:
        repository = CSVRecipeRepository(str(Config.DEFAULT_CSV_FILE))
        service = RecipeService(repository)
        
        print("\nĐang tải dữ liệu...")
        recipes = service.get_all_recipes()
        analyzer = RecipeAnalyzer(recipes)
        print(f"Đã tải {len(recipes)} công thức!")
        
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file CSV tại {Config.DEFAULT_CSV_FILE}")
        print("Vui lòng đảm bảo file dữ liệu tồn tại.")
        return
    except Exception as e:
        print(f"Lỗi khi khởi tạo hệ thống: {e}")
        return
    
    # Main loop
    while True:
        print_menu()
        choice = input("\nChọn chức năng (0-8): ").strip()
        
        if choice == '0':
            print("\nCảm ơn bạn đã sử dụng hệ thống!")
            break
        
        elif choice == '1':
            # Show all recipes
            display_recipes(recipes, "TẤT CẢ CÔNG THỨC")
        
        elif choice == '2':
            # Search by ID
            recipe_id = input("\nNhập ID công thức: ").strip()
            recipe = service.get_recipe_by_id(recipe_id)
            if recipe:
                print("\n" + "=" * 60)
                print(format_recipe_summary(recipe))
                print("=" * 60)
            else:
                print(f"\nKhông tìm thấy công thức với ID: {recipe_id}")
        
        elif choice == '3':
            # Filter by flavor
            flavors = service.get_unique_flavors()
            print("\nCác hương vị có sẵn:")
            for i, flavor in enumerate(flavors, 1):
                print(f"{i}. {flavor}")
            
            flavor_input = input("\nNhập tên hương vị: ").strip()
            filtered = service.get_recipes_by_flavor(flavor_input)
            display_recipes(filtered, f"CÔNG THỨC HƯƠNG VỊ: {flavor_input.upper()}")
        
        elif choice == '4':
            # Filter by difficulty
            print("\nCác mức độ khó:")
            print("1. Dễ")
            print("2. Trung bình")
            print("3. Khó")
            
            diff_input = input("\nNhập độ khó: ").strip()
            filtered = service.search_recipes(difficulty=diff_input)
            display_recipes(filtered, f"CÔNG THỨC ĐỘ KHÓ: {diff_input.upper()}")
        
        elif choice == '5':
            # Show easy recipes
            easy_recipes = service.get_easy_recipes()
            display_recipes(easy_recipes, "CÔNG THỨC DỄ LÀM")
        
        elif choice == '6':
            # Show trending recipes
            trending = service.get_trending_recipes()
            display_recipes(trending, "CÔNG THỨC ĐANG XU HƯỚNG")
        
        elif choice == '7':
            # Show analysis report
            analysis = analyzer.generate_summary_report()
            print(format_analysis_report(analysis))
        
        elif choice == '8':
            # Show system summary
            summary = service.get_recipes_summary()
            print("\n" + "=" * 60)
            print("TÓM TẮT HỆ THỐNG")
            print("=" * 60)
            print(f"Tổng số công thức: {summary['total_recipes']}")
            print(f"Số hương vị khác nhau: {summary['unique_flavors']}")
            print(f"Số danh mục khác nhau: {summary['unique_categories']}")
            print(f"Công thức dễ làm: {summary['easy_recipes']}")
            print(f"Công thức đang xu hướng: {summary['trending_recipes']}")
            print("=" * 60)
        
        else:
            print("\nLựa chọn không hợp lệ. Vui lòng chọn từ 0-8.")
        
        input("\nNhấn Enter để tiếp tục...")


if __name__ == '__main__':
    main()
