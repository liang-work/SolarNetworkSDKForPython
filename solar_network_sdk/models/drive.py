"""
Drive-related models for Solar Network Python SDK.

This module contains data classes for cloud files, file pools,
folders, and drive operations.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from enum import Enum


class UniversalFileType(Enum):
    """Universal file types."""
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    FILE = "file"


@dataclass
class UniversalFile:
    """Universal file wrapper."""
    data: Union[CloudFile, Any]
    type: UniversalFileType
    is_link: bool = False
    display_name: Optional[str] = None

    @property
    def is_on_cloud(self) -> bool:
        return isinstance(self.data, CloudFile)

    @property
    def is_on_device(self) -> bool:
        return not self.is_on_cloud


@dataclass
class FileReplica:
    """File replica information."""
    id: str
    object_id: str
    pool_id: str
    pool: Optional[FilePool] = None
    storage_id: str = ""
    status: int = 0
    is_primary: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None


@dataclass
class CloudFileObject:
    """Cloud file object information."""
    id: str
    size: int = 0
    meta: Optional[Dict[str, Any]] = None
    mime_type: Optional[str] = None
    hash: Optional[str] = None
    has_compression: bool = False
    has_thumbnail: bool = False
    file_replicas: List[FileReplica] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None


@dataclass
class CloudFile:
    """Cloud file information."""
    id: str
    name: str = ""
    description: Optional[str] = None
    file_meta: Optional[Dict[str, Any]] = None
    user_meta: Optional[Dict[str, Any]] = None
    sensitive_marks: List[int] = field(default_factory=list)
    mime_type: Optional[str] = None
    hash: Optional[str] = None
    size: int = 0
    uploaded_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None
    url: Optional[str] = None


@dataclass
class CloudFileIndex:
    """Cloud file index information."""
    id: str
    path: str = ""
    file_id: str = ""
    file: Optional[CloudFile] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None


@dataclass
class FilePool:
    """File pool information."""
    id: str
    name: str = ""
    description: Optional[str] = None
    storage_config: Optional[Dict[str, Any]] = None
    billing_config: Optional[Dict[str, Any]] = None
    policy_config: Optional[Dict[str, Any]] = None
    is_hidden: Optional[bool] = None
    account_id: Optional[str] = None
    resource_identifier: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


@dataclass
class CloudFolder:
    """Cloud folder information."""
    id: str
    name: str = ""
    parent_folder_id: Optional[str] = None
    account_id: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class FileListItem:
    """File list item."""
    file_index: Optional[CloudFileIndex] = None
    folder_name: Optional[str] = None
    unindexed_file: Optional[CloudFile] = None


@dataclass
class DriveTask:
    """Drive task information."""
    id: str
    task_id: str = ""
    file_name: str = ""
    content_type: str = ""
    file_size: int = 0
    uploaded_bytes: int = 0
    total_chunks: int = 0
    uploaded_chunks: int = 0
    status: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    type: str = "FileUpload"  # Task type
    transmission_progress: Optional[float] = None  # Local file upload progress (0.0-1.0)
    error_message: Optional[str] = None
    status_message: Optional[str] = None
    result: Optional[CloudFile] = None
    pool_id: Optional[str] = None
    bundle_id: Optional[str] = None
    encrypt_password: Optional[str] = None
    expired_at: Optional[str] = None

    @property
    def progress(self) -> float:
        """Get upload progress."""
        return self.total_chunks > 0 and self.uploaded_chunks / self.total_chunks or 0.0

    @property
    def estimated_time_remaining(self) -> datetime:
        """Get estimated time remaining."""
        if self.uploaded_bytes == 0 or self.file_size == 0:
            return datetime.now()
        
        remaining_bytes = self.file_size - self.uploaded_bytes
        upload_rate = self.uploaded_bytes / (
            self.created_at - datetime.now()
        ).total_seconds()
        
        if upload_rate == 0:
            return datetime.now()
        
        return datetime.now().replace(
            second=int(remaining_bytes / upload_rate)
        )