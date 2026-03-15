"""
Main client for Solar Network Python SDK.

This module provides the SolarNetworkClient class for interacting
with the Solar Network API.
"""

from __future__ import annotations
from typing import Optional, Dict, Any, List, Union, TypeVar, Generic
from datetime import datetime
import requests
from .auth import WebAuthClient, WebAuthResult
from .models import (
    # Account models
    Account, AccountProfile, AccountStatus, AccountBadge, ContactMethod,
    Notification, VerificationMark, AuthDevice, AuthDeviceWithSession,
    ExperienceRecord, SocialCreditRecord, FriendOverviewItem,
    
    # Auth models
    AuthChallenge, AuthSession, AppToken, GeoIpLocation, AuthFactor,
    AccountConnection,
    
    # Activity models
    NotableDay, TimelineEvent, CheckInResult, FortuneTip, EventCalendarEntry,
    PresenceActivity,
    
    # ActivityPub models
    ActivityPubInstance, ActivityPubUser, ActivityPubActor,
    ActivityPubFollowResponse, ActorStatusResponse,
    
    # Chat models
    ChatRoom, ChatMessage, ChatReaction, ChatMember, ChatSummary,
    ChatOnlineAccount, ChatOnlineStatus, MessageSyncResponse,
    ChatRealtimeJoinResponse, CallParticipant, RealtimeCall,
    
    # Drive models
    FileReplica, CloudFileObject, CloudFile, CloudFileIndex,
    FilePool, CloudFolder, FileListItem, DriveTask, UniversalFile,
    UniversalFileType,
    
    # Live models
    LiveStream, LiveStreamStatus, LiveStreamType, LiveStreamVisibility,
    
    # Post models
    Post, Publisher, PublisherStats, PublisherSubscription, ReactInfo,
    PostEmbedView, PostEmbedViewRenderer, PostAward, PostReaction,
    PostFeaturedRecord, PostWithStats, PollWithStats, Poll, PollQuestion,
    PollOption, SnPollQuestionType, PollAnswer, PostTag, CategorySubscription,
    PostCategory, ScrappedLink, Heatmap, HeatmapItem,
    
    # Realm models
    Realm, RealmMember,
    
    # Wallet models
    Wallet, WalletStats, WalletPocket, Transaction, WalletSubscription,
    WalletSubscriptionRef, WalletOrder, WalletGift, WalletFund,
    WalletFundRecipient, LotteryTicket, LotteryRecord,
)


class SolarNetworkClient:
    """Main client for Solar Network API.
    
    Provides methods for authentication, account management, and content operations.
    """
    
    def __init__(
        self,
        server_url: str = "https://api.solian.app",
        token: Optional[str] = None,
        timeout: int = 30
    ):
        """Initialize the SolarNetworkClient.
        
        Args:
            server_url: The Solar Network API server URL
            token: Optional authentication token
            timeout: Request timeout in seconds
        """
        self.server_url = server_url.rstrip('/')
        self.token = token
        self.timeout = timeout
        self._session = requests.Session()
        
        if self.token:
            self._session.headers.update({'Authorization': f'Bearer {self.token}'})
    
    def set_token(self, token: str) -> None:
        """Set the authentication token.
        
        Args:
            token: The authentication token
        """
        self.token = token
        self._session.headers.update({'Authorization': f'Bearer {self.token}'})
    
    def clear_token(self) -> None:
        """Clear the authentication token."""
        self.token = None
        if 'Authorization' in self._session.headers:
            del self._session.headers['Authorization']
    
    def get_web_auth_client(
        self,
        base_url: str = "http://127.0.0.1",
        default_port: int = 40000,
        web_url: str = "https://app.solian.fr"
    ) -> WebAuthClient:
        """Get a WebAuthClient instance.
        
        Args:
            base_url: The local server base URL
            default_port: The default port to connect to
            web_url: The Solar Network web URL for auth redirects
            
        Returns:
            A WebAuthClient instance
        """
        return WebAuthClient(
            base_url=base_url,
            default_port=default_port,
            web_url=web_url
        )
    
    # Account Management
    def get_account(self) -> Account:
        """Get the current account information.
        
        Returns:
            Account information
        """
        response = self._get('/me')
        return Account(**response)
    
    def update_account(self, **kwargs) -> Account:
        """Update account information.
        
        Args:
            **kwargs: Account fields to update
            
        Returns:
            Updated account information
        """
        response = self._patch('/me', json=kwargs)
        return Account(**response)
    
    def get_account_profile(self) -> AccountProfile:
        """Get the current account profile.
        
        Returns:
            Account profile information
        """
        response = self._get('/me/profile')
        return AccountProfile(**response)
    
    def update_account_profile(self, **kwargs) -> AccountProfile:
        """Update account profile information.
        
        Args:
            **kwargs: Profile fields to update
            
        Returns:
            Updated profile information
        """
        response = self._patch('/me/profile', json=kwargs)
        return AccountProfile(**response)
    
    def get_account_status(self) -> AccountStatus:
        """Get the current account status.
        
        Returns:
            Account status information
        """
        response = self._get('/me/status')
        return AccountStatus(**response)
    
    def set_account_status(
        self,
        attitude: int,
        type: int = 0,
        label: str = "",
        symbol: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None
    ) -> AccountStatus:
        """Set account status.
        
        Args:
            attitude: Status attitude
            type: Status type
            label: Status label
            symbol: Optional status symbol
            meta: Optional status metadata
            
        Returns:
            Updated status information
        """
        payload = {
            'attitude': attitude,
            'type': type,
            'label': label,
        }
        if symbol:
            payload['symbol'] = symbol
        if meta:
            payload['meta'] = meta
        
        response = self._post('/me/status', json=payload)
        return AccountStatus(**response)
    
    def clear_account_status(self) -> None:
        """Clear account status."""
        self._delete('/me/status')
    
    # Activity Operations
    def check_in(self) -> CheckInResult:
        """Perform a daily check-in.
        
        Returns:
            Check-in result
        """
        response = self._post('/me/checkin')
        return CheckInResult(**response)
    
    def get_notable_days(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[NotableDay]:
        """Get notable days.
        
        Args:
            start_date: Start date for the range
            end_date: End date for the range
            
        Returns:
            List of notable days
        """
        params = {}
        if start_date:
            params['start_date'] = start_date.isoformat()
        if end_date:
            params['end_date'] = end_date.isoformat()
        
        response = self._get('/me/notable-days', params=params)
        return [NotableDay(**day) for day in response]
    
    def get_timeline_events(
        self,
        limit: int = 20,
        offset: int = 0,
        types: Optional[List[str]] = None
    ) -> List[TimelineEvent]:
        """Get timeline events.
        
        Args:
            limit: Number of events to return
            offset: Offset for pagination
            types: Optional list of event types to filter
            
        Returns:
            List of timeline events
        """
        params = {
            'limit': limit,
            'offset': offset,
        }
        if types:
            params['types'] = ','.join(types)
        
        response = self._get('/me/timeline', params=params)
        return [TimelineEvent(**event) for event in response]
    
    # Chat Operations
    def get_chat_rooms(
        self,
        limit: int = 20,
        offset: int = 0,
        types: Optional[List[int]] = None
    ) -> List[ChatRoom]:
        """Get chat rooms.
        
        Args:
            limit: Number of rooms to return
            offset: Offset for pagination
            types: Optional list of room types to filter
            
        Returns:
            List of chat rooms
        """
        params = {
            'limit': limit,
            'offset': offset,
        }
        if types:
            params['types'] = ','.join(map(str, types))
        
        response = self._get('/me/chat/rooms', params=params)
        return [ChatRoom(**room) for room in response]
    
    def get_chat_messages(
        self,
        room_id: str,
        limit: int = 50,
        before: Optional[str] = None,
        after: Optional[str] = None
    ) -> List[ChatMessage]:
        """Get chat messages from a room.
        
        Args:
            room_id: The chat room ID
            limit: Number of messages to return
            before: Message ID to get messages before
            after: Message ID to get messages after
            
        Returns:
            List of chat messages
        """
        params = {
            'limit': limit,
        }
        if before:
            params['before'] = before
        if after:
            params['after'] = after
        
        response = self._get(f'/me/chat/rooms/{room_id}/messages', params=params)
        return [ChatMessage(**message) for message in response]
    
    def send_chat_message(
        self,
        room_id: str,
        content: str,
        type: str = "text",
        nonce: Optional[str] = None,
        meta: Optional[Dict[str, Any]] = None
    ) -> ChatMessage:
        """Send a chat message.
        
        Args:
            room_id: The chat room ID
            content: Message content
            type: Message type
            nonce: Optional message nonce
            meta: Optional message metadata
            
        Returns:
            Sent message
        """
        payload = {
            'content': content,
            'type': type,
        }
        if nonce:
            payload['nonce'] = nonce
        if meta:
            payload['meta'] = meta
        
        response = self._post(f'/me/chat/rooms/{room_id}/messages', json=payload)
        return ChatMessage(**response)
    
    # Drive Operations
    def get_file_pools(self) -> List[FilePool]:
        """Get available file pools.
        
        Returns:
            List of file pools
        """
        response = self._get('/me/drive/pools')
        return [FilePool(**pool) for pool in response]
    
    def get_cloud_files(
        self,
        limit: int = 50,
        offset: int = 0,
        pool_id: Optional[str] = None
    ) -> List[CloudFile]:
        """Get cloud files.
        
        Args:
            limit: Number of files to return
            offset: Offset for pagination
            pool_id: Optional pool ID to filter
            
        Returns:
            List of cloud files
        """
        params = {
            'limit': limit,
            'offset': offset,
        }
        if pool_id:
            params['pool_id'] = pool_id
        
        response = self._get('/me/drive/files', params=params)
        return [CloudFile(**file) for file in response]
    
    def upload_file(
        self,
        file_path: str,
        pool_id: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None
    ) -> DriveTask:
        """Upload a file.
        
        Args:
            file_path: Path to the file to upload
            pool_id: Optional pool ID
            name: Optional file name
            description: Optional file description
            
        Returns:
            Upload task information
        """
        with open(file_path, 'rb') as f:
            files = {'file': (name or file_path, f)}
            data = {}
            if pool_id:
                data['pool_id'] = pool_id
            if description:
                data['description'] = description
            
            response = self._post('/me/drive/upload', files=files, data=data)
            return DriveTask(**response)
    
    # Post Operations
    def create_post(
        self,
        content: str,
        title: Optional[str] = None,
        visibility: int = 0,
        type: int = 0,
        attachments: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        categories: Optional[List[str]] = None
    ) -> Post:
        """Create a new post.
        
        Args:
            content: Post content
            title: Optional post title
            visibility: Post visibility level
            type: Post type
            attachments: Optional list of attachment IDs
            tags: Optional list of tag IDs
            categories: Optional list of category IDs
            
        Returns:
            Created post
        """
        payload = {
            'content': content,
            'visibility': visibility,
            'type': type,
        }
        if title:
            payload['title'] = title
        if attachments:
            payload['attachments'] = attachments
        if tags:
            payload['tags'] = tags
        if categories:
            payload['categories'] = categories
        
        response = self._post('/me/posts', json=payload)
        return Post(**response)
    
    def get_posts(
        self,
        limit: int = 20,
        offset: int = 0,
        types: Optional[List[int]] = None,
        visibility: Optional[List[int]] = None
    ) -> List[Post]:
        """Get posts.
        
        Args:
            limit: Number of posts to return
            offset: Offset for pagination
            types: Optional list of post types to filter
            visibility: Optional list of visibility levels to filter
            
        Returns:
            List of posts
        """
        params = {
            'limit': limit,
            'offset': offset,
        }
        if types:
            params['types'] = ','.join(map(str, types))
        if visibility:
            params['visibility'] = ','.join(map(str, visibility))
        
        response = self._get('/me/posts', params=params)
        return [Post(**post) for post in response]
    
    # Wallet Operations
    def get_wallet(self) -> Wallet:
        """Get wallet information.
        
        Returns:
            Wallet information
        """
        response = self._get('/me/wallet')
        return Wallet(**response)
    
    def get_wallet_pockets(self) -> List[WalletPocket]:
        """Get wallet pockets.
        
        Returns:
            List of wallet pockets
        """
        response = self._get('/me/wallet/pockets')
        return [WalletPocket(**pocket) for pocket in response]
    
    def get_wallet_transactions(
        self,
        limit: int = 50,
        offset: int = 0,
        types: Optional[List[int]] = None
    ) -> List[Transaction]:
        """Get wallet transactions.
        
        Args:
            limit: Number of transactions to return
            offset: Offset for pagination
            types: Optional list of transaction types to filter
            
        Returns:
            List of transactions
        """
        params = {
            'limit': limit,
            'offset': offset,
        }
        if types:
            params['types'] = ','.join(map(str, types))
        
        response = self._get('/me/wallet/transactions', params=params)
        return [Transaction(**tx) for tx in response]
    
    # Helper methods
    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request.
        
        Args:
            endpoint: API endpoint
            params: Optional query parameters
            
        Returns:
            Response data
        """
        url = f"{self.server_url}{endpoint}"
        response = self._session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def _post(self, endpoint: str, json: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """Make a POST request.
        
        Args:
            endpoint: API endpoint
            json: Optional JSON payload
            **kwargs: Additional request arguments
            
        Returns:
            Response data
        """
        url = f"{self.server_url}{endpoint}"
        response = self._session.post(url, json=json, timeout=self.timeout, **kwargs)
        response.raise_for_status()
        return response.json()
    
    def _put(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a PUT request.
        
        Args:
            endpoint: API endpoint
            json: Optional JSON payload
            
        Returns:
            Response data
        """
        url = f"{self.server_url}{endpoint}"
        response = self._session.put(url, json=json, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def _patch(self, endpoint: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a PATCH request.
        
        Args:
            endpoint: API endpoint
            json: Optional JSON payload
            
        Returns:
            Response data
        """
        url = f"{self.server_url}{endpoint}"
        response = self._session.patch(url, json=json, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def _delete(self, endpoint: str) -> None:
        """Make a DELETE request.
        
        Args:
            endpoint: API endpoint
        """
        url = f"{self.server_url}{endpoint}"
        response = self._session.delete(url, timeout=self.timeout)
        response.raise_for_status()