# Kiến trúc Phần mềm Quản lý Công thức Bánh

## Tổng quan

Dự án này đã được tái cấu trúc để tuân theo các nguyên tắc thiết kế phần mềm hiện đại:
- **SOLID Principles**: Năm nguyên tắc thiết kế hướng đối tượng
- **DRY (Don't Repeat Yourself)**: Tránh lặp code
- **KISS (Keep It Simple, Stupid)**: Giữ mọi thứ đơn giản

## Cấu trúc Dự án

```
roll-cake-recipes/
├── src/                          # Mã nguồn chính
│   ├── models/                   # Domain models (Recipe, Ingredient)
│   │   ├── __init__.py
│   │   ├── recipe.py            # Recipe model
│   │   └── ingredient.py        # Ingredient model
│   ├── repositories/             # Data Access Layer
│   │   ├── __init__.py
│   │   ├── base_repository.py   # Repository interface
│   │   └── csv_repository.py    # CSV implementation
│   ├── services/                 # Business Logic Layer
│   │   ├── __init__.py
│   │   └── recipe_service.py    # Recipe business logic
│   ├── analytics/                # Analytics and Statistics
│   │   ├── __init__.py
│   │   └── recipe_analyzer.py   # Recipe analytics
│   ├── utils/                    # Utilities
│   │   ├── __init__.py
│   │   ├── formatters.py        # Formatting utilities
│   │   └── validators.py        # Validation utilities
│   └── config/                   # Configuration
│       ├── __init__.py
│       └── settings.py          # App settings
├── cli.py                        # Command-line interface
├── examples.py                   # Usage examples
├── ARCHITECTURE.md              # This file
├── requirements.txt             # Python dependencies
└── roll_cake_recipes_updated.csv # Data file
```

## Nguyên tắc SOLID được áp dụng

### 1. Single Responsibility Principle (SRP)
**Mỗi class chỉ có một lý do duy nhất để thay đổi.**

- `Recipe`: Chỉ đại diện cho một công thức bánh
- `Ingredient`: Chỉ đại diện cho một nguyên liệu
- `CSVRecipeRepository`: Chỉ xử lý truy cập dữ liệu CSV
- `RecipeService`: Chỉ xử lý logic nghiệp vụ
- `RecipeAnalyzer`: Chỉ xử lý phân tích và thống kê

### 2. Open/Closed Principle (OCP)
**Mở cho mở rộng, đóng cho sửa đổi.**

- `IRepository` interface cho phép thêm các nguồn dữ liệu mới (JSON, Database, API) mà không cần sửa code hiện có
- Có thể thêm các service mới kế thừa từ các interface hiện có
- Có thể mở rộng analytics mà không ảnh hưởng đến code cũ

```python
# Ví dụ mở rộng: Thêm nguồn dữ liệu mới
class DatabaseRecipeRepository(IRepository):
    def get_all(self):
        # Implementation for database
        pass
```

### 3. Liskov Substitution Principle (LSP)
**Các đối tượng có thể được thay thế bởi các đối tượng con của chúng.**

- Bất kỳ implementation nào của `IRepository` đều có thể được sử dụng với `RecipeService`
- `CSVRecipeRepository` có thể được thay thế bởi `DatabaseRepository` mà không ảnh hưởng đến logic

```python
# Có thể swap repository dễ dàng
repository = CSVRecipeRepository(file_path)
# hoặc
repository = DatabaseRepository(connection_string)

# Service hoạt động với cả hai
service = RecipeService(repository)
```

### 4. Interface Segregation Principle (ISP)
**Client không nên phụ thuộc vào các interface mà họ không sử dụng.**

- `IRepository` chỉ định nghĩa các method cần thiết: `get_all()`, `get_by_id()`, `filter()`, `count()`
- Không có các method không cần thiết hoặc phức tạp
- Mỗi interface nhỏ, tập trung và dễ implement

### 5. Dependency Inversion Principle (DIP)
**Phụ thuộc vào abstraction, không phụ thuộc vào implementation cụ thể.**

- `RecipeService` phụ thuộc vào `IRepository` (abstraction), không phải `CSVRecipeRepository` (concrete)
- Giúp dễ dàng test và swap implementations

```python
class RecipeService:
    def __init__(self, repository: IRepository):  # Depends on interface
        self.repository = repository
```

## Nguyên tắc DRY (Don't Repeat Yourself)

### 1. Reusable Analytics Methods
```python
# Thay vì lặp code cho mỗi field
def count_by_field(self, field_name: str):
    """Generic counting method - reusable for any field"""
    pass

# Sử dụng cho nhiều cases
count_by_flavor()  # Uses count_by_field
count_by_difficulty()  # Uses count_by_field
count_by_category()  # Uses count_by_field
```

### 2. Reusable Formatting Functions
```python
# Format time một cách nhất quán
format_time(minutes)  # Dùng ở nhiều nơi

# Format percentage một cách nhất quán
format_percentage(value)  # Dùng ở nhiều nơi
```

### 3. Reusable Validation Logic
```python
# Validation logic được tập trung
validate_recipe_data(data)
validate_ingredient_data(data)
```

## Nguyên tắc KISS (Keep It Simple, Stupid)

### 1. Simple Models
- Models đơn giản, chỉ chứa data và behavior cơ bản
- Không có logic phức tạp trong models

### 2. Simple Configuration
```python
class Config:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DEFAULT_CSV_FILE = BASE_DIR / 'roll_cake_recipes_updated.csv'
```

### 3. Simple CLI Interface
- Menu đơn giản, dễ hiểu
- Không có UI phức tạp
- Chỉ cung cấp các chức năng cần thiết

### 4. Clear Separation of Concerns
- Mỗi module có trách nhiệm rõ ràng
- Code dễ đọc, dễ hiểu
- Không có coupling phức tạp

## Lợi ích của Kiến trúc Mới

### 1. Modularity (Tính Module hóa)
- Mỗi component độc lập
- Có thể phát triển và test riêng biệt
- Dễ dàng tái sử dụng

### 2. Extensibility (Khả năng Mở rộng)
- Dễ dàng thêm features mới
- Dễ dàng thêm nguồn dữ liệu mới
- Không cần sửa code cũ

### 3. Testability (Khả năng Test)
- Mỗi component có thể test độc lập
- Dễ dàng mock dependencies
- Unit test và integration test đơn giản

### 4. Maintainability (Khả năng Bảo trì)
- Code rõ ràng, dễ hiểu
- Dễ dàng tìm và sửa lỗi
- Dễ dàng thêm tính năng mới

### 5. Reusability (Khả năng Tái sử dụng)
- Components có thể được sử dụng trong các dự án khác
- Utilities và helpers có thể tái sử dụng
- Models có thể được share

## Cách Sử dụng

### 1. Sử dụng CLI
```bash
python cli.py
```

### 2. Sử dụng như Library
```python
from src.repositories import CSVRecipeRepository
from src.services import RecipeService
from src.config import Config

# Initialize
repository = CSVRecipeRepository(str(Config.DEFAULT_CSV_FILE))
service = RecipeService(repository)

# Use
recipes = service.get_all_recipes()
easy_recipes = service.get_easy_recipes()
```

### 3. Chạy Examples
```bash
python examples.py
```

## Mở rộng trong Tương lai

### 1. Thêm Data Sources
```python
class DatabaseRecipeRepository(IRepository):
    """Repository using database instead of CSV"""
    pass

class APIRecipeRepository(IRepository):
    """Repository using REST API"""
    pass
```

### 2. Thêm Services
```python
class IngredientService:
    """Service for ingredient management"""
    pass

class RecommendationService:
    """Service for recipe recommendations"""
    pass
```

### 3. Thêm Analytics
```python
class TrendAnalyzer:
    """Analyzer for market trends"""
    pass

class NutritionAnalyzer:
    """Analyzer for nutrition information"""
    pass
```

### 4. Thêm Exporters
```python
class PDFExporter:
    """Export recipes to PDF"""
    pass

class JSONExporter:
    """Export recipes to JSON"""
    pass
```

## Kết luận

Kiến trúc mới này:
- ✅ Tuân theo SOLID principles
- ✅ Áp dụng DRY - không lặp code
- ✅ Giữ đơn giản theo KISS
- ✅ Dễ mở rộng và bảo trì
- ✅ Module hóa tốt
- ✅ Dễ test
- ✅ Rõ ràng và dễ hiểu

Đây là nền tảng vững chắc cho việc phát triển thêm các tính năng mới trong tương lai.
