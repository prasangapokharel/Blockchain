# Test Directory

Comprehensive testing suite for PHN Blockchain.

## Directory Structure

```
test/
├── unit/              Unit tests for individual components
├── integration/       Integration tests for multiple components
├── performance/       Performance benchmarks and TPS tests
├── tools/            Testing utilities and verification scripts
├── conversion/       Code conversion utilities
└── utilities/        Helper utilities for testing
```

## Quick Start

### Run All Tests
```bash
# Quick verification
python test/tools/quick_test.py

# Full system verification
python test/tools/final_verification.py
```

### Run Specific Test Categories

#### Unit Tests
```bash
python test/unit/test_api_endpoints.py
python test/unit/test_encryption.py
python test/unit/test_sdk.py
```

#### Integration Tests
```bash
python test/integration/test_system.py
python test/integration/test_multi_node.py
python test/integration/test_1000_transactions.py
```

#### Performance Tests
```bash
python test/performance/benchmark_before_after.py
python test/performance/test_tps_capacity.py
```

## Test Categories

### Unit Tests (`unit/`)
Tests for individual components in isolation:
- API endpoints
- Encryption modules
- Asset management
- Communication
- SDK functionality
- Security features
- Transaction processing

### Integration Tests (`integration/`)
Tests for multiple components working together:
- Complete system tests
- Multi-node synchronization
- Transaction flow (1000+ transactions)
- TPS benchmarks
- Quick integration checks

### Performance Tests (`performance/`)
Performance benchmarks and optimization verification:
- Before/after optimization comparison
- TPS (Transactions Per Second) capacity
- Block hashing speed
- Serialization performance

### Tools (`tools/`)
Testing utilities and verification scripts:
- `quick_test.py` - Fast system verification (10 seconds)
- `final_verification.py` - Complete system check
- `setup_node.py` - Node setup and initialization

### Conversion (`conversion/`)
Code conversion utilities:
- `convert_to_orjson.py` - Convert single files
- `convert_all_to_orjson.py` - Batch conversion

## Test Results

All test results are documented in `docs/reports/`:
- `FINAL_RESULTS.txt` - Complete test results
- `TPS_RESULTS.txt` - TPS capacity results
- `BENCHMARK_RESULTS.md` - Performance benchmarks

## Running Tests

### Prerequisites
```bash
# Install dependencies
pip install -r requirements.txt

# Start node (for integration tests)
python app/main.py
```

### Test Commands
```bash
# Quick test (10 seconds)
python test/tools/quick_test.py

# Full verification
python test/tools/final_verification.py

# TPS benchmark
python test/performance/test_tps_capacity.py

# Integration test
python test/integration/test_system.py
```

## Test Coverage

- Unit Tests: 10+ tests
- Integration Tests: 6+ tests  
- Performance Tests: 2+ benchmarks
- Tools: 3+ utilities

Total: 20+ test files

## Naming Conventions

- Unit tests: `test_<component>.py`
- Integration tests: `test_<feature>_<type>.py`
- Performance tests: `benchmark_<name>.py` or `test_<name>_capacity.py`
- Tools: `<action>_<purpose>.py`

## Contributing

When adding new tests:
1. Place in appropriate subdirectory
2. Follow naming conventions
3. Add documentation in file header
4. Update this README if needed
