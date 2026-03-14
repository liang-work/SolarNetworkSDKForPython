"""
Activity-related models for Solar Network Python SDK.

This module contains data classes for timeline events, check-ins,
fortunes, and presence activities.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any


@dataclass
class NotableDay:
    """Notable day information."""
    date: datetime
    local_name: str
    global_name: str
    country_code: Optional[str] = None
    localizable_key: Optional[str] = None
    holidays: List[int] = field(default_factory=list)


@dataclass
class TimelineEvent:
    """Timeline event information."""
    id: str
    type: str
    resource_identifier: str
    data: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None


@dataclass
class FortuneTip:
    """Fortune tip information."""
    is_positive: bool
    title: str
    content: str


@dataclass
class CheckInResult:
    """Check-in result information."""
    id: str
    level: int
    tips: List[FortuneTip]
    account_id: str
    account: Optional[Account] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None


@dataclass
class EventCalendarEntry:
    """Event calendar entry."""
    date: datetime
    check_in_result: Optional[CheckInResult] = None
    statuses: List[AccountStatus] = field(default_factory=list)


@dataclass
class PresenceActivity:
    """Presence activity information."""
    id: str
    type: int
    manual_id: Optional[str] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    caption: Optional[str] = None
    title_url: Optional[str] = None
    subtitle_url: Optional[str] = None
    small_image: Optional[str] = None
    large_image: Optional[str] = None
    meta: Dict[str, Any] = field(default_factory=dict)
    lease_minutes: int = 0
    lease_expires_at: datetime = field(default_factory=datetime.now)
    account_id: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None