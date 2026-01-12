# PHN Blockchain - Easy Setup Guide

## Quick Start (3 Simple Steps!)

### Step 1: Create Virtual Environment
```bash
cd C:\Users\godsu\Desktop\Blockchain
python -m venv venv
```

### Step 2: Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Step 3: Install Requirements
```bash
pip install -r requirements.txt
```

---

## Run the Blockchain Node

```bash
python app/main.py
```

That's it! Your PHN Blockchain node is now running on `http://localhost:8545`

---

## What You Get

✅ **Fast LMDB Storage** - Production-ready embedded database  
✅ **High Performance** - orjson serialization (2-3x faster)  
✅ **Distributed Network** - Multi-node sync with failure recovery  
✅ **Complete API** - 37+ endpoints for blockchain operations  
✅ **Asset Tokenization** - Gold, land, real estate, custom tokens  
✅ **Secure** - ECDSA signatures, replay attack protection  

---

## Node Configuration

Edit `.env` file to configure your node:

```env
NODE_HOST=0.0.0.0
NODE_PORT=8545
NODE_NAME=PHN-Node-1
NETWORK_ID=phn-mainnet
```

---

## Multi-Node Setup (High Availability)

### Node 1 (Main):
```bash
# .env
NODE_PORT=8545
```

### Node 2 (Backup):
```bash
# .env
NODE_PORT=8546
PEERS=http://localhost:8545
```

### Node 3 (Backup):
```bash
# .env
NODE_PORT=8547
PEERS=http://localhost:8545,http://localhost:8546
```

**Result:** If any node fails, the network continues! Automatic sync and recovery.

---

## API Examples

### Check Balance:
```bash
curl http://localhost:8545/api/v1/balance/<address>
```

### Send Transaction:
```bash
curl -X POST http://localhost:8545/api/v1/transaction/send \
  -H "Content-Type: application/json" \
  -d '{
    "sender": "your_public_key",
    "recipient": "recipient_address", 
    "amount": 10.0,
    "fee": 0.1,
    "signature": "tx_signature"
  }'
```

### Mine Block:
```bash
curl -X POST http://localhost:8545/api/v1/mine \
  -H "Content-Type: application/json" \
  -d '{"miner_address": "your_address"}'
```

---

## Troubleshooting

### Port Already in Use:
Change `NODE_PORT` in `.env` file

### LMDB Error:
Delete `lmdb_data/` folder and restart

### Sync Issues:
Check `PEERS` in `.env` and ensure all nodes are reachable

---

## Security Features

🔒 **Transaction Security:**
- ECDSA signature verification
- Nonce-based replay protection
- Timestamp validation (1-hour window)
- Balance verification before execution

🔒 **Network Security:**
- Peer validation
- Checkpoint system (prevents deep reorgs)
- Chain verification on sync
- Mempool transaction validation

🔒 **Node Security:**
- Rate limiting
- DDoS protection
- Secure peer communication
- Automatic bad peer removal

---

## Performance

- **Mining Speed:** 120,000 H/s average
- **Block Time:** ~10 seconds (configurable)
- **TPS:** ~1000 transactions/second
- **Storage:** LMDB (very fast, no external DB needed)
- **Serialization:** orjson (2-3x faster than json)

---

## Support

- GitHub: https://github.com/prasangapokharel/Blockchain
- Docs: See `docs/` folder
- API Reference: `README.md`

---

## License

MIT License - See LICENSE file
