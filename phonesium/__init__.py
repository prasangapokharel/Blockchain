"""
Phonesium - PHN Blockchain Python SDK
Easy-to-use library for interacting with PHN blockchain

Usage:
    from phonesium import Wallet, PhonesiumClient, Miner
    
    # Create wallet
    wallet = Wallet.create()
    
    # Connect to node
    client = PhonesiumClient("http://localhost:8000")
    
    # Check balance
    balance = client.get_balance(wallet.address)
    
    # Send tokens
    tx = client.send_tokens(wallet, recipient="PHN...", amount=10.0)
    
    # Mine blocks
    miner = Miner(wallet)
    miner.mine_continuous(max_blocks=5)
"""

from .client import PhonesiumClient
from .wallet import Wallet
from .miner import Miner
from .exceptions import (
    PhonesiumError,
    NetworkError,
    InsufficientBalanceError,
    InvalidTransactionError,
    InvalidAddressError,
    WalletError
)

__version__ = "1.0.0"
__author__ = "Phonesium Team"
__email__ = "support@phonesium.network"

__all__ = [
    "PhonesiumClient",
    "Wallet",
    "Miner",
    "PhonesiumError",
    "NetworkError",
    "InsufficientBalanceError",
    "InvalidTransactionError",
    "InvalidAddressError",
    "WalletError"
]
