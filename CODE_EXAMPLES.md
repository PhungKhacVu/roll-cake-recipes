# Code Examples: SOLID, DRY, KISS Implementation

## 📚 Table of Contents
1. [SOLID Principles with Code Examples](#solid-principles)
2. [DRY Principle with Code Examples](#dry-principle)
3. [KISS Principle with Code Examples](#kiss-principle)

---

## SOLID Principles

### 1. Single Responsibility Principle (SRP)

**Principle**: A class should have only one reason to change.

#### ✅ Good Example: Each class has one responsibility

```python
# ✓ Recipe.py - Only handles recipe data
class Recipe:
    """Represents a recipe - ONE responsibility"""
    def __init__(self, recipe_id, name, description):
        self.recipe_id = recipe_id
        self.name = name
        self.description = description
    
    def to_dict(self):
        """Convert to dictionary"""
        return {'recipe_id': self.recipe_id, ...}

# ✓ CSVRecipeRepository.py - Only handles data access
class CSVRecipeRepository:
    """Handles CSV data access - ONE responsibility"""
    def get_all(self):
        """Load from CSV"""
        pass

# ✓ RecipeService.py - Only handles business logic
class RecipeService:
    """Handles business logic - ONE responsibility"""
    def search_recipes(self, criteria):
        """Business logic for search"""
        pass
```

#### ❌ Bad Example: Multiple responsibilities

```python
# ✗ DON'T DO THIS - Multiple responsibilities
class Recipe:
    def __init__(self, ...):
        pass
    
    def save_to_csv(self):  # ✗ Data access responsibility
        pass
    
    def generate_pdf(self):  # ✗ PDF generation responsibility
        pass
    
    def send_email(self):  # ✗ Email responsibility
        pass
    
    # This class has too many reasons to change!
```

---

### 2. Open/Closed Principle (OCP)

**Principle**: Software entities should be open for extension but closed for modification.

#### ✅ Good Example: Extension without modification

```python
# ✓ Define interface (abstraction)
class IRepository(ABC):
    @abstractmethod
    def get_all(self):
        pass

# ✓ Initial implementation
class CSVRecipeRepository(IRepository):
    def get_all(self):
        # Load from CSV
        return self._load_from_csv()

# ✓ NEW: Add database support WITHOUT modifying existing code
class DatabaseRecipeRepository(IRepository):
    def get_all(self):
        # Load from database
        return self._load_from_database()

# ✓ NEW: Add API support WITHOUT modifying existing code
class APIRecipeRepository(IRepository):
    def get_all(self):
        # Load from API
        return self._load_from_api()

# ✓ Service works with ALL implementations
class RecipeService:
    def __init__(self, repository: IRepository):
        self.repository = repository  # Works with any IRepository
```

#### ❌ Bad Example: Modification required for extension

```python
# ✗ DON'T DO THIS - Need to modify existing code
class RecipeService:
    def __init__(self, data_source_type):
        if data_source_type == 'csv':
            self.load = self.load_from_csv
        elif data_source_type == 'database':  # ✗ Need to modify this
            self.load = self.load_from_database
        # Adding new sources requires modifying this class!
```

---

### 3. Liskov Substitution Principle (LSP)

**Principle**: Objects should be replaceable with their subtypes without affecting correctness.

#### ✅ Good Example: Interchangeable implementations

```python
# ✓ Any IRepository implementation can be used
def create_service(use_database=False):
    if use_database:
        repository = DatabaseRecipeRepository(connection)
    else:
        repository = CSVRecipeRepository(file_path)
    
    # Service works the same with either repository
    service = RecipeService(repository)
    return service

# ✓ Both work identically
service1 = RecipeService(CSVRecipeRepository(path))
service2 = RecipeService(DatabaseRecipeRepository(conn))

# Both have same behavior
recipes1 = service1.get_all_recipes()  # ✓ Works
recipes2 = service2.get_all_recipes()  # ✓ Works the same way
```

#### ❌ Bad Example: Inconsistent behavior

```python
# ✗ DON'T DO THIS - Inconsistent behavior
class BaseRepository:
    def get_all(self):
        return []  # Returns list

class BrokenRepository(BaseRepository):
    def get_all(self):
        return None  # ✗ Returns None instead of list!
    
    def get_special_method(self):  # ✗ Extra method not in base
        pass

# This violates LSP - can't substitute safely
```

---

### 4. Interface Segregation Principle (ISP)

**Principle**: No client should be forced to depend on methods it does not use.

#### ✅ Good Example: Minimal, focused interface

```python
# ✓ Minimal interface - only what's needed
class IRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Any]:
        pass
    
    @abstractmethod
    def get_by_id(self, item_id: str) -> Optional[Any]:
        pass
    
    @abstractmethod
    def filter(self, criteria: Dict) -> List[Any]:
        pass
    
    @abstractmethod
    def count(self) -> int:
        pass
    
    # Only 4 essential methods!
```

#### ❌ Bad Example: Fat interface

```python
# ✗ DON'T DO THIS - Too many methods
class IRepository(ABC):
    def get_all(self): pass
    def get_by_id(self): pass
    def create(self): pass  # ✗ Not all implementations need this
    def update(self): pass  # ✗ Not all implementations need this
    def delete(self): pass  # ✗ Not all implementations need this
    def backup(self): pass  # ✗ Not all implementations need this
    def restore(self): pass  # ✗ Not all implementations need this
    def export_to_pdf(self): pass  # ✗ Wrong level of abstraction
    def send_email(self): pass  # ✗ Totally unrelated!
    
    # Forces implementations to implement methods they don't need
```

---

### 5. Dependency Inversion Principle (DIP)

**Principle**: High-level modules should not depend on low-level modules. Both should depend on abstractions.

#### ✅ Good Example: Depend on abstraction

```python
# ✓ High-level module depends on abstraction
class RecipeService:
    def __init__(self, repository: IRepository):  # ✓ Depends on interface
        self.repository = repository
    
    def get_all_recipes(self):
        return self.repository.get_all()

# ✓ Low-level module implements abstraction
class CSVRecipeRepository(IRepository):
    def get_all(self):
        return self._load_from_csv()

# ✓ Easy to test with mock
class MockRepository(IRepository):
    def get_all(self):
        return [Recipe(...), Recipe(...)]

# ✓ Can inject any implementation
service = RecipeService(CSVRecipeRepository(path))
# or
service = RecipeService(MockRepository())
```

#### ❌ Bad Example: Direct dependency on concrete class

```python
# ✗ DON'T DO THIS - Depends on concrete implementation
class RecipeService:
    def __init__(self, csv_file_path):
        # ✗ Directly creates CSVRecipeRepository
        self.repository = CSVRecipeRepository(csv_file_path)
    
    # Can't easily switch to database or mock for testing
    # Tightly coupled to CSV implementation
```

---

## DRY Principle

**Principle**: Don't Repeat Yourself - Every piece of knowledge should have a single representation.

### ✅ Good Example: Reusable generic methods

```python
# ✓ Generic method - DRY
class RecipeAnalyzer:
    def count_by_field(self, field_name: str) -> Dict[str, int]:
        """Generic counting method - reusable!"""
        values = [getattr(r, field_name) for r in self.recipes if getattr(r, field_name)]
        return dict(Counter(values))
    
    # ✓ Reuse generic method
    def count_by_flavor(self):
        return self.count_by_field('flavor_profile')
    
    def count_by_difficulty(self):
        return self.count_by_field('difficulty_level')
    
    def count_by_category(self):
        return self.count_by_field('category')
    
    # One implementation, many uses!
```

### ❌ Bad Example: Code duplication

```python
# ✗ DON'T DO THIS - Repeated code
class RecipeAnalyzer:
    def count_by_flavor(self):
        # ✗ Duplicate logic
        values = []
        for recipe in self.recipes:
            if recipe.flavor_profile:
                values.append(recipe.flavor_profile)
        return dict(Counter(values))
    
    def count_by_difficulty(self):
        # ✗ Same logic repeated
        values = []
        for recipe in self.recipes:
            if recipe.difficulty_level:
                values.append(recipe.difficulty_level)
        return dict(Counter(values))
    
    def count_by_category(self):
        # ✗ Same logic repeated again
        values = []
        for recipe in self.recipes:
            if recipe.category:
                values.append(recipe.category)
        return dict(Counter(values))
    
    # Repeated logic - violation of DRY!
```

### ✅ More DRY Examples

```python
# ✓ Reusable formatting
def format_time(minutes: float) -> str:
    """Reusable time formatting"""
    if minutes < 60:
        return f"{int(minutes)} phút"
    hours = int(minutes // 60)
    remaining = int(minutes % 60)
    return f"{hours} giờ {remaining} phút" if remaining else f"{hours} giờ"

# Use everywhere
print(format_time(45))    # "45 phút"
print(format_time(90))    # "1 giờ 30 phút"
print(format_time(120))   # "2 giờ"

# ✓ Reusable validation
def validate_numeric_field(value, field_name):
    """Reusable numeric validation"""
    if value is not None:
        try:
            float_value = float(value)
            if float_value < 0:
                return False, f"{field_name} cannot be negative"
            return True, None
        except (ValueError, TypeError):
            return False, f"{field_name} must be a number"
    return True, None

# Use for multiple fields
validate_numeric_field(data['prep_time'], 'prep_time')
validate_numeric_field(data['cook_time'], 'cook_time')
validate_numeric_field(data['quantity'], 'quantity')
```

---

## KISS Principle

**Principle**: Keep It Simple, Stupid - Simplicity should be a key goal.

### ✅ Good Example: Simple configuration

```python
# ✓ Simple, clear configuration
class Config:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DEFAULT_CSV_FILE = BASE_DIR / 'roll_cake_recipes_updated.csv'
    
    @classmethod
    def get_csv_path(cls, filename=None):
        return str(cls.DEFAULT_CSV_FILE if not filename else cls.BASE_DIR / filename)

# Easy to use
csv_path = Config.get_csv_path()
```

### ❌ Bad Example: Overcomplicated configuration

```python
# ✗ DON'T DO THIS - Overcomplicated
class Config:
    def __init__(self):
        self._config_manager = ConfigManager()
        self._env_loader = EnvironmentLoader()
        self._validator = ConfigValidator()
    
    def get_csv_path(self, filename=None, environment='production', 
                     override_dir=None, use_cache=True, 
                     validate=True, fallback_enabled=True):
        # 50 lines of complex logic...
        pass

# Too complex for simple task!
```

### ✅ Good Example: Simple CLI menu

```python
# ✓ Simple, clear menu
def print_menu():
    print("1. Xem tất cả công thức")
    print("2. Tìm kiếm theo ID")
    print("3. Lọc theo hương vị")
    print("0. Thoát")

choice = input("Chọn (0-3): ")
if choice == '1':
    display_all()
elif choice == '2':
    search_by_id()
# Clear and simple!
```

### ❌ Bad Example: Overcomplicated menu

```python
# ✗ DON'T DO THIS - Overcomplicated
class MenuSystem:
    def __init__(self):
        self.menu_factory = MenuFactory()
        self.command_processor = CommandProcessor()
        self.state_machine = StateMachine()
    
    def display_menu(self):
        menu_items = self.menu_factory.create_menu_hierarchy()
        for item in menu_items:
            decorated_item = self.decorator.decorate(item)
            self.renderer.render(decorated_item)
        # Too much for a simple menu!
```

### ✅ Good Example: Simple model

```python
# ✓ Simple, straightforward model
@dataclass
class Ingredient:
    name: str
    quantity: Optional[float] = None
    unit: Optional[str] = None
    notes: Optional[str] = None
    
    def __str__(self):
        return f"{self.quantity} {self.unit} {self.name}".strip()

# Easy to understand and use!
```

---

## Summary

### SOLID Benefits
- ✅ **Maintainable**: Easy to modify and extend
- ✅ **Testable**: Easy to test each component
- ✅ **Flexible**: Easy to swap implementations
- ✅ **Scalable**: Easy to add new features

### DRY Benefits
- ✅ **Less code**: Reduced code duplication
- ✅ **Easier maintenance**: Fix once, works everywhere
- ✅ **Consistency**: Same logic = same behavior

### KISS Benefits
- ✅ **Readable**: Easy to understand
- ✅ **Debuggable**: Easy to find bugs
- ✅ **Fast development**: Less complexity = faster coding

### Combined Result
The roll-cake-recipes system is now:
- ✅ Well-architected
- ✅ Easy to maintain
- ✅ Easy to extend
- ✅ Easy to test
- ✅ Easy to understand

Perfect foundation for long-term development! 🎉
