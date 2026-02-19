# Roll Cake Recipes Database (Cơ sở dữ liệu công thức bánh)

[![CI/CD](https://github.com/PhungKhacVu/roll-cake-recipes/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/PhungKhacVu/roll-cake-recipes/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Production-ready API for Vietnamese Roll Cake Recipes with comprehensive data validation, security measures, and automated testing.**

Cơ sở dữ liệu này chứa các công thức làm bánh bông lan cuộn và bánh Pate de Choux được thu thập và phân tích theo xu hướng thị trường. Mục đích là cung cấp một nguồn tài nguyên phong phú cho việc nghiên cứu, phát triển sản phẩm và chia sẻ công thức với khách hàng.

## 🚀 Tính năng mới

- ✅ **RESTful API** với FastAPI - High-performance async API
- ✅ **Data Validation** - Pydantic models với security measures
- ✅ **Clean Architecture** - Domain-driven design với clear separation of concerns
- ✅ **Comprehensive Testing** - Unit tests với 80%+ coverage
- ✅ **CI/CD Pipeline** - Automated testing và code quality checks
- ✅ **Security** - CSV injection prevention, input sanitization, rate limiting
- ✅ **Documentation** - Auto-generated OpenAPI/Swagger docs
- ✅ **Type Safety** - Full type hints với MyPy validation

## 📋 Mục lục

- [Cài đặt nhanh](#cài-đặt-nhanh)
- [Kiến trúc](#kiến-trúc)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Testing](#testing)
- [Cấu trúc dữ liệu](#cấu-trúc-dữ-liệu)
- [Bảo mật](#bảo-mật)

## 🚀 Cài đặt nhanh

### Prerequisites

- Python 3.11 or higher
- pip

### Installation

```bash
# Clone repository
git clone https://github.com/PhungKhacVu/roll-cake-recipes.git
cd roll-cake-recipes

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run API server
python -m uvicorn src.api.main:app --reload
```

API sẽ chạy tại: http://localhost:8000

- **API Documentation (Swagger)**: http://localhost:8000/api/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/api/redoc

## 🏗️ Kiến trúc

Project sử dụng **Clean Architecture** với clear separation of concerns:

```
roll-cake-recipes/
├── src/
│   ├── domain/              # Business entities & rules
│   │   └── models.py        # Pydantic models (Recipe, Ingredient, etc.)
│   ├── application/         # Use cases & business logic
│   │   └── services.py      # RecipeService with business operations
│   ├── infrastructure/      # External concerns (data access)
│   │   └── repositories.py  # CSV data access (Repository Pattern)
│   └── api/                # API layer (FastAPI endpoints)
│       └── main.py         # HTTP endpoints & routing
├── tests/
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
├── data/                   # CSV data files
└── docs/                   # Documentation
```

### Design Patterns

- **Repository Pattern**: Abstract data access
- **Service Pattern**: Encapsulate business logic
- **Factory Pattern**: Object creation
- **Dependency Injection**: Loose coupling

## 📚 API Documentation

### Endpoints

#### Recipes

- `GET /api/v1/recipes` - List all recipes (with pagination)
- `GET /api/v1/recipes/{id}` - Get specific recipe
- `GET /api/v1/recipes/search/filter` - Search with filters
- `GET /api/v1/recipes/random/one` - Get random recipe

#### Metadata

- `GET /api/v1/flavors` - List all flavor profiles
- `GET /api/v1/categories` - List all categories
- `GET /api/v1/stats` - Get statistics

#### Curated Collections

- `GET /api/v1/trending` - Get trending recipes
- `GET /api/v1/top-rated` - Get highly rated recipes
- `GET /api/v1/quick-recipes` - Get quick recipes

### Example Usage

```bash
# Get all recipes (paginated)
curl http://localhost:8000/api/v1/recipes?limit=10&offset=0

# Search by flavor
curl "http://localhost:8000/api/v1/recipes/search/filter?flavor=Chocolate&difficulty=Dễ"

# Get statistics
curl http://localhost:8000/api/v1/stats

# Get trending recipes
curl http://localhost:8000/api/v1/trending?limit=5
```

## 💻 Development

### Project Structure

```bash
# Install development dependencies
pip install -r requirements.txt

# Run linting
ruff check src/ tests/

# Run type checking
mypy src/ --ignore-missing-imports

# Format code
black src/ tests/

# Run security scan
bandit -r src/
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_models.py -v

# Run only unit tests
pytest tests/unit/ -v
```

### Test Coverage

Current coverage: **80%+**

- Unit tests: ✅ Models, Repository, Services
- Integration tests: ✅ API endpoints
- Property-based tests: ✅ Data validation

## 📊 Cấu trúc dữ liệu

Cơ sở dữ liệu được lưu trữ dưới dạng file CSV (`data/roll_cake_recipes_updated.csv`) với các trường dữ liệu sau:

*   **Recipe_ID**: Mã định danh duy nhất cho mỗi công thức.
*   **Recipe_Name**: Tên của công thức.
*   **Description**: Mô tả ngắn gọn về công thức.
*   **Category**: Phân loại công thức (ví dụ: Hiện đại, Truyền thống).
*   **Flavor_Profile**: Hồ sơ hương vị chính của bánh (ví dụ: Chocolate, Trái cây, Trà xanh, Sầu riêng, Khoai môn, Trứng muối, Cà phê, Dừa non, Phô mai).
*   **Difficulty_Level**: Mức độ khó của công thức (ví dụ: Dễ, Trung bình, Khó).
*   **Prep_Time_Minutes**: Thời gian chuẩn bị tính bằng phút.
*   **Cook_Time_Minutes**: Thời gian nấu/nướng tính bằng phút.
*   **Total_Time_Minutes**: Tổng thời gian cần thiết tính bằng phút.
*   **Servings**: Số lượng khẩu phần ăn mà công thức tạo ra.
*   **Image_URL**: Đường dẫn URL đến hình ảnh của bánh.
*   **Video_URL**: Đường dẫn URL đến video hướng dẫn (nếu có).
*   **Source**: Nguồn gốc của công thức.
*   **Date_Created**: Ngày công thức được tạo hoặc xuất bản.
*   **Date_Updated**: Ngày công thức được cập nhật lần cuối.
*   **Ingredient_Name**: Tên thành phần.
*   **Quantity**: Số lượng thành phần.
*   **Unit**: Đơn vị của thành phần.
*   **Notes**: Ghi chú về thành phần.
*   **Instructions**: Danh sách các bước hướng dẫn.
*   **Tips_Tricks**: Các mẹo và thủ thuật hữu ích cho công thức.
*   **Storage_Instructions**: Hướng dẫn bảo quản bánh.
*   **Customer_Feedback_Score**: Điểm đánh giá từ khách hàng (nếu có).
*   **Market_Trend_Relevance**: Mức độ liên quan đến xu hướng thị trường (ví dụ: Cao, Trung bình, Thấp).

## Hướng dẫn sử dụng

1.  **Tải xuống:** Tải file `roll_cake_recipes_updated.csv` về máy tính của bạn.
2.  **Mở bằng phần mềm bảng tính:** Bạn có thể mở file CSV bằng các phần mềm như Microsoft Excel, Google Sheets, LibreOffice Calc hoặc bất kỳ trình soạn thảo văn bản nào.
3.  **Phân tích dữ liệu:** Sử dụng các công cụ phân tích dữ liệu trong phần mềm bảng tính để lọc, sắp xếp và tạo biểu đồ từ dữ liệu. Ví dụ, bạn có thể phân tích các hương vị phổ biến, độ khó trung bình, hoặc các thành phần được sử dụng nhiều nhất.
4.  **Cập nhật:** Để cập nhật cơ sở dữ liệu, bạn có thể chỉnh sửa trực tiếp file CSV hoặc thêm các công thức mới theo cấu trúc đã định.
5.  **Nghiên cứu và chia sẻ:** Sử dụng thông tin từ cơ sở dữ liệu để nghiên cứu xu hướng, tạo ra các công thức mới hoặc gửi các công thức đã chọn đến khách hàng của bạn.

## 🔒 Bảo mật

Project implement nhiều security best practices:

### Input Validation & Sanitization

- ✅ **CSV Injection Prevention**: Block dangerous characters (=, +, -, @) at start of fields
- ✅ **URL Validation**: Validate all URLs with regex patterns
- ✅ **Data Type Validation**: Pydantic enforces strict types
- ✅ **Range Validation**: Time values, scores must be in valid ranges

### Security Measures

- ✅ **Rate Limiting**: 100 requests/minute per IP (configurable)
- ✅ **CORS Protection**: Configurable allowed origins
- ✅ **Error Handling**: No sensitive data in error messages
- ✅ **Security Scanning**: Automated Bandit scans in CI/CD

### Example: CSV Injection Prevention

```python
# This will be REJECTED
recipe_name = "=cmd|'/c calc'!A0"  # ❌ CSV injection attempt

# This will be ACCEPTED
recipe_name = "Chocolate Roll Cake"  # ✅ Safe input
```

## 📈 Performance

- **API Response Time**: < 100ms (p95)
- **Caching**: LRU cache for repeated queries (O(1) after first call)
- **Pagination**: Efficient data loading
- **Indexed Lookups**: O(1) recipe lookup by ID

## 🤝 Contributing

Xem [CONTRIBUTING.md](CONTRIBUTING.md) để biết chi tiết về:
- Code style guide
- Pull request process
- Testing requirements
- Code review guidelines

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

- **Repository**: https://github.com/PhungKhacVu/roll-cake-recipes
- **Issues**: https://github.com/PhungKhacVu/roll-cake-recipes/issues

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- Pydantic for data validation
- All contributors to the recipe database

---

## 📊 Phân tích dữ liệu

Các biểu đồ phân tích dữ liệu đã được tạo ra và lưu dưới dạng hình ảnh:

*   `flavor_analysis.png`: Biểu đồ phân tích hương vị bánh bông lan cuộn.
*   `difficulty_analysis.png`: Biểu đồ phân tích độ khó của các công thức bánh bông lan cuộn.
*   `ingredient_analysis.png`: Biểu đồ các thành phần phổ biến nhất trong bánh bông lan cuộn.

Các biểu đồ này cung cấp cái nhìn tổng quan về các đặc điểm chính của các công thức trong cơ sở dữ liệu.

---

**⚡ Powered by Clean Architecture, FastAPI, and Pydantic**
