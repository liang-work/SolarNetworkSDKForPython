"""
Pagination utilities for Solar Network Python SDK.

This module provides pagination support for API responses.
"""

from __future__ import annotations
from typing import List, Optional, TypeVar, Generic, Callable, Awaitable
from dataclasses import dataclass, field
from abc import ABC, abstractmethod


T = TypeVar('T')


@dataclass
class PaginationState(Generic[T]):
    """Pagination state information."""
    items: List[T] = field(default_factory=list)
    is_loading: bool = False
    is_reloading: bool = False
    total_count: Optional[int] = None
    has_more: bool = True
    cursor: Optional[str] = None


class PaginationController(ABC, Generic[T]):
    """Abstract pagination controller."""
    
    @property
    @abstractmethod
    def total_count(self) -> Optional[int]:
        """Get the total count of items."""
        pass
    
    @property
    @abstractmethod
    def fetched_count(self) -> int:
        """Get the number of fetched items."""
        pass
    
    @property
    @abstractmethod
    def fetched_all(self) -> bool:
        """Check if all items have been fetched."""
        pass
    
    @property
    @abstractmethod
    def is_loading(self) -> bool:
        """Check if currently loading."""
        pass
    
    @property
    @abstractmethod
    def is_reloading(self) -> bool:
        """Check if currently reloading."""
        pass
    
    @property
    @abstractmethod
    def has_more(self) -> bool:
        """Check if there are more items to fetch."""
        pass
    
    @has_more.setter
    @abstractmethod
    def has_more(self, value: bool) -> None:
        """Set the has_more flag."""
        pass
    
    @property
    @abstractmethod
    def cursor(self) -> Optional[str]:
        """Get the current cursor."""
        pass
    
    @cursor.setter
    @abstractmethod
    def cursor(self, value: Optional[str]) -> None:
        """Set the current cursor."""
        pass
    
    @abstractmethod
    async def fetch(self) -> List[T]:
        """Fetch the next page of items."""
        pass
    
    @abstractmethod
    async def refresh(self) -> None:
        """Refresh the pagination state."""
        pass
    
    @abstractmethod
    async def fetch_further(self) -> None:
        """Fetch more items."""
        pass


class AsyncPaginationController(PaginationController[T]):
    """Asynchronous pagination controller."""
    
    def __init__(self, fetch_func: Callable[[], Awaitable[List[T]]]):
        """Initialize the pagination controller.
        
        Args:
            fetch_func: Function to fetch items
        """
        self._fetch_func = fetch_func
        self._state = PaginationState[T]()
        self._total_count: Optional[int] = None
    
    @property
    def total_count(self) -> Optional[int]:
        """Get the total count of items."""
        return self._total_count
    
    @property
    def fetched_count(self) -> int:
        """Get the number of fetched items."""
        return 0 if self._state.is_reloading else len(self._state.items)
    
    @property
    def fetched_all(self) -> bool:
        """Check if all items have been fetched."""
        return not self._state.has_more or (
            self._total_count is not None and 
            self.fetched_count >= self._total_count
        )
    
    @property
    def is_loading(self) -> bool:
        """Check if currently loading."""
        return self._state.is_loading
    
    @property
    def is_reloading(self) -> bool:
        """Check if currently reloading."""
        return self._state.is_reloading
    
    @property
    def has_more(self) -> bool:
        """Check if there are more items to fetch."""
        return self._state.has_more
    
    @has_more.setter
    def has_more(self, value: bool) -> None:
        """Set the has_more flag."""
        self._state.has_more = value
    
    @property
    def cursor(self) -> Optional[str]:
        """Get the current cursor."""
        return self._state.cursor
    
    @cursor.setter
    def cursor(self, value: Optional[str]) -> None:
        """Set the current cursor."""
        self._state.cursor = value
    
    async def fetch(self) -> List[T]:
        """Fetch the next page of items."""
        return await self._fetch_func()
    
    async def refresh(self) -> None:
        """Refresh the pagination state."""
        self._state = PaginationState(
            items=[],
            is_loading=True,
            is_reloading=True,
            total_count=None,
            has_more=True,
            cursor=None,
        )
        
        new_items = await self.fetch()
        
        self._state = PaginationState(
            items=new_items,
            is_loading=False,
            is_reloading=False,
            total_count=self._total_count,
            has_more=self._state.has_more,
            cursor=self._state.cursor,
        )
    
    async def fetch_further(self) -> None:
        """Fetch more items."""
        if self.fetched_all or self.is_loading:
            return
        
        self._state.is_loading = True
        
        new_items = await self.fetch()
        
        self._state = PaginationState(
            items=self._state.items + new_items,
            is_loading=False,
            is_reloading=self._state.is_reloading,
            total_count=self._total_count,
            has_more=self._state.has_more,
            cursor=self._state.cursor,
        )


class PaginationFiltered(Generic[T]):
    """Pagination with filtering support."""
    
    def __init__(self, controller: PaginationController[T]):
        """Initialize with a pagination controller.
        
        Args:
            controller: The pagination controller
        """
        self._controller = controller
        self._current_filter: Optional[dict] = None
    
    @property
    def current_filter(self) -> Optional[dict]:
        """Get the current filter."""
        return self._current_filter
    
    @current_filter.setter
    def current_filter(self, value: Optional[dict]) -> None:
        """Set the current filter."""
        self._current_filter = value
    
    async def apply_filter(self, filter_params: dict) -> None:
        """Apply a filter and refresh the data.
        
        Args:
            filter_params: The filter parameters
        """
        if self._current_filter == filter_params:
            return
        
        self._state = PaginationState(
            items=[],
            is_loading=True,
            is_reloading=True,
            total_count=None,
            has_more=True,
            cursor=None,
        )
        
        self._current_filter = filter_params
        
        new_items = await self._controller.fetch()
        
        self._state = PaginationState(
            items=new_items,
            is_loading=False,
            is_reloading=False,
            total_count=self._controller.total_count,
            has_more=self._controller.has_more,
            cursor=self._controller.cursor,
        )