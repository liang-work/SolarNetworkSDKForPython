"""
ActivityPub-related models for Solar Network Python SDK.

This module contains data classes for ActivityPub federation,
instances, users, and actors.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any


@dataclass
class ActivityPubInstance:
    """ActivityPub instance information."""
    id: str
    domain: str
    name: Optional[str] = None
    description: Optional[str] = None
    software: Optional[str] = None
    version: Optional[str] = None
    icon_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    contact_email: Optional[str] = None
    contact_account_username: Optional[str] = None
    active_users: Optional[int] = None
    is_blocked: bool = False
    is_silenced: bool = False
    block_reason: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    last_fetched_at: Optional[datetime] = None
    last_activity_at: Optional[datetime] = None
    metadata_fetched_at: Optional[datetime] = None


@dataclass
class ActivityPubUser:
    """ActivityPub user information."""
    actor_uri: str
    username: str
    display_name: str
    bio: str
    avatar_url: str
    followed_at: datetime = field(default_factory=datetime.now)
    is_local: bool = False
    instance_domain: str = ""


@dataclass
class ActivityPubActor:
    """ActivityPub actor information."""
    id: str
    uri: str
    type: str = ""
    display_name: Optional[str] = None
    username: Optional[str] = None
    summary: Optional[str] = None
    inbox_uri: Optional[str] = None
    outbox_uri: Optional[str] = None
    followers_uri: Optional[str] = None
    following_uri: Optional[str] = None
    featured_uri: Optional[str] = None
    avatar_url: Optional[str] = None
    header_url: Optional[str] = None
    public_key_id: Optional[str] = None
    public_key: Optional[str] = None
    is_bot: bool = False
    is_locked: bool = False
    discoverable: bool = True
    manually_approves_followers: bool = False
    endpoints: Optional[Dict[str, Any]] = None
    public_key_data: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    last_fetched_at: Optional[datetime] = None
    last_activity_at: Optional[datetime] = None
    instance: Optional[ActivityPubInstance] = None
    instance_id: str = ""
    is_following: Optional[bool] = None


@dataclass
class ActivityPubFollowResponse:
    """ActivityPub follow response."""
    success: bool
    message: str


@dataclass
class ActorStatusResponse:
    """Actor status response."""
    enabled: bool
    follower_count: int = 0
    actor: Optional[ActivityPubActor] = None
    actor_uri: Optional[str] = None