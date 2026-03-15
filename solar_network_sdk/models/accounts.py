"""
Account-related models for Solar Network Python SDK.

This module contains data classes for account management, authentication,
and user-related functionality.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum

# Import missing types
from .wallets import WalletSubscriptionRef
from .activity import PresenceActivity
from .drive import CloudFile
from .auth import AuthSession


class AccountStatusType(Enum):
    """Account status types."""
    DEFAULT = 0
    BUSY = 1
    DO_NOT_DISTURB = 2
    INVISIBLE = 3


@dataclass
class ProfileLink:
    """Profile link model."""
    name: str
    url: str


@dataclass
class UsernameColor:
    """Username color configuration."""
    type: str = "plain"
    value: Optional[str] = None
    direction: Optional[str] = None
    colors: List[str] = field(default_factory=list)


@dataclass
class AccountProfile:
    """Account profile information."""
    id: str
    first_name: str = ""
    middle_name: str = ""
    last_name: str = ""
    bio: str = ""
    gender: str = ""
    pronouns: str = ""
    location: str = ""
    time_zone: str = ""
    birthday: Optional[datetime] = None
    links: List[ProfileLink] = field(default_factory=list)
    last_seen_at: Optional[datetime] = None
    active_badge: Optional[AccountBadge] = None
    experience: int = 0
    level: int = 0
    social_credits: float = 100.0
    social_credits_level: int = 0
    leveling_progress: float = 0.0
    picture: Optional[CloudFile] = None
    background: Optional[CloudFile] = None
    verification: Optional[VerificationMark] = None
    username_color: Optional[UsernameColor] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None


@dataclass
class AccountStatus:
    """Account status information."""
    id: str
    attitude: int
    is_online: bool
    is_customized: bool
    type: int = AccountStatusType.DEFAULT.value
    label: str = ""
    symbol: Optional[str] = None
    meta: Dict[str, Any] = field(default_factory=dict)
    cleared_at: Optional[datetime] = None
    app_identifier: Optional[str] = None
    is_automated: bool = False
    account_id: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None

    @property
    def is_invisible(self) -> bool:
        return self.type == AccountStatusType.INVISIBLE.value

    @property
    def is_not_disturb(self) -> bool:
        return self.type == AccountStatusType.DO_NOT_DISTURB.value

    @property
    def is_busy(self) -> bool:
        return self.type == AccountStatusType.BUSY.value


@dataclass
class AccountBadge:
    """Account badge information."""
    id: str
    type: str
    label: Optional[str] = None
    caption: Optional[str] = None
    meta: Dict[str, Any] = field(default_factory=dict)
    expired_at: Optional[datetime] = None
    account_id: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    activated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


@dataclass
class ContactMethod:
    """Contact method information."""
    id: str
    type: int
    verified_at: Optional[datetime] = None
    is_primary: bool = False
    is_public: bool = False
    content: str = ""
    account_id: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None


@dataclass
class Notification:
    """Notification information."""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None
    id: str = ""
    topic: str = ""
    title: str = ""
    subtitle: str = ""
    content: str = ""
    meta: Dict[str, Any] = field(default_factory=dict)
    priority: int = 0
    viewed_at: Optional[datetime] = None
    account_id: str = ""


@dataclass
class VerificationMark:
    """Account verification mark."""
    type: int
    title: Optional[str] = None
    description: Optional[str] = None
    verified_by: Optional[str] = None


@dataclass
class AuthDevice:
    """Authentication device information."""
    id: str
    device_id: str
    device_name: str
    device_label: Optional[str] = None
    account_id: str = ""
    platform: int = 0
    is_current: bool = False


@dataclass
class AuthDeviceWithSession(AuthDevice):
    """Authentication device with sessions."""
    sessions: List[AuthSession] = field(default_factory=list)


@dataclass
class ExperienceRecord:
    """Experience record information."""
    id: str
    delta: int
    reason_type: str
    reason: str
    bonus_multiplier: float = 1.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None


@dataclass
class SocialCreditRecord:
    """Social credit record information."""
    id: str
    delta: float
    reason_type: str
    reason: str
    expired_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None


@dataclass
class FriendOverviewItem:
    """Friend overview item."""
    account: Account
    status: AccountStatus
    activities: List[PresenceActivity]


@dataclass
class Account:
    """Main account model."""
    id: str
    name: str
    nick: str
    language: str
    profile: AccountProfile
    region: str = ""
    is_superuser: bool = False
    automated_id: Optional[str] = None
    perk_subscription: Optional[WalletSubscriptionRef] = None
    badges: List[AccountBadge] = field(default_factory=list)
    contacts: List[ContactMethod] = field(default_factory=list)
    activated_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None
