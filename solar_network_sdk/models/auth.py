"""
Authentication-related models for Solar Network Python SDK.

This module contains data classes for authentication challenges, sessions,
and related security functionality.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any


@dataclass
class AppToken:
    """Application token model."""
    token: str


@dataclass
class GeoIpLocation:
    """Geographic IP location information."""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    country_code: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None


@dataclass
class AuthFactor:
    """Authentication factor information."""
    id: str
    type: int
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None
    expired_at: Optional[datetime] = None
    enabled_at: Optional[datetime] = None
    trustworthy: int = 0
    created_response: Optional[Dict[str, Any]] = None


@dataclass
class AccountConnection:
    """Account connection information."""
    id: str
    account_id: str
    provider: str
    provided_identifier: str
    meta: Dict[str, Any] = field(default_factory=dict)
    last_used_at: datetime = field(default_factory=datetime.now)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None


@dataclass
class AuthChallenge:
    """Authentication challenge information."""
    id: str
    expired_at: Optional[datetime] = None
    step_remain: int = 0
    step_total: int = 0
    failed_attempts: int = 0
    blacklist_factors: List[str] = field(default_factory=list)
    audiences: List[str] = field(default_factory=list)
    scopes: List[str] = field(default_factory=list)
    ip_address: str = ""
    user_agent: str = ""
    nonce: Optional[str] = None
    country_code: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    account_id: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None


@dataclass
class AuthSession:
    """Authentication session information."""
    id: str
    label: Optional[str] = None
    last_granted_at: datetime = field(default_factory=datetime.now)
    expired_at: Optional[datetime] = None
    audiences: List[str] = field(default_factory=list)
    scopes: List[str] = field(default_factory=list)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    location: Optional[GeoIpLocation] = None
    type: int = 0
    account_id: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None