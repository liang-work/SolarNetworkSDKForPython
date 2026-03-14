"""
Wallet-related models for Solar Network Python SDK.

This module contains data classes for wallets, transactions,
subscriptions, and financial operations.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any


@dataclass
class WalletStats:
    """Wallet statistics."""
    period_begin: datetime = field(default_factory=datetime.now)
    period_end: datetime = field(default_factory=datetime.now)
    total_transactions: int = 0
    total_orders: int = 0
    total_income: float = 0.0
    total_outgoing: float = 0.0
    sum: float = 0.0
    income_categories: Dict[str, float] = field(default_factory=dict)
    outgoing_categories: Dict[str, float] = field(default_factory=dict)


@dataclass
class WalletPocket:
    """Wallet pocket information."""
    id: str = ""
    currency: str = ""
    amount: float = 0.0
    wallet_id: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None


@dataclass
class Transaction:
    """Transaction information."""
    id: str = ""
    currency: str = ""
    amount: float = 0.0
    remarks: Optional[str] = None
    type: int = 0
    payer_wallet_id: Optional[str] = None
    payer_wallet: Optional[Wallet] = None
    payee_wallet_id: Optional[str] = None
    payee_wallet: Optional[Wallet] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None


@dataclass
class WalletSubscription:
    """Wallet subscription information."""
    id: str = ""
    begun_at: datetime = field(default_factory=datetime.now)
    ended_at: Optional[datetime] = None
    identifier: str = ""
    is_active: bool = True
    is_free_trial: bool = False
    status: int = 1
    payment_method: Optional[str] = None
    payment_details: Optional[Dict[str, Any]] = None
    base_price: Optional[float] = None
    coupon_id: Optional[str] = None
    coupon: Optional[Dict[str, Any]] = None
    renewal_at: Optional[datetime] = None
    account_id: str = ""
    account: Optional[Account] = None
    is_available: bool = True
    final_price: Optional[float] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None


@dataclass
class WalletSubscriptionRef:
    """Wallet subscription reference."""
    id: str = ""
    is_active: bool = False
    account_id: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None
    updated_at: datetime = field(default_factory=datetime.now)
    identifier: str = ""


@dataclass
class WalletOrder:
    """Wallet order information."""
    id: str = ""
    status: int = 0
    currency: str = ""
    remarks: Optional[str] = None
    app_identifier: str = ""
    meta: Dict[str, Any] = field(default_factory=dict)
    amount: int = 0
    expired_at: datetime = field(default_factory=datetime.now)
    payee_wallet_id: Optional[str] = None
    transaction_id: Optional[str] = None
    issuer_app_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None


@dataclass
class WalletGift:
    """Wallet gift information."""
    id: str = ""
    gift_code: str = ""
    subscription_identifier: str = ""
    recipient_id: Optional[str] = None
    recipient: Optional[Account] = None
    gifter_id: str = ""
    gifter: Optional[Account] = None
    redeemer_id: Optional[str] = None
    redeemer: Optional[Account] = None
    message: Optional[str] = None
    status: int = 0
    redeemed_at: Optional[datetime] = None
    expired_at: Optional[datetime] = None
    subscription_id: Optional[str] = None
    subscription: Optional[WalletSubscription] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None


@dataclass
class WalletFund:
    """Wallet fund information."""
    id: str = ""
    currency: str = ""
    total_amount: float = 0.0
    remaining_amount: float = 0.0
    amount_of_splits: int = 0
    split_type: int = 0  # 0: even, 1: random
    status: int = 0  # 0: created, 1: partially claimed, 2: fully claimed, 3: expired
    message: Optional[str] = None
    creator_account_id: str = ""
    creator_account: Optional[Account] = None
    expired_at: datetime = field(default_factory=datetime.now)
    recipients: List[WalletFundRecipient] = field(default_factory=list)
    is_open: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None


@dataclass
class WalletFundRecipient:
    """Wallet fund recipient information."""
    id: str = ""
    fund_id: str = ""
    recipient_account_id: str = ""
    recipient_account: Optional[Account] = None
    amount: float = 0.0
    is_received: bool = False
    received_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None


@dataclass
class LotteryTicket:
    """Lottery ticket information."""
    id: str = ""
    account_id: str = ""
    account: Optional[Account] = None
    region_one_numbers: List[int] = field(default_factory=list)
    region_two_number: int = 0
    multiplier: int = 0
    draw_status: int = 0
    draw_date: Optional[datetime] = None
    matched_region_one_numbers: Optional[List[int]] = None
    matched_region_two_number: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None


@dataclass
class LotteryRecord:
    """Lottery record information."""
    id: str = ""
    draw_date: datetime = field(default_factory=datetime.now)
    winning_region_one_numbers: List[int] = field(default_factory=list)
    winning_region_two_number: int = 0
    total_tickets: int = 0
    total_prizes_awarded: int = 0
    total_prize_amount: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None


@dataclass
class Wallet:
    """Wallet information."""
    id: str = ""
    pockets: List[WalletPocket] = field(default_factory=list)
    account_id: str = ""
    account: Optional[Account] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = None