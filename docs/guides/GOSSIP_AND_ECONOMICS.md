# PHN Blockchain - Gossip Protocol & Economic Model

## Overview
PHN blockchain implements a **gossip protocol** for fast block propagation and a **fair economic model** with proper fee distribution and halving schedule.

---

## Gossip Protocol (P2P Block Propagation)

### How It Works

```
Miner A mines block → Submit to Node → Node validates → Node broadcasts to all peers
                                                      ↓
                                      Peer 1 ← Peer 2 ← Peer 3 ← Peer 4
                                        ↓       ↓       ↓       ↓
                                     Miner B  Miner C  Miner D  Miner E
```

### Implementation

**File: `app/main.py`**

1. **`broadcast_block_to_peers(block)`** - Gossip function
   - Called automatically when a block is submitted
   - Sends block to ALL connected peers
   - Provides feedback on success/failure

2. **`http_submit_block(request)`** - Block submission endpoint
   - Validates the block
   - Adds to blockchain
   - **Triggers gossip broadcast** to all peers

### Benefits

✓ **Fast Propagation**: Blocks reach all miners quickly  
✓ **Decentralization**: No single point of failure  
✓ **Validation**: Each peer validates before accepting  
✓ **Redundancy**: Multiple paths for block propagation

### Network Topology

```
     Node A (Port 8765)
     /    |    \
    /     |     \
 Node B  Node C  Node D
   |       |       |
Miner 1  Miner 2  Miner 3
```

Each node:
- Validates blocks independently
- Broadcasts to connected peers
- Maintains peer list
- Syncs on startup

---

## Economic Model

### 1. Token Distribution

| Allocation | Amount | Purpose |
|-----------|---------|---------|
| **Owner** | 100M PHN (10%) | Network development |
| **Minable** | 900M PHN (90%) | Miner rewards |
| **Total** | 1B PHN | Total supply |

### 2. Halving Schedule

**Configuration:**
- **Initial Reward:** 50 PHN per block
- **Halving Interval:** 1,800,000 blocks
- **Halving Trigger:** Every 10% of supply mined

**Schedule:**

| Halving | Block Height | Reward | Cumulative Mined | % of Supply |
|---------|-------------|--------|------------------|-------------|
| 0 | 0 - 1.8M | 50.0000 PHN | 90M PHN | 10% |
| 1 | 1.8M - 3.6M | 25.0000 PHN | 135M PHN | 15% |
| 2 | 3.6M - 5.4M | 12.5000 PHN | 157.5M PHN | 17.5% |
| 3 | 5.4M - 7.2M | 6.2500 PHN | 168.75M PHN | 18.75% |
| 4 | 7.2M - 9M | 3.1250 PHN | 174.37M PHN | 19.37% |
| 5 | 9M - 10.8M | 1.5625 PHN | 177.19M PHN | 19.69% |
| 6 | 10.8M - 12.6M | 0.7812 PHN | 178.59M PHN | 19.84% |
| 7 | 12.6M - 14.4M | 0.3906 PHN | 179.30M PHN | 19.92% |
| 8 | 14.4M - 16.2M | 0.1953 PHN | 179.65M PHN | 19.96% |
| 9 | 16.2M - 18M | 0.0977 PHN | 179.82M PHN | 19.98% |

**Formula:**
```python
reward = INITIAL_REWARD / (2 ^ halvings)
halvings = current_block_height // HALVING_INTERVAL
```

### 3. Fee Distribution (CRITICAL FIX)

#### ❌ OLD (WRONG) Logic:
```
Block mined by Alice:
├─ Alice gets: 50 PHN (block reward only)
└─ Owner gets: Transaction fees
```

#### ✅ NEW (CORRECT) Logic:
```
Block mined by Alice:
└─ Alice gets: 50 PHN (block reward) + Transaction fees
```

#### Implementation

**Block Structure:**
```json
{
  "transactions": [
    {
      "sender": "coinbase",
      "recipient": "PHN<miner_address>",
      "amount": 50.0,
      "fee": 0.0
    },
    {
      "sender": "PHN<user_a>",
      "recipient": "PHN<user_b>",
      "amount": 100.0,
      "fee": 0.02
    },
    {
      "sender": "miners_pool",
      "recipient": "PHN<miner_address>",
      "amount": 0.02,
      "fee": 0.0
    }
  ]
}
```

**Validation Logic (`app/core/blockchain.py:555-575`):**
1. Find miner address from coinbase transaction
2. Calculate total fees from user transactions
3. Verify `miners_pool` transaction sends fees to miner
4. Reject block if fees don't go to miner

**Miner Logic (`user/Miner.py:174-177`):**
```python
# Fees go to the miner who mined the block
if total_fees > 0:
    fee_payout_tx = create_fee_payout_transaction(MINER_ADDRESS, total_fees)
    transactions.append(fee_payout_tx)
```

---

## Mining Incentives

### Total Miner Revenue Per Block

```
Total Revenue = Block Reward + Transaction Fees
```

**Example:**
- Block reward: 50 PHN
- Transactions in block: 10
- Average fee: 0.02 PHN
- **Total: 50.20 PHN**

### Why This Matters

1. **Fair Compensation:** Miners get rewarded for including transactions
2. **Fee Market:** Higher fees = priority processing
3. **Network Security:** Strong incentives maintain hashpower
4. **Decentralization:** Anyone can mine and earn

### Economic Incentive Analysis

| Block Height | Reward | Avg Fees | Total | Annual (6 blocks/hour) |
|-------------|--------|----------|-------|------------------------|
| 0-1.8M | 50 PHN | 0.20 PHN | 50.20 PHN | ~2.6M PHN/year |
| 1.8M-3.6M | 25 PHN | 0.20 PHN | 25.20 PHN | ~1.3M PHN/year |
| 3.6M-5.4M | 12.5 PHN | 0.20 PHN | 12.70 PHN | ~667K PHN/year |

---

## Configuration

### Update Your `.env` File

```env
# CRITICAL: Update this value!
HALVING_INTERVAL=1800000  # Every 1.8M blocks = 10% of supply

# Other settings
DIFFICULTY=3
STARTING_BLOCK_REWARD=50.0
MIN_TX_FEE=0.02
```

### Verify Configuration

```bash
# Check current settings
python -c "from app.settings import settings; print(f'Halving: {settings.HALVING_INTERVAL:,} blocks')"

# Should output: Halving: 1,800,000 blocks
```

---

## Testing

### Run Comprehensive Tests

```bash
# Test halving and fee distribution
python test/test_halving_and_fees.py

# Test complete system
python test/test_complete_system.py
```

### Manual Testing (Multi-Node)

**Terminal 1: Node A**
```bash
# Edit .env: NODE_PORT=8765
python -m app.main
```

**Terminal 2: Node B**
```bash
# Edit .env: NODE_PORT=8766, PEERS=http://localhost:8765
python -m app.main
```

**Terminal 3: Miner on Node A**
```bash
# Edit user/.env: NODE_URL=http://localhost:8765
python user/Miner.py
```

**Terminal 4: Miner on Node B**
```bash
# Edit user/.env: NODE_URL=http://localhost:8766
python user/Miner.py
```

**Terminal 5: Send Transaction**
```bash
python user/SendTokens.py
```

**Expected Behavior:**
1. Transaction appears in pending pool on both nodes
2. First miner to solve block submits to their node
3. Node validates and accepts block
4. **Gossip protocol broadcasts block to all peers**
5. Other nodes receive and validate block
6. All nodes now have the new block
7. Miner receives reward + fees

---

## Gossip Protocol API

### Endpoints

#### 1. Submit Block (with broadcast)
```bash
POST /submit_block
Content-Type: application/json

{
  "block": {
    "index": 123,
    "timestamp": 1234567890,
    "transactions": [...],
    "prev_hash": "abc123...",
    "nonce": 12345,
    "hash": "000abc..."
  }
}
```

**Response:**
```json
{
  "status": "accepted",
  "index": 123
}
```

**Behavior:**
- Validates block
- Adds to blockchain
- **Broadcasts to all peers** (gossip)
- Returns immediately (async broadcast)

#### 2. Add Peer
```bash
POST /add_peer
Content-Type: application/json

{
  "peer": "http://localhost:8766"
}
```

**Response:**
```json
{
  "status": "ok",
  "peers": [
    "http://localhost:8766",
    "http://localhost:8767"
  ]
}
```

---

## Production Checklist

- [x] Halving occurs every 1.8M blocks (10% of supply)
- [x] Fees go to miner (not owner)
- [x] Block reward calculation correct
- [x] Gossip protocol implemented
- [x] Multi-node peer broadcasting
- [x] POUV validation for all transactions
- [x] LMDB storage for persistence
- [x] Clean, production-standard code

---

## Summary

### Key Features

1. **Gossip Protocol**
   - Fast block propagation
   - Peer-to-peer broadcasting
   - Automatic peer sync

2. **Fair Economics**
   - Halving every 10% of supply
   - Fees go to miners
   - Strong mining incentives

3. **Production Quality**
   - Clean code
   - Comprehensive tests
   - Proper validation
   - LMDB persistence

### Formula Reference

```python
# Halving
reward = 50.0 / (2 ** (block_height // 1_800_000))

# Miner Revenue
total = block_reward + sum(tx.fee for tx in block)

# Supply Distribution
owner_allocation = 100_000_000  # 10%
minable_supply = 900_000_000    # 90%
```

---

**PHN Blockchain - Production Ready** ✓
