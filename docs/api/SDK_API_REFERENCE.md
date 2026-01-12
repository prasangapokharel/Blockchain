# Phonesium SDK - Complete API Reference

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Wallet API](#wallet-api)
4. [Client API](#client-api)
5. [Miner API](#miner-api)
6. [Error Handling](#error-handling)
7. [Examples](#examples)

---

## Installation

```bash
# Install from source
pip install -e .

# Or install from PyPI (when published)
pip install phonesium
```

**Requirements:**
- Python 3.10+
- requests>=2.28.0
- ecdsa>=0.18.0
- cryptography>=41.0.0

---

## Quick Start

```python
from phonesium import Wallet, PhonesiumClient, Miner

# Create a new wallet
wallet = Wallet.create()
print(f"Address: {wallet.address}")

# Save wallet with encryption
wallet.save("my_wallet.json", password="secure_password")

# Load wallet
wallet = Wallet.load("my_wallet.json", password="secure_password")

# Connect to blockchain
client = PhonesiumClient(node_url="http://localhost:8000")

# Check balance
balance = client.get_balance(wallet.address)
print(f"Balance: {balance} PHN")

# Send tokens
tx = client.send_tokens(
    wallet=wallet,
    recipient="PHN...",
    amount=10.0,
    fee=1.0
)
print(f"Transaction ID: {tx['txid']}")
```

---

## Wallet API

### Class: `Wallet`

A secure wallet for PHN blockchain with AES-256-GCM encryption.

#### Methods

##### `Wallet.create() -> Wallet`

Create a new wallet with randomly generated keys.

**Returns:**
- `Wallet` object with new address and keys

**Example:**
```python
wallet = Wallet.create()
print(wallet.address)  # PHN...
```

---

##### `Wallet.from_private_key(private_key: str) -> Wallet`

Create wallet from existing private key.

**Parameters:**
- `private_key` (str): 64-character hex private key

**Returns:**
- `Wallet` object

**Raises:**
- `WalletError`: If private key is invalid

**Example:**
```python
wallet = Wallet.from_private_key("abc123...")
```

---

##### `wallet.save(filepath: str, password: str) -> None`

Save wallet with AES-256-GCM encryption.

**Parameters:**
- `filepath` (str): Path to save wallet file
- `password` (str): Encryption password (min 8 characters)

**Security:**
- Uses PBKDF2-HMAC with 100,000 iterations
- AES-256-GCM encryption
- Private key never stored in plaintext

**Example:**
```python
wallet.save("my_wallet.json", password="strong_password")
```

---

##### `Wallet.load(filepath: str, password: str) -> Wallet`

Load encrypted wallet from file.

**Parameters:**
- `filepath` (str): Path to wallet file
- `password` (str): Decryption password

**Returns:**
- `Wallet` object

**Raises:**
- `WalletError`: If password is wrong or file is corrupted

**Example:**
```python
wallet = Wallet.load("my_wallet.json", password="strong_password")
```

---

##### `wallet.sign(data) -> str`

Sign data with private key using ECDSA.

**Parameters:**
- `data` (str or bytes): Data to sign

**Returns:**
- Hex-encoded signature (str)

**Example:**
```python
signature = wallet.sign("Hello World")
```

---

##### `wallet.verify_signature(data, signature: str) -> bool`

Verify signature validity.

**Parameters:**
- `data` (str or bytes): Original data
- `signature` (str): Hex-encoded signature

**Returns:**
- `True` if valid, `False` otherwise

**Example:**
```python
is_valid = wallet.verify_signature("Hello", signature)
```

---

##### `wallet.create_transaction(recipient: str, amount: float, fee: float = 1.0) -> dict`

Create and sign a transaction.

**Parameters:**
- `recipient` (str): Recipient PHN address
- `amount` (float): Amount to send
- `fee` (float): Transaction fee (default: 1.0)

**Returns:**
- Transaction dictionary ready to broadcast

**Example:**
```python
tx = wallet.create_transaction(
    recipient="PHN...",
    amount=100.5,
    fee=1.0
)
```

---

##### `wallet.get_private_key(show_warning: bool = True) -> str`

Get private key (USE WITH CAUTION).

**Parameters:**
- `show_warning` (bool): Show security warning

**Returns:**
- 64-character hex private key

**Warning:**
- Never share your private key
- Only use when absolutely necessary

**Example:**
```python
private_key = wallet.get_private_key()
```

---

##### `wallet.export_private_key(confirm: bool = False) -> str`

Export private key with confirmation.

**Parameters:**
- `confirm` (bool): Must be `True` to export

**Returns:**
- Private key (str)

**Raises:**
- `WalletError`: If `confirm=False`

**Example:**
```python
key = wallet.export_private_key(confirm=True)
```

---

##### `wallet.export_wallet(include_private_key: bool = False) -> dict`

Export wallet data as dictionary.

**Parameters:**
- `include_private_key` (bool): Include private key (dangerous!)

**Returns:**
- Wallet data dictionary

**Example:**
```python
# Public data only
data = wallet.export_wallet(include_private_key=False)

# Full export (dangerous!)
data = wallet.export_wallet(include_private_key=True)
```

---

#### Properties

- `wallet.address` (str): PHN address (43 characters)
- `wallet.public_key` (str): Public key (128 hex characters)
- `wallet.private_key` (str): Private property (use `get_private_key()`)

---

## Client API

### Class: `PhonesiumClient`

API client for interacting with PHN blockchain node.

#### Constructor

```python
PhonesiumClient(node_url: str = "http://localhost:8000")
```

**Parameters:**
- `node_url` (str): URL of the blockchain node

**Example:**
```python
client = PhonesiumClient("http://localhost:8000")
```

---

#### Methods

##### `client.get_balance(address: str) -> float`

Get balance for an address.

**Parameters:**
- `address` (str): PHN address

**Returns:**
- Balance in PHN (float)

**Raises:**
- `NetworkError`: If node is unreachable
- `InvalidAddressError`: If address is invalid

**Example:**
```python
balance = client.get_balance("PHN...")
print(f"Balance: {balance} PHN")
```

---

##### `client.send_tokens(wallet: Wallet, recipient: str, amount: float, fee: float = 1.0) -> dict`

Send tokens to recipient.

**Parameters:**
- `wallet` (Wallet): Sender wallet
- `recipient` (str): Recipient PHN address
- `amount` (float): Amount to send
- `fee` (float): Transaction fee

**Returns:**
- Transaction result dictionary

**Raises:**
- `InsufficientBalanceError`: Not enough balance
- `InvalidAddressError`: Invalid recipient address
- `NetworkError`: Node communication error

**Example:**
```python
tx = client.send_tokens(
    wallet=my_wallet,
    recipient="PHN...",
    amount=50.0,
    fee=1.0
)
```

---

##### `client.get_blockchain_info() -> dict`

Get blockchain information.

**Returns:**
- Dictionary with blockchain data:
  - `height`: Current block height
  - `difficulty`: Current mining difficulty
  - `last_block_hash`: Hash of latest block
  - `total_supply`: Total tokens in circulation

**Example:**
```python
info = client.get_blockchain_info()
print(f"Height: {info['height']}")
```

---

##### `client.get_block(block_index: int) -> dict`

Get specific block by index.

**Parameters:**
- `block_index` (int): Block height

**Returns:**
- Block data dictionary

**Raises:**
- `ValueError`: If block index out of range
- `NetworkError`: If node is unreachable

**Example:**
```python
block = client.get_block(100)
print(f"Block hash: {block['hash']}")
```

---

##### `client.get_latest_blocks(count: int = 10) -> list`

Get recent blocks.

**Parameters:**
- `count` (int): Number of blocks to retrieve

**Returns:**
- List of block dictionaries

**Example:**
```python
blocks = client.get_latest_blocks(5)
for block in blocks:
    print(f"Block {block['index']}: {block['hash']}")
```

---

##### `client.search_transaction(txid: str) -> dict`

Search for transaction by ID.

**Parameters:**
- `txid` (str): Transaction ID (hash)

**Returns:**
- Dictionary with transaction and block info:
  - `transaction`: Transaction data
  - `block_index`: Block height
  - `block_hash`: Block hash
  - `confirmed`: Confirmation status

**Raises:**
- `ValueError`: If transaction not found

**Example:**
```python
tx = client.search_transaction("abc123...")
print(f"Confirmed in block {tx['block_index']}")
```

---

##### `client.get_address_transactions(address: str) -> list`

Get all transactions for an address.

**Parameters:**
- `address` (str): PHN address

**Returns:**
- List of transactions (sent and received)

**Example:**
```python
txs = client.get_address_transactions("PHN...")
for tx in txs:
    print(f"{tx['type']}: {tx['amount']} PHN")
```

---

##### `client.get_mempool() -> list`

Get pending transactions in mempool.

**Returns:**
- List of pending transactions

**Example:**
```python
pending = client.get_mempool()
print(f"{len(pending)} pending transactions")
```

---

##### `client.get_peers() -> list`

Get list of connected peers.

**Returns:**
- List of peer URLs

**Example:**
```python
peers = client.get_peers()
print(f"Connected to {len(peers)} peers")
```

---

## Miner API

### Class: `Miner`

Simple miner for PHN blockchain.

#### Constructor

```python
Miner(wallet: Wallet, node_url: str = "http://localhost:8000")
```

**Parameters:**
- `wallet` (Wallet): Wallet to receive mining rewards
- `node_url` (str): URL of blockchain node

**Example:**
```python
miner = Miner(my_wallet, "http://localhost:8000")
```

---

#### Methods

##### `miner.mine_block(timeout: int = 60) -> dict`

Mine a single block.

**Parameters:**
- `timeout` (int): Maximum seconds to spend mining

**Returns:**
- Mining result dictionary:
  - `success` (bool): Whether block was accepted
  - `block` (dict): Block data
  - `reward` (float): Mining reward
  - `time` (float): Time taken
  - `hashrate` (float): Hashes per second
  - `hashes` (int): Total hashes tried

**Example:**
```python
result = miner.mine_block(timeout=120)
if result and result['success']:
    print(f"Mined block! Reward: {result['reward']} PHN")
```

---

##### `miner.mine_continuous(max_blocks: int = None, delay: float = 1.0) -> None`

Mine continuously.

**Parameters:**
- `max_blocks` (int): Max blocks to mine (None = infinite)
- `delay` (float): Delay between blocks (seconds)

**Example:**
```python
# Mine 10 blocks
miner.mine_continuous(max_blocks=10, delay=1.0)

# Mine indefinitely (press Ctrl+C to stop)
miner.mine_continuous()
```

---

##### `miner.get_mining_info() -> dict`

Get current mining parameters.

**Returns:**
- Dictionary with mining info:
  - `difficulty`: Current difficulty
  - `height`: Current block height
  - `last_block_hash`: Previous block hash
  - `mining_reward`: Current reward

**Example:**
```python
info = miner.get_mining_info()
print(f"Difficulty: {info['difficulty']}")
```

---

##### `miner.get_stats() -> dict`

Get miner statistics.

**Returns:**
- Dictionary with miner stats:
  - `miner_address`: Wallet address
  - `blocks_mined`: Total blocks mined
  - `total_rewards`: Total rewards earned
  - `node_url`: Connected node

**Example:**
```python
stats = miner.get_stats()
print(f"Blocks mined: {stats['blocks_mined']}")
print(f"Total rewards: {stats['total_rewards']} PHN")
```

---

## Error Handling

### Exception Hierarchy

```
PhonesiumError
├── NetworkError
├── InsufficientBalanceError
├── InvalidTransactionError
├── InvalidAddressError
└── WalletError
```

### Exception Details

#### `PhonesiumError`

Base exception for all Phonesium errors.

---

#### `NetworkError`

Network connection or API error.

**Common Causes:**
- Node is not running
- Incorrect node URL
- Network connectivity issues

**Example:**
```python
try:
    balance = client.get_balance("PHN...")
except NetworkError as e:
    print(f"Node error: {e}")
```

---

#### `InsufficientBalanceError`

Not enough balance for transaction.

**Example:**
```python
try:
    tx = client.send_tokens(wallet, "PHN...", 1000000)
except InsufficientBalanceError:
    print("Not enough funds")
```

---

#### `InvalidAddressError`

Invalid PHN address format.

**Valid Format:**
- Starts with "PHN"
- 43 characters total
- Alphanumeric

**Example:**
```python
try:
    balance = client.get_balance("invalid")
except InvalidAddressError:
    print("Invalid address")
```

---

#### `WalletError`

Wallet creation or loading error.

**Common Causes:**
- Wrong password
- Corrupted wallet file
- Invalid private key

**Example:**
```python
try:
    wallet = Wallet.load("wallet.json", "wrong_password")
except WalletError as e:
    print(f"Wallet error: {e}")
```

---

## Examples

### Example 1: Create and Save Wallet

```python
from phonesium import Wallet

# Create new wallet
wallet = Wallet.create()
print(f"Created wallet: {wallet.address}")

# Save with encryption
wallet.save("my_wallet.json", password="SecureP@ssw0rd")
print("Wallet saved securely!")

# Load wallet
wallet2 = Wallet.load("my_wallet.json", password="SecureP@ssw0rd")
print(f"Loaded wallet: {wallet2.address}")

# Verify same wallet
assert wallet.address == wallet2.address
```

---

### Example 2: Send Tokens

```python
from phonesium import Wallet, PhonesiumClient

# Load wallet
wallet = Wallet.load("sender.json", password="password")

# Connect to node
client = PhonesiumClient("http://localhost:8000")

# Check balance
balance = client.get_balance(wallet.address)
print(f"Current balance: {balance} PHN")

# Send tokens
if balance > 10:
    tx = client.send_tokens(
        wallet=wallet,
        recipient="PHN...",
        amount=10.0,
        fee=1.0
    )
    print(f"Sent! TX ID: {tx['txid']}")
else:
    print("Insufficient balance")
```

---

### Example 3: Mining

```python
from phonesium import Wallet, Miner

# Load wallet
wallet = Wallet.load("miner.json", password="password")

# Create miner
miner = Miner(wallet, node_url="http://localhost:8000")

# Mine single block
result = miner.mine_block(timeout=120)

if result and result['success']:
    print(f"Mined block!")
    print(f"Reward: {result['reward']} PHN")
    print(f"Hashrate: {result['hashrate']:.0f} H/s")
else:
    print("Mining failed or timed out")

# Mine continuously (5 blocks)
miner.mine_continuous(max_blocks=5)
```

---

### Example 4: Transaction History

```python
from phonesium import PhonesiumClient

client = PhonesiumClient("http://localhost:8000")

# Get all transactions for address
address = "PHN..."
txs = client.get_address_transactions(address)

print(f"Transaction history for {address}:")
print(f"Total transactions: {len(txs)}\n")

for tx in txs:
    print(f"Block {tx['block_index']}")
    print(f"Type: {tx['type']}")
    print(f"Amount: {tx['amount']} PHN")
    print(f"Fee: {tx['fee']} PHN")
    print(f"TX ID: {tx['txid']}")
    print("-" * 50)
```

---

### Example 5: Block Explorer

```python
from phonesium import PhonesiumClient

client = PhonesiumClient("http://localhost:8000")

# Get blockchain info
info = client.get_blockchain_info()
print(f"Blockchain Height: {info['height']}")
print(f"Current Difficulty: {info['difficulty']}")
print(f"Total Supply: {info['total_supply']} PHN\n")

# Get latest blocks
blocks = client.get_latest_blocks(5)
print("Latest 5 blocks:")

for block in blocks:
    print(f"\nBlock #{block['index']}")
    print(f"Hash: {block['hash']}")
    print(f"Miner: {block['miner']}")
    print(f"Transactions: {len(block.get('transactions', []))}")
    print(f"Timestamp: {block['timestamp']}")
```

---

### Example 6: Error Handling

```python
from phonesium import Wallet, PhonesiumClient
from phonesium.exceptions import (
    NetworkError,
    InsufficientBalanceError,
    InvalidAddressError,
    WalletError
)

try:
    # Load wallet
    wallet = Wallet.load("wallet.json", password="password")
    
    # Connect to node
    client = PhonesiumClient("http://localhost:8000")
    
    # Send tokens
    tx = client.send_tokens(
        wallet=wallet,
        recipient="PHN...",
        amount=100.0,
        fee=1.0
    )
    
    print(f"Success! TX: {tx['txid']}")

except WalletError as e:
    print(f"Wallet error: {e}")
except NetworkError as e:
    print(f"Network error: {e}")
except InsufficientBalanceError:
    print("Not enough funds")
except InvalidAddressError:
    print("Invalid recipient address")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Best Practices

### Security

1. **Always encrypt wallets** with strong passwords
2. **Never share private keys** or wallet passwords
3. **Backup wallet files** to multiple secure locations
4. **Use high fees** for urgent transactions
5. **Verify addresses** before sending tokens

### Performance

1. **Reuse client instances** instead of creating new ones
2. **Handle NetworkError** with retries
3. **Use appropriate timeouts** for mining
4. **Check balance** before sending transactions
5. **Monitor node status** regularly

### Development

1. **Test with small amounts** first
2. **Use try-except blocks** for all API calls
3. **Log errors** for debugging
4. **Validate inputs** before API calls
5. **Keep SDK updated** to latest version

---

## Support

For issues and questions:
- Check this documentation
- Review example code
- Search GitHub issues
- Create new issue with details

---

**Phonesium SDK v1.0.0**  
Production-ready Python SDK for PHN Blockchain
