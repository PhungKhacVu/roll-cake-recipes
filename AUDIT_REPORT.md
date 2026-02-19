# BÁO CÁO KIỂM DUYỆT (AUDIT) VÀ ĐỀ XUẤT CẢI TIẾN
## Dự án: Cơ sở dữ liệu công thức bánh (Roll Cake Recipes)

**Người thực hiện**: Senior Software Architect & Lead Developer
**Ngày**: 2026-02-19
**Công nghệ**: Python 3.11+, FastAPI, Pydantic, Pytest

---

## TÓM TẮT ĐIỀU HÀNH (EXECUTIVE SUMMARY)

Dự án hiện tại là một cơ sở dữ liệu công thức bánh được lưu trữ dưới dạng CSV. Mặc dù dữ liệu có giá trị, việc thiếu cấu trúc phần mềm chuyên nghiệp, validation, testing và bảo mật tạo ra nhiều rủi ro cho việc mở rộng và bảo trì.

### Vấn đề ưu tiên cao cần giải quyết ngay:

1. **THIẾU DATA VALIDATION** - Không có kiểm tra tính hợp lệ của dữ liệu
2. **THIẾU STRUCTURE** - Không có cấu trúc project chuẩn
3. **THIẾU TESTING** - Không có unit tests hoặc integration tests
4. **THIẾU API LAYER** - Không có interface để truy cập dữ liệu
5. **THIẾU CI/CD** - Không có automated testing và deployment
6. **THIẾU SECURITY** - Không có xử lý input sanitization và validation

---

## 1. KIẾN TRÚC & THIẾT KẾ

### 1.1. Vấn đề hiện tại

❌ **Vi phạm SOLID Principles**:
- **Single Responsibility**: Dữ liệu và logic không được tách biệt
- **Open/Closed**: Không có abstraction layer để mở rộng
- **Dependency Inversion**: Không có interface hoặc contracts

❌ **Vi phạm DRY (Don't Repeat Yourself)**:
- Duplicate data trong hai CSV files (roll_cake_recipes.csv và roll_cake_recipes_updated.csv)
- Không có single source of truth

❌ **Thiếu Design Patterns**:
- Không có Repository Pattern cho data access
- Không có Factory Pattern cho object creation
- Không có Singleton Pattern cho configuration

### 1.2. Đề xuất cải tiến

✅ **Áp dụng Clean Architecture**:
```
/roll-cake-recipes/
├── src/
│   ├── domain/          # Business logic & entities
│   │   ├── models.py    # Pydantic models (Domain entities)
│   │   └── interfaces.py # Abstract interfaces
│   ├── application/     # Use cases & services
│   │   ├── services.py  # Business logic services
│   │   └── validators.py # Data validation logic
│   ├── infrastructure/  # External concerns
│   │   ├── repositories.py # Data access (Repository Pattern)
│   │   └── csv_adapter.py  # CSV file handling
│   └── api/            # API endpoints
│       └── endpoints.py # FastAPI routes
├── tests/              # Unit & integration tests
├── data/              # Data files
└── docs/              # Documentation
```

✅ **Design Patterns**:
- **Repository Pattern**: Tách biệt data access logic
- **Factory Pattern**: Tạo recipe objects từ CSV data
- **Singleton Pattern**: Configuration management
- **Strategy Pattern**: Multiple validation strategies

---

## 2. HIỆU SUẤT (PERFORMANCE)

### 2.1. Bottlenecks hiện tại

❌ **I/O Bottlenecks**:
- Reading entire CSV file vào memory mỗi lần truy cập
- Time Complexity: O(n) cho mỗi search operation
- Space Complexity: O(n) - load toàn bộ data vào RAM

❌ **Không có Caching**:
- Mỗi request đều phải đọc file từ disk
- Không có in-memory cache

❌ **Không có Indexing**:
- Linear search cho tất cả queries
- Không có index cho Recipe_ID, Category, Flavor_Profile

### 2.2. Đề xuất tối ưu hóa

✅ **Caching Strategy**:
```python
# Sử dụng functools.lru_cache
from functools import lru_cache

@lru_cache(maxsize=1)
def load_recipes_cached():
    """Load recipes with caching - O(1) after first call"""
    return load_recipes_from_csv()
```

✅ **Indexing**:
```python
# Tạo index dictionaries
recipes_by_id: Dict[str, Recipe] = {}      # O(1) lookup
recipes_by_flavor: Dict[str, List[Recipe]] = {}  # O(1) lookup
```

✅ **Lazy Loading**:
- Chỉ load data khi cần thiết
- Pagination cho large datasets

✅ **Database Migration** (Future):
- Migrate từ CSV sang SQLite/PostgreSQL
- Indexed queries: O(log n) hoặc O(1)

---

## 3. BẢO MẬT (SECURITY)

### 3.1. Lỗ hổng bảo mật theo OWASP Top 10

❌ **A03:2021 - Injection**:
- Không validate CSV input
- Risk: CSV Injection (Formula Injection)
- Ví dụ: `=cmd|'/c calc'!A0` trong CSV cell

❌ **A04:2021 - Insecure Design**:
- Không có authentication/authorization
- Bất kỳ ai cũng có thể access hoặc modify data

❌ **A05:2021 - Security Misconfiguration**:
- Không có .gitignore cho sensitive files
- Không có environment variable management

❌ **A08:2021 - Software and Data Integrity Failures**:
- Không verify CSV data integrity
- Không có checksum hoặc digital signatures

❌ **A09:2021 - Security Logging and Monitoring Failures**:
- Không có logging cho data access
- Không track data modifications

### 3.2. Đề xuất bảo mật

✅ **Input Validation & Sanitization**:
```python
from pydantic import BaseModel, validator, Field

class Recipe(BaseModel):
    recipe_id: str = Field(..., regex=r'^[a-z0-9_]+$')
    recipe_name: str = Field(..., min_length=1, max_length=200)
    prep_time_minutes: float = Field(..., ge=0, le=1440)

    @validator('recipe_name', 'description')
    def sanitize_text(cls, v):
        # Prevent CSV injection
        if v and v[0] in ['=', '+', '-', '@']:
            raise ValueError('Invalid character at start')
        return v.strip()
```

✅ **Environment Variables**:
```python
# .env file for sensitive configuration
from pydantic import BaseSettings

class Settings(BaseSettings):
    data_path: str
    api_key: str
    allowed_origins: List[str]

    class Config:
        env_file = ".env"
```

✅ **Access Control**:
```python
# API rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/recipes")
@limiter.limit("100/minute")
async def get_recipes():
    pass
```

✅ **Audit Logging**:
```python
import logging

logger = logging.getLogger(__name__)

def log_access(user_id: str, action: str, resource: str):
    logger.info(f"User {user_id} performed {action} on {resource}")
```

---

## 4. CHẤT LƯỢNG MÃ (CLEAN CODE)

### 4.1. Vấn đề hiện tại

❌ **Không có Code**:
- Chỉ có raw CSV data
- Không có logic xử lý

❌ **Thiếu Documentation**:
- README cơ bản, không có technical docs
- Không có API documentation

❌ **Inconsistent Data Format**:
- Mixed language (Vietnamese và English)
- Inconsistent naming conventions

### 4.2. Đề xuất cải tiến

✅ **Clean Code Principles**:
```python
# BAD: Magic numbers
if prep_time > 30:
    difficulty = "Hard"

# GOOD: Named constants
PREP_TIME_THRESHOLD_MEDIUM = 30
PREP_TIME_THRESHOLD_HARD = 60

if prep_time > PREP_TIME_THRESHOLD_HARD:
    difficulty = DifficultyLevel.HARD
elif prep_time > PREP_TIME_THRESHOLD_MEDIUM:
    difficulty = DifficultyLevel.MEDIUM
else:
    difficulty = DifficultyLevel.EASY
```

✅ **Type Hints & Documentation**:
```python
from typing import List, Optional
from enum import Enum

class DifficultyLevel(Enum):
    """Enumeration of recipe difficulty levels."""
    EASY = "Dễ"
    MEDIUM = "Trung bình"
    HARD = "Khó"

def calculate_difficulty(
    prep_time: float,
    cook_time: float,
    ingredient_count: int
) -> DifficultyLevel:
    """
    Calculate recipe difficulty based on multiple factors.

    Args:
        prep_time: Preparation time in minutes
        cook_time: Cooking time in minutes
        ingredient_count: Number of ingredients

    Returns:
        Calculated difficulty level

    Examples:
        >>> calculate_difficulty(10, 15, 5)
        DifficultyLevel.EASY
    """
    total_time = prep_time + cook_time

    if total_time > 90 or ingredient_count > 15:
        return DifficultyLevel.HARD
    elif total_time > 45 or ingredient_count > 10:
        return DifficultyLevel.MEDIUM
    else:
        return DifficultyLevel.EASY
```

✅ **Consistent Naming**:
- Use snake_case for Python (PEP 8)
- Use descriptive names: `get_recipe_by_id()` not `get()`
- Avoid abbreviations: `recipe_repository` not `rec_repo`

---

## 5. ĐỘ TIN CẬY & KIỂM THỬ

### 5.1. Vấn đề hiện tại

❌ **Không có Tests**:
- Zero test coverage
- Không có CI/CD pipeline

❌ **Edge Cases không được xử lý**:
- Empty CSV files
- Malformed data (missing fields, wrong types)
- Duplicate Recipe_IDs
- Invalid URLs
- Negative numbers for time/servings

❌ **Không có Error Handling**:
- No try-catch blocks
- No validation before processing

### 5.2. Đề xuất Testing Strategy

✅ **Unit Tests với Pytest**:
```python
import pytest
from src.domain.models import Recipe, Ingredient
from src.application.validators import RecipeValidator
from pydantic import ValidationError

class TestRecipeModel:
    """Test suite for Recipe domain model."""

    def test_valid_recipe_creation(self):
        """Test creating a valid recipe."""
        recipe = Recipe(
            recipe_id="test_001",
            recipe_name="Test Cake",
            category="Hiện đại",
            flavor_profile="Chocolate",
            difficulty_level="Dễ",
            prep_time_minutes=20,
            cook_time_minutes=30,
            servings=8
        )
        assert recipe.recipe_id == "test_001"
        assert recipe.total_time_minutes == 50

    def test_invalid_recipe_id(self):
        """Test that invalid recipe IDs are rejected."""
        with pytest.raises(ValidationError) as exc_info:
            Recipe(
                recipe_id="INVALID ID!",  # Spaces and special chars
                recipe_name="Test",
                # ... other fields
            )
        assert "recipe_id" in str(exc_info.value)

    def test_negative_prep_time(self):
        """Test that negative prep time is rejected."""
        with pytest.raises(ValidationError):
            Recipe(
                recipe_id="test_001",
                recipe_name="Test",
                prep_time_minutes=-10  # Invalid
            )

    def test_csv_injection_prevention(self):
        """Test that CSV injection attempts are blocked."""
        with pytest.raises(ValidationError):
            Recipe(
                recipe_id="test_001",
                recipe_name="=cmd|'/c calc'!A0"  # CSV injection attempt
            )

class TestRecipeRepository:
    """Test suite for Recipe Repository."""

    @pytest.fixture
    def mock_csv_data(self, tmp_path):
        """Create a temporary CSV file for testing."""
        csv_file = tmp_path / "test_recipes.csv"
        csv_file.write_text(
            "Recipe_ID,Recipe_Name,Category\n"
            "test_001,Test Cake,Hiện đại\n"
        )
        return csv_file

    def test_load_recipes_from_csv(self, mock_csv_data):
        """Test loading recipes from CSV file."""
        repo = RecipeRepository(str(mock_csv_data))
        recipes = repo.get_all()
        assert len(recipes) == 1
        assert recipes[0].recipe_id == "test_001"

    def test_empty_csv_file(self, tmp_path):
        """Test handling of empty CSV file."""
        empty_csv = tmp_path / "empty.csv"
        empty_csv.write_text("")
        repo = RecipeRepository(str(empty_csv))
        recipes = repo.get_all()
        assert recipes == []

    def test_duplicate_recipe_ids(self, tmp_path):
        """Test that duplicate IDs are detected."""
        csv_file = tmp_path / "duplicate.csv"
        csv_file.write_text(
            "Recipe_ID,Recipe_Name\n"
            "test_001,Cake 1\n"
            "test_001,Cake 2\n"  # Duplicate!
        )
        repo = RecipeRepository(str(csv_file))
        with pytest.raises(ValueError, match="Duplicate recipe ID"):
            repo.get_all()

class TestRecipeService:
    """Test suite for Recipe Service (business logic)."""

    def test_search_by_flavor(self):
        """Test searching recipes by flavor profile."""
        service = RecipeService()
        results = service.search_by_flavor("Chocolate")
        assert all(r.flavor_profile == "Chocolate" for r in results)

    def test_filter_by_difficulty(self):
        """Test filtering recipes by difficulty."""
        service = RecipeService()
        easy_recipes = service.filter_by_difficulty("Dễ")
        assert all(r.difficulty_level == "Dễ" for r in easy_recipes)

    def test_calculate_total_time(self):
        """Test total time calculation."""
        recipe = Recipe(prep_time_minutes=20, cook_time_minutes=30)
        assert recipe.total_time_minutes == 50

@pytest.mark.integration
class TestAPIEndpoints:
    """Integration tests for API endpoints."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        from fastapi.testclient import TestClient
        from src.api.main import app
        return TestClient(app)

    def test_get_all_recipes(self, client):
        """Test GET /recipes endpoint."""
        response = client.get("/api/v1/recipes")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_recipe_by_id(self, client):
        """Test GET /recipes/{id} endpoint."""
        response = client.get("/api/v1/recipes/japanese_fruit_roll_cake_001")
        assert response.status_code == 200
        recipe = response.json()
        assert recipe["recipe_id"] == "japanese_fruit_roll_cake_001"

    def test_get_nonexistent_recipe(self, client):
        """Test 404 for nonexistent recipe."""
        response = client.get("/api/v1/recipes/nonexistent_999")
        assert response.status_code == 404

    def test_search_with_filters(self, client):
        """Test search with query parameters."""
        response = client.get(
            "/api/v1/recipes/search?flavor=Chocolate&difficulty=Dễ"
        )
        assert response.status_code == 200
```

✅ **Test Coverage Requirements**:
- Minimum 80% code coverage
- 100% coverage for critical paths (validation, security)

✅ **Property-Based Testing**:
```python
from hypothesis import given, strategies as st

@given(
    prep_time=st.floats(min_value=0, max_value=1440),
    cook_time=st.floats(min_value=0, max_value=1440)
)
def test_total_time_always_positive(prep_time, cook_time):
    """Property: Total time should always be non-negative."""
    recipe = Recipe(
        prep_time_minutes=prep_time,
        cook_time_minutes=cook_time
    )
    assert recipe.total_time_minutes >= 0
```

---

## 6. KIẾN TRÚC HỆ THỐNG MỚI

### 6.1. Technology Stack

```
Backend:
- Python 3.11+
- FastAPI (High-performance async API)
- Pydantic (Data validation)
- Pandas (Data processing)
- SQLAlchemy (Future database ORM)

Testing:
- Pytest (Unit & integration tests)
- Pytest-cov (Coverage reporting)
- Hypothesis (Property-based testing)

CI/CD:
- GitHub Actions
- Pre-commit hooks
- Black (Code formatting)
- Ruff (Fast linting)
- MyPy (Static type checking)

Documentation:
- Sphinx (Auto-generated docs)
- MkDocs (User documentation)
- OpenAPI/Swagger (API docs)
```

### 6.2. API Design

```python
# RESTful API Endpoints

GET    /api/v1/recipes              # List all recipes (paginated)
GET    /api/v1/recipes/{id}         # Get specific recipe
GET    /api/v1/recipes/search       # Search recipes with filters
GET    /api/v1/recipes/random       # Get random recipe
GET    /api/v1/flavors              # List all flavor profiles
GET    /api/v1/categories           # List all categories
GET    /api/v1/stats                # Get statistics

# Query parameters for search:
# ?flavor=Chocolate
# ?difficulty=Dễ
# ?max_prep_time=30
# ?category=Hiện đại
# ?page=1&per_page=20
```

---

## 7. MIGRATION PLAN

### Phase 1: Foundation (Week 1)
- [x] Create project structure
- [ ] Add .gitignore and requirements.txt
- [ ] Create Pydantic models
- [ ] Implement basic CSV loader
- [ ] Write unit tests

### Phase 2: API Layer (Week 2)
- [ ] Implement FastAPI endpoints
- [ ] Add validation middleware
- [ ] Create OpenAPI documentation
- [ ] Add error handling

### Phase 3: Testing & Quality (Week 3)
- [ ] Achieve 80%+ test coverage
- [ ] Add integration tests
- [ ] Set up CI/CD pipeline
- [ ] Add pre-commit hooks

### Phase 4: Security & Performance (Week 4)
- [ ] Implement rate limiting
- [ ] Add authentication (optional)
- [ ] Implement caching
- [ ] Performance optimization

### Phase 5: Database Migration (Future)
- [ ] Design database schema
- [ ] Migrate CSV to PostgreSQL
- [ ] Update repository layer
- [ ] Add database migrations

---

## 8. METRICS & KPIs

### Code Quality Metrics
- Test Coverage: Target 80%+ (Current: 0%)
- Code Complexity: Cyclomatic complexity < 10
- Type Coverage: 100% (mypy strict)
- Documentation: 100% public API documented

### Performance Metrics
- API Response Time: < 100ms (p95)
- Memory Usage: < 512MB for full dataset
- Throughput: > 1000 requests/second

### Security Metrics
- Zero High/Critical vulnerabilities (Bandit scan)
- All inputs validated (100%)
- Audit logs for all data access

---

## 9. KẾT LUẬN

Dự án hiện tại cần một cuộc đại tu toàn diện để đạt được tiêu chuẩn production-ready. Các cải tiến được đề xuất sẽ:

1. **Tăng độ tin cậy**: Qua testing và validation
2. **Cải thiện bảo mật**: Qua input validation và sanitization
3. **Tăng hiệu suất**: Qua caching và indexing
4. **Dễ bảo trì**: Qua clean architecture và documentation
5. **Dễ mở rộng**: Qua proper abstraction và design patterns

### Next Steps
1. Review và approve audit report này
2. Prioritize các improvements theo business value
3. Implement theo phases đã định nghĩa
4. Continuous monitoring và improvement

---

**Prepared by**: Senior Software Architect
**Review Status**: Pending Approval
**Last Updated**: 2026-02-19
