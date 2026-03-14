"""
Solar Network Python SDK

A Python SDK for interacting with the Solar Network API, providing authentication,
account management, and content operations.
"""

from .client import SolarNetworkClient
from .auth import WebAuthClient
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
    PollOption, PollQuestionType, PollAnswer, PostTag, CategorySubscription,
    PostCategory, ScrappedLink, Heatmap, HeatmapItem,
    
    # Realm models
    Realm, RealmMember,
    
    # Wallet models
    Wallet, WalletStats, WalletPocket, Transaction, WalletSubscription,
    WalletSubscriptionRef, WalletOrder, WalletGift, WalletFund,
    WalletFundRecipient, LotteryTicket, LotteryRecord,
)

__version__ = "1.0.0"
__author__ = "Solar Network"
__license__ = "MIT"

__all__ = [
    # Main classes
    'SolarNetworkClient',
    'WebAuthClient',
    
    # Account models
    'Account', 'AccountProfile', 'AccountStatus', 'AccountBadge',
    'ContactMethod', 'Notification', 'VerificationMark', 'AuthDevice',
    'AuthDeviceWithSession', 'ExperienceRecord', 'SocialCreditRecord',
    'FriendOverviewItem',
    
    # Auth models
    'AuthChallenge', 'AuthSession', 'AppToken', 'GeoIpLocation',
    'AuthFactor', 'AccountConnection',
    
    # Activity models
    'NotableDay', 'TimelineEvent', 'CheckInResult', 'FortuneTip',
    'EventCalendarEntry', 'PresenceActivity',
    
    # ActivityPub models
    'ActivityPubInstance', 'ActivityPubUser', 'ActivityPubActor',
    'ActivityPubFollowResponse', 'ActorStatusResponse',
    
    # Chat models
    'ChatRoom', 'ChatMessage', 'ChatReaction', 'ChatMember', 'ChatSummary',
    'ChatOnlineAccount', 'ChatOnlineStatus', 'MessageSyncResponse',
    'ChatRealtimeJoinResponse', 'CallParticipant', 'RealtimeCall',
    
    # Drive models
    'FileReplica', 'CloudFileObject', 'CloudFile', 'CloudFileIndex',
    'FilePool', 'CloudFolder', 'FileListItem', 'DriveTask', 'UniversalFile',
    'UniversalFileType',
    
    # Live models
    'LiveStream', 'LiveStreamStatus', 'LiveStreamType', 'LiveStreamVisibility',
    
    # Post models
    'Post', 'Publisher', 'PublisherStats', 'PublisherSubscription',
    'ReactInfo', 'PostEmbedView', 'PostEmbedViewRenderer', 'PostAward',
    'PostReaction', 'PostFeaturedRecord', 'PostWithStats', 'PollWithStats',
    'Poll', 'PollQuestion', 'PollOption', 'PollQuestionType', 'PollAnswer',
    'PostTag', 'CategorySubscription', 'PostCategory', 'ScrappedLink',
    'Heatmap', 'HeatmapItem',
    
    # Realm models
    'Realm', 'RealmMember',
    
    # Wallet models
    'Wallet', 'WalletStats', 'WalletPocket', 'Transaction',
    'WalletSubscription', 'WalletSubscriptionRef', 'WalletOrder',
    'WalletGift', 'WalletFund', 'WalletFundRecipient', 'LotteryTicket',
    'LotteryRecord',
]