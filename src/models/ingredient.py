"""
Ingredient domain model.
Single Responsibility Principle: Represents a single ingredient with its properties.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Ingredient:
    """Represents an ingredient used in a recipe."""
    
    name: str
    quantity: Optional[float] = None
    unit: Optional[str] = None
    notes: Optional[str] = None
    
    def __str__(self) -> str:
        """String representation of ingredient."""
        parts = [self.name]
        if self.quantity:
            parts.insert(0, f"{self.quantity}")
        if self.unit:
            parts.insert(1 if self.quantity else 0, self.unit)
        if self.notes:
            parts.append(f"({self.notes})")
        return " ".join(parts)
    
    def to_dict(self) -> dict:
        """Convert ingredient to dictionary."""
        return {
            'name': self.name,
            'quantity': self.quantity,
            'unit': self.unit,
            'notes': self.notes
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Ingredient':
        """Create ingredient from dictionary."""
        return cls(
            name=data.get('name', ''),
            quantity=data.get('quantity'),
            unit=data.get('unit'),
            notes=data.get('notes')
        )
