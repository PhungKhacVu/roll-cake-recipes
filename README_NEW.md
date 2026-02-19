# Hệ thống Quản lý Công thức Bánh Bông Lan Cuộn

## 🎯 Giới thiệu

Dự án này là một hệ thống quản lý công thức bánh bông lan cuộn được thiết kế với kiến trúc phần mềm hiện đại, tuân theo các nguyên tắc **SOLID**, **DRY** và **KISS**.

## ✨ Tính năng

- 📚 Quản lý cơ sở dữ liệu công thức bánh
- 🔍 Tìm kiếm và lọc công thức theo nhiều tiêu chí
- 📊 Phân tích dữ liệu và thống kê
- 💻 Giao diện dòng lệnh (CLI) đơn giản
- 🧩 Kiến trúc module hóa, dễ mở rộng

## 🏗️ Kiến trúc

Dự án được tổ chức theo kiến trúc phân lớp (Layered Architecture):

```
┌─────────────────────────────────────┐
│      Presentation Layer (CLI)       │  ← KISS: Đơn giản, dễ sử dụng
├─────────────────────────────────────┤
│     Business Logic (Services)       │  ← SRP: Mỗi service một nhiệm vụ
├─────────────────────────────────────┤
│    Data Access (Repositories)       │  ← DIP: Phụ thuộc vào abstraction
├─────────────────────────────────────┤
│      Domain Models (Entities)       │  ← SRP: Models đơn giản, rõ ràng
└─────────────────────────────────────┘
```

### Nguyên tắc SOLID

1. **Single Responsibility**: Mỗi class có một trách nhiệm duy nhất
2. **Open/Closed**: Mở cho mở rộng, đóng cho sửa đổi
3. **Liskov Substitution**: Có thể thay thế implementations
4. **Interface Segregation**: Interfaces nhỏ, tập trung
5. **Dependency Inversion**: Phụ thuộc vào abstractions

### Nguyên tắc DRY

- Không lặp code
- Các hàm tiện ích được tái sử dụng
- Generic methods cho operations chung

### Nguyên tắc KISS

- Giao diện đơn giản
- Code dễ đọc, dễ hiểu
- Không over-engineering

Xem [ARCHITECTURE.md](ARCHITECTURE.md) để biết chi tiết.

## 📦 Cài đặt

### Yêu cầu

- Python 3.7 trở lên
- Không cần thư viện bên ngoài (chỉ sử dụng Python standard library)

### Cài đặt

```bash
# Clone repository
git clone https://github.com/PhungKhacVu/roll-cake-recipes.git
cd roll-cake-recipes

# (Optional) Cài đặt dependencies cho features tương lai
pip install -r requirements.txt
```

## 🚀 Sử dụng

### 1. Chạy CLI

```bash
python cli.py
```

Menu CLI cung cấp các chức năng:
- Xem tất cả công thức
- Tìm kiếm theo ID
- Lọc theo hương vị, độ khó
- Xem công thức dễ làm
- Xem công thức đang xu hướng
- Xem báo cáo phân tích

### 2. Sử dụng như Library

```python
from src.repositories import CSVRecipeRepository
from src.services import RecipeService
from src.analytics import RecipeAnalyzer
from src.config import Config

# Khởi tạo
repository = CSVRecipeRepository(str(Config.DEFAULT_CSV_FILE))
service = RecipeService(repository)

# Lấy tất cả công thức
recipes = service.get_all_recipes()

# Tìm kiếm
chocolate_recipes = service.get_recipes_by_flavor("Chocolate")
easy_recipes = service.get_easy_recipes()

# Phân tích
analyzer = RecipeAnalyzer(recipes)
report = analyzer.generate_summary_report()
```

### 3. Chạy Examples

```bash
python examples.py
```

## 📊 Dữ liệu

Dữ liệu được lưu trong file CSV với các trường:
- Recipe_ID, Recipe_Name, Description
- Category, Flavor_Profile, Difficulty_Level
- Prep_Time, Cook_Time, Total_Time
- Ingredients, Instructions
- Tips_Tricks, Storage_Instructions
- Customer_Feedback_Score, Market_Trend_Relevance

## 🔧 Cấu trúc Thư mục

```
roll-cake-recipes/
├── src/                      # Mã nguồn
│   ├── models/              # Domain models
│   ├── repositories/        # Data access layer
│   ├── services/            # Business logic
│   ├── analytics/           # Analytics module
│   ├── utils/               # Utilities
│   └── config/              # Configuration
├── cli.py                   # CLI application
├── examples.py              # Usage examples
├── ARCHITECTURE.md          # Architecture documentation
├── README_NEW.md            # This file
└── requirements.txt         # Dependencies
```

## 🎨 Ví dụ

### Tìm kiếm công thức

```python
# Tìm theo hương vị
fruit_recipes = service.get_recipes_by_flavor("Trái cây")

# Tìm theo độ khó
easy_recipes = service.search_recipes(difficulty="Dễ")

# Tìm với nhiều tiêu chí
results = service.search_recipes(
    flavor="Chocolate",
    difficulty="Trung bình",
    max_time=90
)
```

### Phân tích dữ liệu

```python
analyzer = RecipeAnalyzer(recipes)

# Đếm theo hương vị
flavor_counts = analyzer.count_by_flavor()

# Thống kê thời gian
time_stats = analyzer.get_time_statistics()

# Top nguyên liệu
top_ingredients = analyzer.get_most_common_ingredients(10)

# Báo cáo tổng hợp
report = analyzer.generate_summary_report()
```

## 🔌 Mở rộng

Kiến trúc cho phép dễ dàng mở rộng:

### Thêm nguồn dữ liệu mới

```python
from src.repositories import IRepository

class DatabaseRecipeRepository(IRepository):
    def get_all(self):
        # Lấy từ database
        pass
```

### Thêm service mới

```python
class RecommendationService:
    """Service đề xuất công thức"""
    def recommend(self, user_preferences):
        # Logic đề xuất
        pass
```

### Thêm analytics mới

```python
class NutritionAnalyzer:
    """Phân tích dinh dưỡng"""
    def calculate_nutrition(self, recipe):
        # Tính toán
        pass
```

## 🧪 Testing

```python
# Unit test example
def test_recipe_service():
    repository = CSVRecipeRepository("test_data.csv")
    service = RecipeService(repository)
    recipes = service.get_all_recipes()
    assert len(recipes) > 0
```

## 📝 License

MIT License

## 👤 Tác giả

PhungKhacVu

## 🤝 Đóng góp

Contributions, issues và feature requests được chào đón!

## 📚 Tài liệu Bổ sung

- [ARCHITECTURE.md](ARCHITECTURE.md) - Chi tiết về kiến trúc
- [examples.py](examples.py) - Các ví dụ sử dụng
- [README.md](README.md) - README gốc với thông tin dữ liệu

---

⭐ Nếu bạn thấy dự án hữu ích, hãy cho một star!
