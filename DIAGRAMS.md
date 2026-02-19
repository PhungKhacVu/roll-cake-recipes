# Biểu đồ Kiến trúc Hệ thống

## Sơ đồ Tổng quan

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERACTION                          │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  PRESENTATION LAYER (CLI)                        │
│  ┌──────────┐                                                    │
│  │ cli.py   │  - Simple menu interface                          │
│  └──────────┘  - User input/output                              │
│                 - KISS: Keep it simple                           │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SERVICE LAYER                                 │
│  ┌─────────────────┐    ┌──────────────────┐                   │
│  │ RecipeService   │    │ RecipeAnalyzer   │                   │
│  │                 │    │                  │                   │
│  │ - get_all()     │    │ - count_by_*()   │                   │
│  │ - search()      │    │ - statistics()   │                   │
│  │ - filter()      │    │ - reports()      │                   │
│  └────────┬────────┘    └──────────────────┘                   │
│           │                                                      │
│  SRP: Single responsibility for business logic                  │
│  DRY: Reusable methods, no code duplication                     │
└───────────┼──────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  REPOSITORY LAYER                                │
│  ┌──────────────────┐                                           │
│  │   IRepository    │  ◄─── Interface (ISP, DIP)               │
│  │   (Interface)    │                                           │
│  └────────┬─────────┘                                           │
│           │                                                      │
│           │ implements                                           │
│           ▼                                                      │
│  ┌──────────────────────┐       ┌─────────────────────┐        │
│  │ CSVRecipeRepository  │       │ Future: Database    │        │
│  │                      │       │        API          │        │
│  │ - Load from CSV      │       │        JSON, etc.   │        │
│  │ - Parse data         │       │                     │        │
│  │ - Cache results      │       │ (OCP: Easy to add)  │        │
│  └──────────┬───────────┘       └─────────────────────┘        │
│             │                                                    │
│  LSP: All implementations interchangeable                       │
│  OCP: Open for extension, closed for modification               │
└─────────────┼────────────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DOMAIN LAYER                                │
│  ┌──────────┐         ┌──────────────┐                         │
│  │  Recipe  │         │  Ingredient  │                         │
│  │          │         │              │                         │
│  │ Fields:  │         │ Fields:      │                         │
│  │ - id     │  1:N    │ - name       │                         │
│  │ - name   ├────────►│ - quantity   │                         │
│  │ - flavor │         │ - unit       │                         │
│  │ - etc.   │         │ - notes      │                         │
│  └──────────┘         └──────────────┘                         │
│                                                                  │
│  SRP: Each model represents one entity                          │
│  Clean, simple domain objects                                   │
└──────────────────────────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       DATA SOURCE                                │
│  ┌──────────────────────────────────────────────────────┐      │
│  │     roll_cake_recipes_updated.csv                    │      │
│  │                                                       │      │
│  │  Recipe_ID, Recipe_Name, Description, Category,      │      │
│  │  Flavor_Profile, Difficulty_Level, ...               │      │
│  └──────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

## Sơ đồ Luồng dữ liệu (Data Flow)

```
User Input
    │
    ▼
┌─────────┐
│   CLI   │  1. User selects an option
└────┬────┘
     │
     ▼
┌─────────────┐
│   Service   │  2. Service processes request
└──────┬──────┘
       │
       ▼
┌───────────────┐
│  Repository   │  3. Repository fetches data
└───────┬───────┘
        │
        ▼
┌───────────────┐
│   CSV File    │  4. Parse CSV data
└───────┬───────┘
        │
        ▼
┌───────────────┐
│    Models     │  5. Create domain objects
└───────┬───────┘
        │
        ▼
┌───────────────┐
│   Service     │  6. Business logic processing
└───────┬───────┘
        │
        ▼
┌───────────────┐
│  Analytics    │  7. Optional: Analytics
└───────┬───────┘
        │
        ▼
┌───────────────┐
│  Formatters   │  8. Format for display
└───────┬───────┘
        │
        ▼
┌───────────────┐
│      CLI      │  9. Display to user
└───────────────┘
```

## Sơ đồ SOLID Principles

```
┌────────────────────────────────────────────────────────┐
│         SINGLE RESPONSIBILITY PRINCIPLE (SRP)          │
│                                                        │
│  Recipe         → Represents a recipe                  │
│  Ingredient     → Represents an ingredient             │
│  Repository     → Data access only                     │
│  Service        → Business logic only                  │
│  Analyzer       → Analytics only                       │
│  Formatter      → Formatting only                      │
│  Validator      → Validation only                      │
│                                                        │
│  Each class has ONE reason to change                   │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│          OPEN/CLOSED PRINCIPLE (OCP)                   │
│                                                        │
│  IRepository (Interface)                               │
│      ↑                                                 │
│      ├─── CSVRecipeRepository                         │
│      ├─── DatabaseRepository (future)                 │
│      ├─── APIRepository (future)                      │
│      └─── JSONRepository (future)                     │
│                                                        │
│  Open for extension, closed for modification           │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│       LISKOV SUBSTITUTION PRINCIPLE (LSP)              │
│                                                        │
│  RecipeService(repository: IRepository)                │
│                    ↑                                   │
│                    │                                   │
│      Any IRepository implementation can be used        │
│                    │                                   │
│      ┌─────────────┴──────────────┐                   │
│      │                             │                   │
│  CSVRepository            DatabaseRepository           │
│                                                        │
│  Can substitute any implementation                     │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│      INTERFACE SEGREGATION PRINCIPLE (ISP)             │
│                                                        │
│  IRepository (minimal interface)                       │
│    - get_all()                                         │
│    - get_by_id()                                       │
│    - filter()                                          │
│    - count()                                           │
│                                                        │
│  Only essential methods, no bloat                      │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│      DEPENDENCY INVERSION PRINCIPLE (DIP)              │
│                                                        │
│  High-level: RecipeService                             │
│       ↓ depends on ↓                                   │
│  Abstraction: IRepository                              │
│       ↑ implemented by ↑                               │
│  Low-level: CSVRecipeRepository                        │
│                                                        │
│  Depend on abstractions, not concretions               │
└────────────────────────────────────────────────────────┘
```

## Sơ đồ DRY Examples

```
❌ BEFORE (Without DRY):
─────────────────────────
count_by_flavor():
    for recipe in recipes:
        count flavor...
        
count_by_difficulty():
    for recipe in recipes:
        count difficulty...
        
count_by_category():
    for recipe in recipes:
        count category...

✅ AFTER (With DRY):
────────────────────
count_by_field(field_name):  ◄─── Generic method
    for recipe in recipes:
        count field...

count_by_flavor():
    return count_by_field('flavor')
    
count_by_difficulty():
    return count_by_field('difficulty')
    
count_by_category():
    return count_by_field('category')
```

## Mô hình Extensibility

```
Current Implementation
──────────────────────
┌──────────────────┐
│ CSVRepository    │
└──────────────────┘

Easy to Extend
──────────────
┌──────────────────┐
│ CSVRepository    │
└──────────────────┘
┌──────────────────┐
│ DatabaseRepo     │ ◄─── Add without changing existing
└──────────────────┘
┌──────────────────┐
│ APIRepository    │ ◄─── Add without changing existing
└──────────────────┘
┌──────────────────┐
│ JSONRepository   │ ◄─── Add without changing existing
└──────────────────┘

All work with RecipeService without modifications!
```

## Module Dependencies

```
┌────────────┐
│    CLI     │
└─────┬──────┘
      │
      ▼
┌────────────┐     ┌──────────────┐
│  Services  │────►│  Analytics   │
└─────┬──────┘     └──────────────┘
      │
      ▼
┌────────────┐     ┌──────────────┐
│Repositories│     │   Utilities   │
└─────┬──────┘     └──────────────┘
      │
      ▼
┌────────────┐     ┌──────────────┐
│   Models   │     │    Config    │
└────────────┘     └──────────────┘

Dependencies flow downward
No circular dependencies
Clean architecture
```
