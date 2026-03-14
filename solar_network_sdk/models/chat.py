"""
Chat-related models for Solar Network Python SDK.

This module contains data classes for chat rooms, messages,
reactions, and real-time communication.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any


@dataclass
class ChatRoom:
    """Chat room information."""
    id: str
    name: Optional[str] = None
    description: Optional[str] = None
    type: int = 0
    encryption_mode: int = 0
    is_public: bool = False
    is_community: bool = False
    picture: Optional[CloudFile] = None
    background: Optional[CloudFile] = None
    realm_id: Optional[str] = None
    account_id: Optional[str] = None
    realm: Optional[Realm] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None
    members: Optional[List[ChatMember]] = None
    is_pinned: bool = False


@dataclass
class ChatMessage:
    """Chat message information."""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None
    id: str = ""
    type: str = "text"
    content: Optional[str] = None
    nonce: Optional[str] = None
    meta: Dict[str, Any] = field(default_factory=dict)
    members_mentioned: List[str] = field(default_factory=list)
    edited_at: Optional[datetime] = None
    attachments: List[CloudFile] = field(default_factory=list)
    reactions: List[ChatReaction] = field(default_factory=list)
    replied_message_id: Optional[str] = None
    forwarded_message_id: Optional[str] = None
    sender_id: str = ""
    sender: Optional[ChatMember] = None
    chat_room_id: str = ""


@dataclass
class ChatReaction:
    """Chat reaction information."""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None
    id: str = ""
    message_id: str = ""
    sender_id: str = ""
    sender: Optional[ChatMember] = None
    symbol: str = ""
    attitude: int = 0


@dataclass
class ChatMember:
    """Chat member information."""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None
    id: str = ""
    chat_room_id: str = ""
    chat_room: Optional[ChatRoom] = None
    account_id: str = ""
    account: Optional[Account] = None
    nick: Optional[str] = None
    notify: int = 0
    joined_at: Optional[datetime] = None
    break_until: Optional[datetime] = None
    timeout_until: Optional[datetime] = None
    status: Optional[AccountStatus] = None
    last_typed: Optional[datetime] = None


@dataclass
class ChatSummary:
    """Chat summary information."""
    unread_count: int = 0
    last_message: Optional[ChatMessage] = None


@dataclass
class ChatOnlineAccount:
    """Chat online account information."""
    id: str = ""
    name: str = ""
    nick: str = ""


@dataclass
class ChatOnlineStatus:
    """Chat online status information."""
    online_count: int = 0
    direct_message_status: Optional[AccountStatus] = None
    online_user_names: List[str] = field(default_factory=list)
    online_accounts: List[ChatOnlineAccount] = field(default_factory=list)


@dataclass
class MessageSyncResponse:
    """Message sync response."""
    messages: List[ChatMessage] = field(default_factory=list)
    total_count: int = 0
    current_timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class CallParticipant:
    """Call participant information."""
    identity: str = ""
    name: str = ""
    joined_at: datetime = field(default_factory=datetime.now)


@dataclass
class ChatRealtimeJoinResponse:
    """Chat real-time join response."""
    provider: str = ""
    endpoint: str = ""
    token: str = ""
    call_id: str = ""
    room_name: str = ""
    is_admin: bool = False
    participants: List[CallParticipant] = field(default_factory=list)


@dataclass
class RealtimeCall:
    """Real-time call information."""
    id: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    sender_id: str = ""
    sender: Optional[ChatMember] = None
    room_id: str = ""
    room: Optional[ChatRoom] = None
    upstream_config: Dict[str, Any] = field(default_factory=dict)
    provider_name: Optional[str] = None
    session_id: Optional[str] = None