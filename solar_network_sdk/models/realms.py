"""
Realm-related models for Solar Network Python SDK.

This module contains data classes for realms and realm members.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any


@dataclass
class Realm:
    """Realm information."""
    id: str
    slug: str
    name: str = ""
    description: str = ""
    verified_as: Optional[str] = None
    verified_at: Optional[datetime] = None
    is_community: bool = False
    is_public: bool = False
    picture: Optional[CloudFile] = None
    background: Optional[CloudFile] = None
    account_id: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None


@dataclass
class RealmMember:
    """Realm member information."""
    realm_id: str = ""
    realm: Optional[Realm] = None
    account_id: str = ""
    account: Optional[Account] = None
    role: int = 0
    joined_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None
    status: Optional[AccountStatus] = None