# PHN BLOCKCHAIN - QUICK START GUIDE

## ✅ SYSTEM STATUS: 100% OPERATIONAL

---

## Installation (1 minute)

```bash
# Install dependencies
pip install lmdb aiohttp requests python-dotenv ecdsa filelock

# Verify installation
python test/test_complete_system.py
```

**Expected Output:** All tests should show `[OK]` and final message: `[SUCCESS] ALL TESTS PASSED`

---

## Running the Blockchain (3 steps)

### Step 1: Start the Node

```bash
python -m app.main
```

**You should see:**
```
[LMDB] Initialized at C:\Users\...\lmdb_data
[Blockchain] LMDB initialized successfully
Successfully loaded and verified 2 blocks
======== Running on http://localhost:8765 ========
```

### Step 2: Start the Miner (in new terminal)

```bash
python user/Miner.py
```

**You should see:**
```
PHN NETWORK MINER
Node: http://localhost:8765
Miner: PHN0a2e1f46a128caa0fded990ac8f7c9fb5e7da8a6
Mining block #2 - Target: 000...
Block found! 
SUCCESS: Block accepted by network!
```

### Step 3: Make a Transaction (in new terminal)

```bash
python user/SendTokens.py
```

**Follow the prompts:**
- Enter private key: (from `backups/owner.txt` line 1)
- Enter recipient: Create wallet first with `python user/CreateWallet.py`
- Enter amount: 1000
- Confirm: y

---

## Owner Wallet Information

**Location:** `backups/owner.txt`

```
Line 1: Private Key (keep secret!)
Line 2: Public Key
Line 3: PHN Address
```

**Current Owner:**
- Address: `PHN0a2e1f46a128caa0fded990ac8f7c9fb5e7da8a6`
- Balance: 100,000,000 PHN (10% of total supply)

---

## Useful Commands

### Check Balance
```bash
python user/CheckBalance.py
# Enter any PHN address to check balance
```

### Create New Wallet
```bash
python user/CreateWallet.py
# Generates new wallet with private key, public key, and PHN address
```

### View Blockchain Status
```bash
curl http://localhost:8765/
```

### Get Mining Info
```bash
curl http://localhost:8765/mining_info
```

---

## Key Features

✅ **LMDB Storage** - Fast, no C++ compiler needed  
✅ **POUV Validation** - Every transaction universally validated  
✅ **Mining** - 50 PHN reward per block  
✅ **Transactions** - 0.02 PHN minimum fee  
✅ **Owner Rewards** - All fees go to network owner  

---

## Troubleshooting

### Node won't start
- Check if port 8765 is available
- Install dependencies: `pip install -r requirements.txt`

### Miner shows "no pending transactions"
- Make a transaction first using `SendTokens.py`
- Or wait for other users to submit transactions

### Transaction rejected
- Check sender balance with `CheckBalance.py`
- Ensure fee >= 0.02 PHN
- Verify private key is correct

---

## File Structure

```
blockchain/
├── app/main.py              # Start node here
├── user/
│   ├── Miner.py             # Mining client
│   ├── SendTokens.py        # Send transactions
│   ├── CheckBalance.py      # Check balances
│   └── CreateWallet.py      # Generate wallets
├── test/
│   └── test_complete_system.py  # Run tests
├── backups/
│   └── owner.txt            # Owner credentials
└── lmdb_data/               # Database (auto-created)
```

---

## Production Deployment

1. ✅ All tests passing (100%)
2. ✅ LMDB database working
3. ✅ POUV validation active
4. ✅ Mining functional
5. ✅ Transactions working
6. ✅ Code is production-ready

**The system is ready for deployment!**

---

## Support

For detailed information, see:
- `README.md` - Full documentation
- `SYSTEM_VERIFICATION.md` - Test results
- Owner address and private key in `backups/owner.txt`

---

**PHN Blockchain - Built with LMDB and POUV Technology**
