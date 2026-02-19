"""
Base repository interface.
Interface Segregation Principle: Define minimal interface for data access.
Open/Closed Principle: Open for extension, closed for modification.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any


class IRepository(ABC):
    """
    Base interface for data repositories.
    Following Interface Segregation Principle - only essential methods.
    """
    
    @abstractmethod
    def get_all(self) -> List[Any]:
        """Get all items from repository."""
        pass
    
    @abstractmethod
    def get_by_id(self, item_id: str) -> Optional[Any]:
        """Get item by ID."""
        pass
    
    @abstractmethod
    def filter(self, criteria: Dict[str, Any]) -> List[Any]:
        """Filter items by criteria."""
        pass
    
    @abstractmethod
    def count(self) -> int:
        """Count total items in repository."""
        pass
