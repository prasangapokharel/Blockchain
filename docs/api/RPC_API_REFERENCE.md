# PHN Blockchain - Complete RPC API Documentation

## Overview
PHN Blockchain provides a comprehensive RESTful API for web developers to integrate blockchain functionality into their applications. All endpoints return JSON with standardized response format.

**Base URL:** `http://localhost:8765`

**Standard Response Format:**
```json
{
  "success": true/false,
  "data": {...},
  "error": null/"error message",
  "timestamp": 1234567890
}
```

---

## 🔐 Wallet API (`/api/v1/wallet/*`)

### Create Wallet
**POST** `/api/v1/wallet/create`

Creates a new wallet with public/private keypair.

**Response:**
```json
{
  "success": true,
  "data": {
    "public_key": "128 hex chars",
    "private_key": "64 hex chars",
    "address": "PHN...",
    "warning": "STORE PRIVATE KEY SECURELY - Cannot be recovered if lost"
  }
}
```

### Import Wallet
**POST** `/api/v1/wallet/import`

Import wallet from private key.

**Body:**
```json
{
  "private_key": "64 hex character private key"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "public_key": "...",
    "address": "PHN...",
    "imported": true
  }
}
```

### Sign Message
**POST** `/api/v1/wallet/sign`

Sign a message or transaction.

**Body:**
```json
{
  "private_key": "signer's private key",
  "message": "message to sign" // or object
}
```

### Verify Signature
**POST** `/api/v1/wallet/verify`

Verify a signed message.

**Body:**
```json
{
  "public_key": "signer's public key",
  "message": "original message",
  "signature": "signature to verify"
}
```

### Get Address from Public Key
**GET** `/api/v1/wallet/address/{public_key}`

Convert public key to PHN address.

---

## 💰 Balance API (`/api/v1/balance/*`)

### Get PHN Balance
**GET** `/api/v1/balance/{address}`

Get PHN balance for an address.

**Response:**
```json
{
  "success": true,
  "data": {
    "address": "PHN...",
    "balance": 1000.50,
    "pending": 50.25,
    "total": 1050.75
  }
}
```

### Get Portfolio
**GET** `/api/v1/balance/portfolio/{address}`

Get complete portfolio (PHN + assets).

**Response:**
```json
{
  "success": true,
  "data": {
    "address": "PHN...",
    "phn_balance": 1000.50,
    "total_received": 5000.00,
    "total_sent": 3999.50,
    "transaction_count": 42,
    "first_seen": 1234567890,
    "last_activity": 1234567900
  }
}
```

### Get Balance History
**GET** `/api/v1/balance/history/{address}?limit=100`

Get balance history over time.

### Get Rich List
**GET** `/api/v1/balance/richlist?limit=100&exclude_system=true`

Get richest addresses on the network.

---

## 📝 Transaction API (`/api/v1/tx/*`)

### Send Transaction
**POST** `/api/v1/tx/send`

Send a transaction to the network.

**Body:**
```json
{
  "tx": {
    "sender": "public key or address",
    "recipient": "PHN address",
    "amount": 100.50,
    "fee": 0.01,
    "timestamp": 1234567890,
    "txid": "transaction id",
    "signature": "ECDSA signature"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "txid": "abc123...",
    "status": "pending",
    "mempool_size": 42
  }
}
```

### Get Transaction
**GET** `/api/v1/tx/{txid}`

Get transaction by TXID.

**Response:**
```json
{
  "success": true,
  "data": {
    "transaction": {...},
    "block_index": 1234,
    "block_hash": "abc...",
    "timestamp": 1234567890,
    "confirmations": 10,
    "status": "confirmed"
  }
}
```

### Get Transaction History
**GET** `/api/v1/tx/history/{address}?limit=50&offset=0&type=all`

Get transaction history for an address.

**Query Parameters:**
- `limit`: Max transactions (default 50, max 500)
- `offset`: Pagination offset (default 0)
- `type`: Filter by `all`, `sent`, or `received`

### Get Pending Transactions
**GET** `/api/v1/tx/pending?limit=50&sort=fee`

Get pending transactions in mempool.

**Query Parameters:**
- `limit`: Max transactions (default 50, max 500)
- `sort`: Sort by `fee` or `time` (default `fee`)

### Broadcast Transaction
**POST** `/api/v1/tx/broadcast`

Broadcast a signed transaction (alias for `/api/v1/tx/send`).

---

## 🔍 Explorer API (`/api/v1/explorer/*`)

### Get Block by Index
**GET** `/api/v1/explorer/block/{index}`

Get block by index (0 = genesis).

**Response:**
```json
{
  "success": true,
  "data": {
    "index": 1234,
    "hash": "abc...",
    "timestamp": 1234567890,
    "transactions": [...],
    "transaction_count": 10,
    "total_amount": 500.00,
    "total_fees": 0.10,
    "size_bytes": 5000,
    "confirmations": 100
  }
}
```

### Get Latest Blocks
**GET** `/api/v1/explorer/blocks/latest?limit=10`

Get latest blocks.

### Get Block Range
**GET** `/api/v1/explorer/blocks/range/{start}/{end}`

Get range of blocks (max 100 blocks).

### Get Network Statistics
**GET** `/api/v1/explorer/stats`

Get comprehensive network statistics.

**Response:**
```json
{
  "success": true,
  "data": {
    "chain": {
      "height": 10000,
      "size_bytes": 50000000,
      "size_mb": 47.68
    },
    "supply": {
      "total_supply": 21000000,
      "circulating_supply": 5000000,
      "remaining": 16000000,
      "percentage_mined": 23.81
    },
    "mining": {
      "current_difficulty": 4,
      "current_block_reward": 50,
      "average_block_time": 61.5,
      "target_block_time": 60,
      "total_blocks_mined": 10000
    },
    "transactions": {
      "total_confirmed": 50000,
      "pending": 42,
      "total_fees_paid": 250.50
    },
    "network": {
      "unique_addresses": 1000,
      "active_addresses_24h": 150
    }
  }
}
```

### Search Blockchain
**GET** `/api/v1/explorer/search/{query}`

Search by block hash, txid, or address.

**Returns:** Block, transaction, or address data.

### Get Node Info
**GET** `/api/v1/explorer/info`

Get node information.

---

## 🎨 Assets API (`/api/v1/asset/*`)

### Create Asset
**POST** `/api/v1/asset/create`

Create a new tokenized asset (NFT or fractionalized).

**Body:**
```json
{
  "asset_type": "GOLD|LAND|REAL_ESTATE|COMMODITY|SECURITY|CUSTOM",
  "name": "Gold Bar #1234",
  "description": "1kg 24k gold bar",
  "total_supply": 1,
  "owner_address": "PHN...",
  "metadata": {
    "weight": "1kg",
    "purity": "24k",
    "location": "Vault A"
  },
  "fractional": false,
  "standard": "PHN721"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "asset_id": "unique_id",
    "asset": {...}
  }
}
```

### Transfer Asset
**POST** `/api/v1/asset/transfer`

Transfer asset ownership.

**Body:**
```json
{
  "asset_id": "unique_id",
  "from_address": "PHN...",
  "to_address": "PHN...",
  "amount": 1,
  "signature": "ECDSA signature"
}
```

### Fractionalize Asset
**POST** `/api/v1/asset/fractionalize`

Fractionalize an asset into shares.

**Body:**
```json
{
  "asset_id": "unique_id",
  "owner_address": "PHN...",
  "shares": 1000,
  "signature": "ECDSA signature"
}
```

### Get Asset Details
**GET** `/api/v1/asset/{asset_id}`

Get complete asset information.

### Get Asset History
**GET** `/api/v1/asset/history/{asset_id}`

Get asset transaction history.

### Get Assets by Owner
**GET** `/api/v1/assets/owner/{address}`

Get all assets owned by an address.

### Get Assets by Type
**GET** `/api/v1/assets/type/{asset_type}?limit=50`

Get all assets of a specific type.

### List All Assets
**GET** `/api/v1/assets/list?limit=50&offset=0`

List all assets with pagination.

### Get Asset Statistics
**GET** `/api/v1/assets/stats`

Get asset platform statistics.

---

## 🪙 Token Platform API (`/api/v1/token/*`)

### Create Custom Token
**POST** `/api/v1/token/create`

Create a custom token (like ERC-20).

**Body:**
```json
{
  "name": "MyToken",
  "symbol": "MTK",
  "total_supply": 1000000,
  "decimals": 8,
  "owner_address": "PHN...",
  "description": "My custom token",
  "metadata": {},
  "mintable": false,
  "burnable": true
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "token_id": "ABC123",
    "token": {
      "token_id": "ABC123",
      "name": "MyToken",
      "symbol": "MTK",
      "total_supply": 1000000,
      "decimals": 8,
      "owner_address": "PHN...",
      "standard": "PHN-20",
      "created_at": 1234567890
    },
    "message": "Token MTK created successfully"
  }
}
```

### Mint Tokens
**POST** `/api/v1/token/mint`

Mint additional tokens (only if mintable).

**Body:**
```json
{
  "token_id": "ABC123",
  "to_address": "PHN...",
  "amount": 1000,
  "signature": "owner signature"
}
```

### Burn Tokens
**POST** `/api/v1/token/burn`

Burn (destroy) tokens.

**Body:**
```json
{
  "token_id": "ABC123",
  "from_address": "PHN...",
  "amount": 100,
  "signature": "signature"
}
```

### Transfer Tokens
**POST** `/api/v1/token/transfer`

Transfer tokens between addresses.

**Body:**
```json
{
  "token_id": "ABC123",
  "from_address": "PHN...",
  "to_address": "PHN...",
  "amount": 50,
  "signature": "sender signature"
}
```

### Get Token Info
**GET** `/api/v1/token/{token_id}`

Get token information.

### Get Token Balance
**GET** `/api/v1/token/balance/{token_id}/{address}`

Get token balance for an address.

### Get Token Supply
**GET** `/api/v1/token/supply/{token_id}`

Get token supply information.

### List All Tokens
**GET** `/api/v1/tokens/list?limit=50&offset=0`

List all tokens with pagination.

### Get Tokens by Holder
**GET** `/api/v1/tokens/holder/{address}`

Get all tokens held by an address.

### Get Token Statistics
**GET** `/api/v1/tokens/stats`

Get token platform statistics.

---

## 🔧 Legacy Endpoints (Backward Compatibility)

These endpoints maintain compatibility with existing tools:

- `POST /send_tx` → Redirects to `/api/v1/tx/send`
- `POST /get_pending` → Returns pending transactions
- `POST /get_balance` → Returns balance
- `POST /get_transaction` → Returns transaction
- `GET /info` → Node information
- `GET /token_info` → PHN token information
- `GET /mining_info` → Mining parameters
- `POST /submit_block` → Submit mined block
- `POST /get_blockchain` → Get entire blockchain

---

## 🔑 Authentication & Security

### Signature Requirements
Most write operations (send, transfer, mint, burn) require ECDSA signatures:

1. **Create signature:**
   - Hash message with SHA-256
   - Sign hash with SECP256k1 private key
   - Include signature in request

2. **Server validation:**
   - Verifies signature matches public key
   - Ensures sender has sufficient balance
   - Validates transaction structure

### Security Features
- ✅ ECDSA signatures (SECP256k1)
- ✅ Nonce for TXID uniqueness
- ✅ Replay attack protection
- ✅ Rate limiting on endpoints
- ✅ Balance validation before operations
- ✅ Immutable blockchain records

---

## 📊 Response Status Codes

- `200 OK` - Request successful
- `400 Bad Request` - Invalid parameters or insufficient balance
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

---

## 🚀 Quick Start Examples

### JavaScript (Node.js)
```javascript
const axios = require('axios');

// Create wallet
const wallet = await axios.post('http://localhost:8765/api/v1/wallet/create');
console.log('Address:', wallet.data.data.address);

// Check balance
const balance = await axios.get(`http://localhost:8765/api/v1/balance/${wallet.data.data.address}`);
console.log('Balance:', balance.data.data.balance);

// Create custom token
const token = await axios.post('http://localhost:8765/api/v1/token/create', {
  name: 'MyToken',
  symbol: 'MTK',
  total_supply: 1000000,
  owner_address: wallet.data.data.address
});
console.log('Token ID:', token.data.data.token_id);
```

### Python
```python
import requests

# Create wallet
wallet = requests.post('http://localhost:8765/api/v1/wallet/create').json()
address = wallet['data']['address']
print(f'Address: {address}')

# Check balance
balance = requests.get(f'http://localhost:8765/api/v1/balance/{address}').json()
print(f'Balance: {balance["data"]["balance"]}')

# Get network stats
stats = requests.get('http://localhost:8765/api/v1/explorer/stats').json()
print(f'Chain height: {stats["data"]["chain"]["height"]}')
```

### cURL
```bash
# Create wallet
curl -X POST http://localhost:8765/api/v1/wallet/create

# Get balance
curl http://localhost:8765/api/v1/balance/PHN...

# Get network stats
curl http://localhost:8765/api/v1/explorer/stats

# Create token
curl -X POST http://localhost:8765/api/v1/token/create \
  -H "Content-Type: application/json" \
  -d '{"name":"MyToken","symbol":"MTK","total_supply":1000000,"owner_address":"PHN..."}'
```

---

## 🎯 Use Cases

### Web3 Wallet Integration
Use wallet endpoints to create/import wallets and sign transactions.

### Blockchain Explorer
Use explorer endpoints to display blocks, transactions, and network stats.

### DeFi Application
Use token endpoints to create custom tokens, manage liquidity, and enable trading.

### Asset Tokenization Platform
Use asset endpoints to tokenize real-world assets (gold, real estate, etc.).

### Payment Gateway
Use transaction endpoints to accept PHN payments with confirmations tracking.

### Portfolio Tracker
Use balance and history endpoints to track holdings and transactions.

---

## 📚 Additional Resources

- **SDK Documentation:** `docs/SDK_API_REFERENCE.md`
- **Phonesium Python SDK:** `phonesium/` directory
- **Security Audit:** `docs/SECURITY_AUDIT.md`
- **User Tools:** `user/` directory

---

## 🆘 Support

For issues or questions:
- Check existing documentation in `docs/` folder
- Review code examples in `test/` and `user/` directories
- Inspect API endpoint source code in `app/api/v1/endpoints/`

---

**PHN Blockchain** - Enterprise-grade blockchain with complete transparency
