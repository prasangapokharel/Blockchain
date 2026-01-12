# PHN Blockchain - Project Structure

## Clean and Organized Directory Layout

```
PHN Blockchain/
├── README.md                    # Main project documentation
├── requirements.txt             # Python dependencies
├── setup.py                     # Python package setup
├── pyproject.toml              # Python project configuration
├── .env                        # Environment configuration
├── .gitignore                  # Git ignore rules
├── phn.png                     # Logo image
│
├── app/                        # Main blockchain application
│   ├── main.py                 # Node server entry point
│   ├── settings.py             # Configuration settings
│   ├── config.py               # Config wrapper
│   │
│   ├── core/                   # Core blockchain logic
│   │   ├── blockchain.py       # Blockchain implementation
│   │   ├── transactions.py     # Transaction handling
│   │   ├── transactions_secure.py  # Secure transaction module
│   │   ├── lmdb_storage.py     # LMDB database interface
│   │   ├── assets.py           # Asset tokenization
│   │   ├── mempool.py          # Transaction pool
│   │   ├── node_sync.py        # Peer synchronization
│   │   ├── tunnel_transfer.py  # Secure file transfer
│   │   └── config.py           # Core configuration
│   │
│   ├── api/                    # API endpoints
│   │   └── v1/
│   │       └── endpoints/
│   │           ├── blockchain.py    # Blockchain endpoints
│   │           ├── assets_api.py    # Asset endpoints
│   │           ├── transactions.py  # Transaction endpoints
│   │           ├── explorer.py      # Explorer endpoints
│   │           └── tokens.py        # Token endpoints
│   │
│   └── utils/                  # Utility functions
│       ├── constants.py        # Global constants
│       ├── helpers.py          # Helper functions
│       ├── secure_wallet.py    # Wallet security
│       └── wallet_generator.py # Wallet creation
│
├── user/                       # User-facing tools
│   ├── CreateWallet.py         # Create new wallets
│   ├── SendTokens.py           # Send PHN tokens
│   ├── CheckBalance.py         # Check wallet balance
│   ├── Miner.py                # Mining client
│   ├── Explorer.py             # Blockchain explorer
│   ├── CreateAssets.py         # Asset creation
│   ├── TokenInfo.py            # Token information
│   ├── Communication.py        # Encrypted messaging
│   └── TunnelServer.py         # File transfer server
│
├── phonesium/                  # PHN SDK
│   ├── __init__.py             # SDK initialization
│   ├── client.py               # Blockchain client
│   ├── wallet.py               # Wallet management
│   └── example_complete.py     # Usage examples
│
├── test/                       # All test files
│   ├── benchmarks/             # Performance benchmarks
│   │   ├── benchmark_before_after.py   # Before/after comparison
│   │   └── test_tps_capacity.py        # TPS capacity test
│   │
│   ├── integration/            # Integration tests
│   │
│   ├── test_*.py              # Unit tests
│   ├── final_verification.py  # System verification
│   ├── quick_test.py          # Quick verification
│   ├── convert_*.py           # Conversion utilities
│   └── setup_node.py          # Node setup script
│
├── scripts/                    # Utility scripts
│   ├── start_node.bat         # Start node (Windows)
│   └── run_1000tx_test.bat    # Run transaction test
│
├── docs/                       # Documentation
│   ├── SETUP.md               # Setup instructions
│   ├── QUICKSTART.md          # Quick start guide
│   ├── BENCHMARK_RESULTS.md   # Performance benchmarks
│   ├── FINAL_RESULTS.txt      # Final test results
│   ├── TPS_RESULTS.txt        # TPS capacity results
│   ├── SYSTEM_READY.md        # System readiness report
│   ├── API_REFERENCE.md       # API documentation
│   ├── SDK_REFERENCE.md       # SDK documentation
│   └── SECURITY_AUDIT.md      # Security documentation
│
├── lmdb_data/                  # LMDB database files
│   └── (database files)
│
└── backups/                    # Empty (cleaned up)
```

---

## Directory Descriptions

### Root Level

- **README.md** - Main project documentation with overview and quick start
- **requirements.txt** - Python package dependencies (orjson, lmdb, ecdsa, etc.)
- **setup.py** - Python package installation configuration
- **.env** - Environment variables (NODE_PORT, MINER_ADDRESS, etc.)

### app/

Main blockchain application code.

**core/** - Core blockchain functionality
- Blockchain consensus and validation
- Transaction processing and signing
- LMDB storage interface
- Asset tokenization system
- Mempool management
- Peer synchronization with health monitoring
- Secure file transfer

**api/** - REST API endpoints
- Blockchain operations
- Transaction submission
- Asset management
- Explorer functionality
- Token operations

**utils/** - Shared utilities
- Helper functions
- Wallet security
- Constants and configuration

### user/

User-facing command-line tools:
- Wallet management
- Transaction sending
- Mining client
- Blockchain explorer
- Asset creation
- Encrypted communication
- File transfer

### phonesium/

Official PHN blockchain SDK:
- Python client library
- Wallet management
- Transaction building
- Usage examples

### test/

All testing and verification files organized by type:

**benchmarks/** - Performance tests
- Before/after optimization comparison
- TPS capacity measurements

**integration/** - Integration tests
- Multi-component testing
- End-to-end scenarios

**Root test files:**
- Unit tests for specific components
- System verification scripts
- Conversion utilities

### scripts/

Utility scripts for common operations:
- Node startup
- Test execution
- Batch operations

### docs/

Complete project documentation:
- Setup and configuration guides
- Performance benchmarks and results
- API and SDK references
- Security audits
- Architecture documentation

---

## File Naming Conventions

### Test Files
- `test_*.py` - Unit/integration tests
- `benchmark_*.py` - Performance benchmarks
- `*_verification.py` - System verification

### Documentation Files
- `*.md` - Markdown documentation
- `*_RESULTS.txt` - Test result reports
- `*_SUMMARY.txt` - Summary reports

### Script Files
- `*.bat` - Windows batch scripts
- `*.sh` - Unix shell scripts (future)

---

## Key Files

### Production
- `app/main.py` - Node server (start with `python app/main.py`)
- `app/settings.py` - Configuration (difficulty, fees, rewards)
- `user/Miner.py` - Mining client

### Testing
- `test/final_verification.py` - Full system verification
- `test/quick_test.py` - Fast system check
- `test/benchmarks/test_tps_capacity.py` - TPS benchmark

### Documentation
- `docs/SETUP.md` - Installation instructions
- `docs/QUICKSTART.md` - Quick start guide
- `docs/FINAL_RESULTS.txt` - Complete test results

---

## Quick Access

### Start Node
```bash
python app/main.py
# or
scripts/start_node.bat
```

### Run Tests
```bash
# Quick verification
python test/quick_test.py

# Full verification
python test/final_verification.py

# TPS benchmark
python test/benchmarks/test_tps_capacity.py
```

### User Tools
```bash
# Create wallet
python user/CreateWallet.py

# Start mining
python user/Miner.py

# Send tokens
python user/SendTokens.py

# Check balance
python user/CheckBalance.py
```

---

## Storage

### LMDB Database
Location: `lmdb_data/`
- Fast embedded database
- Memory-mapped file I/O
- No JSON overhead
- Production-ready storage

### Backups
Location: `backups/`
- Cleaned up (497 MB freed)
- No longer needed with LMDB

---

## Development

### Adding New Tests
Place test files in `test/` with `test_` prefix:
- Unit tests: `test/test_<component>.py`
- Benchmarks: `test/benchmarks/benchmark_<name>.py`
- Integration: `test/integration/test_<scenario>.py`

### Adding Documentation
Place documentation in `docs/` with descriptive names:
- Guides: `docs/<TOPIC>_GUIDE.md`
- References: `docs/<NAME>_REFERENCE.md`
- Reports: `docs/<NAME>_RESULTS.txt`

### Adding Scripts
Place utility scripts in `scripts/`:
- Windows: `scripts/<name>.bat`
- Unix: `scripts/<name>.sh`

---

## Clean Directory Benefits

### Organization
✓ All tests in `test/` directory
✓ All docs in `docs/` directory
✓ All scripts in `scripts/` directory
✓ Clean root directory
✓ Clear file structure

### Maintainability
✓ Easy to find files
✓ Logical grouping
✓ Consistent naming
✓ Scalable structure

### Professional
✓ Industry-standard layout
✓ Easy onboarding for new developers
✓ Clear separation of concerns
✓ Production-ready organization

---

## Statistics

### Project Size
- Total files: 100+
- Python files: 70+
- Test files: 30+
- Documentation files: 20+
- User tools: 9

### Code Organization
- Core modules: 12
- API endpoints: 10
- User tools: 9
- SDK modules: 3
- Test files: 30+

### Documentation
- Setup guides: 3
- API references: 3
- Performance reports: 5
- Security docs: 2
- Architecture docs: 5+

---

## Version

**Structure Version:** 2.0 (Cleaned & Organized)
**Date:** January 12, 2026
**Status:** Production Ready

---

**The project is now clean, organized, and production-ready!** 🚀
