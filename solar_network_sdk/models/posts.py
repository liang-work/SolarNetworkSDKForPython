"""
Post-related models for Solar Network Python SDK.

This module contains data classes for posts, publishers, polls,
tags, categories, and post-related operations.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from enum import Enum


class PostEmbedViewRenderer(Enum):
    """Post embed view renderer."""
    WEB_VIEW = 0


class SnPollQuestionType(Enum):
    """Poll question types."""
    SINGLE_CHOICE = 0
    MULTIPLE_CHOICE = 1
    YES_NO = 2
    RATING = 3
    FREE_TEXT = 4


@dataclass
class PostEmbedView:
    """Post embed view information."""
    uri: str = ""
    aspect_ratio: Optional[float] = None
    renderer: PostEmbedViewRenderer = PostEmbedViewRenderer.WEB_VIEW


@dataclass
class PostAward:
    """Post award information."""
    id: str = ""
    amount: float = 0.0
    attitude: int = 0
    message: Optional[str] = None
    post_id: str = ""
    account_id: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


@dataclass
class PostReaction:
    """Post reaction information."""
    id: str = ""
    symbol: str = ""
    attitude: int = 0
    post_id: str = ""
    sender_id: str = ""
    sender: Optional[ChatMember] = None
    account_id: str = ""
    account: Optional[Account] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None


@dataclass
class PostFeaturedRecord:
    """Post featured record information."""
    id: str = ""
    post_id: str = ""
    featured_at: Optional[datetime] = None
    social_credits: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None


@dataclass
class PostWithStats:
    """Post with statistics."""
    post: Post = field(default_factory=lambda: Post())
    user_answer: Optional[PollAnswer] = None
    stats: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PollWithStats:
    """Poll with statistics."""
    poll: Poll = field(default_factory=lambda: Poll())
    user_answer: Optional[PollAnswer] = None
    stats: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Poll:
    """Poll information."""
    id: str = ""
    questions: List[PollQuestion] = field(default_factory=list)
    title: Optional[str] = None
    description: Optional[str] = None
    ended_at: Optional[datetime] = None
    publisher_id: str = ""
    publisher: Optional[Publisher] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None


@dataclass
class PollQuestion:
    """Poll question information."""
    id: str = ""
    type: SnPollQuestionType = SnPollQuestionType.SINGLE_CHOICE
    options: Optional[List[PollOption]] = None
    title: str = ""
    description: Optional[str] = None
    order: int = 0
    is_required: bool = False


@dataclass
class PollOption:
    """Poll option information."""
    id: str = ""
    label: str = ""
    description: Optional[str] = None
    order: int = 0


@dataclass
class PollAnswer:
    """Poll answer information."""
    id: str = ""
    answer: Dict[str, Any] = field(default_factory=dict)
    account_id: str = ""
    poll_id: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None
    account: Optional[Account] = None


@dataclass
class PostTag:
    """Post tag information."""
    id: str = ""
    slug: str = ""
    name: Optional[str] = None
    posts: List[Post] = field(default_factory=list)
    usage: int = 0


@dataclass
class CategorySubscription:
    """Category subscription information."""
    id: str = ""
    account_id: str = ""
    category_id: Optional[str] = None
    category: Optional[PostCategory] = None
    tag_id: Optional[str] = None
    tag: Optional[PostTag] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None


@dataclass
class PostCategory:
    """Post category information."""
    id: str = ""
    slug: str = ""
    name: Optional[str] = None
    posts: List[Post] = field(default_factory=list)
    usage: int = 0

    @property
    def category_translation_key(self) -> str:
        """Get category translation key."""
        capitalized_slug = self.slug.replace('_', ' ').title().replace(' ', '')
        return f'postCategory{capitalized_slug}'


@dataclass
class ScrappedLink:
    """Scrapped link information."""
    type: str = ""
    url: str = ""
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    favicon_url: Optional[str] = None
    site_name: Optional[str] = None
    content_type: Optional[str] = None
    author: Optional[str] = None
    published_date: Optional[datetime] = None


@dataclass
class Heatmap:
    """Heatmap information."""
    unit: str = ""
    period_start: datetime = field(default_factory=datetime.now)
    period_end: datetime = field(default_factory=datetime.now)
    items: List[HeatmapItem] = field(default_factory=list)


@dataclass
class HeatmapItem:
    """Heatmap item information."""
    date: datetime = field(default_factory=datetime.now)
    count: int = 0


@dataclass
class ReactInfo:
    """Reaction information."""
    icon: str = ""
    attitude: int = 0

    @staticmethod
    def get_translation_key(template_key: str) -> str:
        """Get translation key for reaction."""
        parts = template_key.split('_')
        camel_case = ''.join(part.capitalize() for part in parts)
        return f'reaction{camel_case}'


@dataclass
class PublisherStats:
    """Publisher statistics."""
    posts_created: int = 0
    sticker_packs_created: int = 0
    stickers_created: int = 0
    upvote_received: int = 0
    downvote_received: int = 0


@dataclass
class PublisherSubscription:
    """Publisher subscription information."""
    account_id: str = ""
    publisher_id: str = ""
    publisher: Publisher = field(default_factory=lambda: Publisher())


@dataclass
class Post:
    """Post information."""
    id: str = ""
    title: Optional[str] = None
    description: Optional[str] = None
    language: Optional[str] = None
    edited_at: Optional[datetime] = None
    drafted_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    visibility: int = 0
    content: Optional[str] = None
    slug: Optional[str] = None
    type: int = 0
    meta: Optional[Dict[str, Any]] = None
    embed_view: Optional[PostEmbedView] = None
    views_unique: int = 0
    views_total: int = 0
    upvotes: int = 0
    downvotes: int = 0
    replies_count: int = 0
    threaded_replies_count: int = 0
    debug_rank: Optional[float] = None
    awarded_score: int = 0
    pin_mode: Optional[int] = None
    threaded_post_id: Optional[str] = None
    threaded_post: Optional[Post] = None
    replied_post_id: Optional[str] = None
    replied_post: Optional[Post] = None
    forwarded_post_id: Optional[str] = None
    forwarded_post: Optional[Post] = None
    realm_id: Optional[str] = None
    realm: Optional[Realm] = None
    publisher_id: Optional[str] = None
    publisher: Optional[Publisher] = None
    actorid: Optional[str] = None
    actor: Optional[ActivityPubActor] = None
    fediverse_uri: Optional[str] = None
    fediverse_type: Optional[int] = None
    content_type: int = 0
    attachments: List[CloudFile] = field(default_factory=list)
    reactions_count: Dict[str, int] = field(default_factory=dict)
    reactions_made: Dict[str, bool] = field(default_factory=dict)
    reactions: List[Dict[str, Any]] = field(default_factory=list)
    tags: List[PostTag] = field(default_factory=list)
    categories: List[PostCategory] = field(default_factory=list)
    collections: List[Dict[str, Any]] = field(default_factory=list)
    featured_records: List[PostFeaturedRecord] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    replied_gone: bool = False
    forwarded_gone: bool = False
    is_truncated: bool = False


@dataclass
class Publisher:
    """Publisher information."""
    id: str = ""
    type: int = 0
    name: str = ""
    nick: str = ""
    bio: str = ""
    picture: Optional[CloudFile] = None
    background: Optional[CloudFile] = None
    account: Optional[Account] = None
    account_id: Optional[str] = None
    realm_id: Optional[str] = None
    verification: Optional[VerificationMark] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None