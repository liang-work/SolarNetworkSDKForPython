"""
Live streaming models for Solar Network Python SDK.

This module contains data classes for live streams and streaming operations.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum


class LiveStreamStatus(Enum):
    """Live stream status."""
    PENDING = 0
    ACTIVE = 1
    ENDED = 2
    ERROR = 3


class LiveStreamType(Enum):
    """Live stream type."""
    REGULAR = 0
    INTERACTIVE = 1


class LiveStreamVisibility(Enum):
    """Live stream visibility."""
    PUBLIC = 0
    UNLISTED = 1
    PRIVATE = 2


@dataclass
class LiveStream:
    """Live stream information."""
    id: str
    title: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None
    type: LiveStreamType = LiveStreamType.REGULAR
    visibility: LiveStreamVisibility = LiveStreamVisibility.PUBLIC
    status: LiveStreamStatus = LiveStreamStatus.PENDING
    room_name: str = ""
    ingress_id: Optional[str] = None
    ingress_stream_key: Optional[str] = None
    egress_id: Optional[str] = None
    hls_egress_id: Optional[str] = None
    hls_playlist_path: Optional[str] = None
    hls_started_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    viewer_count: int = 0
    peak_viewer_count: int = 0
    thumbnail: Optional[CloudFile] = None
    metadata: Optional[Dict[str, Any]] = None
    publisher_id: Optional[str] = None
    publisher: Optional[Publisher] = None
    resource_identifier: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None