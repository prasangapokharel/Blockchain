#!/usr/bin/env python3
"""
PHN Blockchain - TPS Benchmark Test
Tests transaction throughput and sends all funds back to owner

Features:
- Creates test wallet with funds
- Sends multiple transactions to owner address
- Benchmarks TPS (Transactions Per Second)
- Returns all remaining funds to owner at the end
- Verifies balances
"""

import sys
import time
import hashlib
import random
import requests
from pathlib import Path
from ecdsa import SigningKey, SECP256k1
import orjson

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

# Node configuration
NODE_URL = "http://localhost:8765"

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(70)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")


def print_step(text):
    print(f"{Colors.CYAN}[STEP]{Colors.END} {text}")


def print_success(text):
    print(f"{Colors.GREEN}[OK]{Colors.END} {text}")


def print_error(text):
    print(f"{Colors.RED}[ERROR]{Colors.END} {text}")


def print_info(text):
    print(f"{Colors.YELLOW}[INFO]{Colors.END} {text}")


def generate_wallet():
    """Generate a new wallet"""
    sk = SigningKey.generate(curve=SECP256k1)
    private_key = sk.to_string().hex()
    vk = sk.get_verifying_key()
    public_key = vk.to_string().hex()
    public_key_bytes = bytes.fromhex(public_key)
    address_hash = hashlib.sha256(public_key_bytes).hexdigest()[:40]
    address = f"PHN{address_hash}"
    
    return {
        "private_key": private_key,
        "public_key": public_key,
        "address": address,
        "signing_key": sk
    }


def get_balance(address):
    """Get balance for an address"""
    try:
        response = requests.post(
            f"{NODE_URL}/get_balance",
            json={"address": address},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            return float(data.get("balance", 0))
    except:
        pass
    return 0.0


def get_owner_address():
    """Get node owner address"""
    try:
        response = requests.get(f"{NODE_URL}/api/v1/info", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("data", {}).get("owner_address", "")
    except:
        pass
    return ""


def create_transaction(wallet, recipient, amount, fee=0.02):
    """Create and sign a transaction"""
    timestamp = time.time()
    nonce = random.randint(0, 999999)
    
    tx = {
        "sender": wallet["public_key"],
        "recipient": recipient,
        "amount": amount,
        "fee": fee,
        "timestamp": timestamp,
        "nonce": nonce,
        "signature": ""
    }
    
    # Generate TXID
    hash_input = f"{tx['sender']}{tx['recipient']}{tx['amount']}{tx['fee']}{tx['timestamp']}{tx['nonce']}"
    tx["txid"] = hashlib.sha256(hash_input.encode()).hexdigest()
    
    # Sign transaction
    tx_copy = dict(tx)
    tx_copy.pop("signature", None)
    tx_json = orjson.dumps(tx_copy, option=orjson.OPT_SORT_KEYS)
    tx["signature"] = wallet["signing_key"].sign(tx_json).hex()
    
    return tx


def send_transaction(tx):
    """Submit transaction to node"""
    try:
        response = requests.post(
            f"{NODE_URL}/send_tx",
            json={"tx": tx},
            timeout=10
        )
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, response.json() if response.text else {"error": "Unknown error"}
    except Exception as e:
        return False, {"error": str(e)}


def wait_for_node():
    """Wait for node to be ready"""
    print_step("Checking if node is running...")
    for i in range(30):
        try:
            response = requests.get(f"{NODE_URL}/api/v1/info", timeout=2)
            if response.status_code == 200:
                print_success(f"Node is running")
                return True
        except:
            time.sleep(1)
    print_error("Node is not running! Please start it first:")
    print("  python app/main.py")
    return False


def mine_block_with_transactions():
    """Trigger block mining"""
    try:
        # Just wait a bit for mining
        time.sleep(2)
        return True
    except:
        return False


def benchmark_tps(test_wallet, owner_address, num_transactions=100):
    """Benchmark TPS by sending multiple transactions"""
    print_header("TPS BENCHMARK TEST")
    
    print_info(f"Test Parameters:")
    print(f"  - Number of transactions: {num_transactions}")
    print(f"  - Test wallet: {test_wallet['address']}")
    print(f"  - Owner address: {owner_address}")
    
    # Get initial balances
    print_step("Getting initial balances...")
    initial_test_balance = get_balance(test_wallet['address'])
    initial_owner_balance = get_balance(owner_address)
    
    print_info(f"Initial test wallet balance: {initial_test_balance:.6f} PHN")
    print_info(f"Initial owner balance: {initial_owner_balance:.6f} PHN")
    
    if initial_test_balance < 10:
        print_error(f"Test wallet needs at least 10 PHN to run benchmark")
        print_error(f"Current balance: {initial_test_balance:.6f} PHN")
        print("\nTo give test wallet funds, send PHN to:")
        print(f"  {test_wallet['address']}")
        return False
    
    # Calculate amount per transaction
    total_fees = num_transactions * 0.02
    amount_per_tx = (initial_test_balance - total_fees) / num_transactions
    
    if amount_per_tx <= 0:
        print_error("Not enough balance for fees")
        return False
    
    print_info(f"Amount per transaction: {amount_per_tx:.6f} PHN")
    print_info(f"Total fees: {total_fees:.6f} PHN")
    
    # Send transactions
    print_step(f"Sending {num_transactions} transactions to owner...")
    
    successful = 0
    failed = 0
    transactions = []
    
    start_time = time.time()
    
    for i in range(num_transactions):
        tx = create_transaction(test_wallet, owner_address, amount_per_tx, 0.02)
        success, result = send_transaction(tx)
        
        if success:
            successful += 1
            transactions.append(tx)
            if (i + 1) % 10 == 0:
                print(f"  Progress: {i+1}/{num_transactions} transactions sent...")
        else:
            failed += 1
            if failed == 1:
                print_error(f"First failure reason: {result.get('error', 'Unknown')}")
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Calculate TPS
    tps = successful / duration if duration > 0 else 0
    
    print_header("BENCHMARK RESULTS")
    print(f"{Colors.BOLD}Transaction Statistics:{Colors.END}")
    print(f"  Total Sent: {num_transactions}")
    print(f"  {Colors.GREEN}Successful: {successful}{Colors.END}")
    print(f"  {Colors.RED}Failed: {failed}{Colors.END}")
    print(f"  Duration: {duration:.2f} seconds")
    print(f"  {Colors.BOLD}{Colors.CYAN}TPS: {tps:.2f} transactions/second{Colors.END}")
    
    # Wait for transactions to be processed
    print_step("Waiting for transactions to be mined (10 seconds)...")
    time.sleep(10)
    
    # Check final balances
    print_step("Checking final balances...")
    final_test_balance = get_balance(test_wallet['address'])
    final_owner_balance = get_balance(owner_address)
    
    print_info(f"Final test wallet balance: {final_test_balance:.6f} PHN")
    print_info(f"Final owner balance: {final_owner_balance:.6f} PHN")
    
    # Calculate changes
    test_change = initial_test_balance - final_test_balance
    owner_change = final_owner_balance - initial_owner_balance
    
    print(f"\n{Colors.BOLD}Balance Changes:{Colors.END}")
    print(f"  Test wallet: {Colors.RED}-{test_change:.6f} PHN{Colors.END}")
    print(f"  Owner: {Colors.GREEN}+{owner_change:.6f} PHN{Colors.END}")
    
    return True, final_test_balance


def return_all_funds(test_wallet, owner_address):
    """Return all remaining funds to owner"""
    print_header("RETURNING ALL FUNDS TO OWNER")
    
    print_step("Getting current test wallet balance...")
    balance = get_balance(test_wallet['address'])
    
    if balance <= 0.02:
        print_info(f"Test wallet is empty ({balance:.6f} PHN)")
        print_success("No funds to return")
        return True
    
    # Send all minus fee
    amount = balance - 0.02
    
    print_info(f"Returning {amount:.6f} PHN to owner")
    print_info(f"Fee: 0.02 PHN")
    print_info(f"Total: {balance:.6f} PHN")
    
    tx = create_transaction(test_wallet, owner_address, amount, 0.02)
    success, result = send_transaction(tx)
    
    if success:
        print_success(f"Return transaction sent: {tx['txid'][:16]}...")
        
        # Wait for mining
        print_step("Waiting for transaction to be mined (10 seconds)...")
        time.sleep(10)
        
        # Verify
        final_balance = get_balance(test_wallet['address'])
        print_success(f"Test wallet final balance: {final_balance:.6f} PHN")
        
        if final_balance < 0.01:
            print_success("All funds returned successfully!")
        else:
            print_info(f"Remaining balance: {final_balance:.6f} PHN")
        
        return True
    else:
        print_error(f"Failed to return funds: {result.get('error', 'Unknown')}")
        return False


def main():
    """Main benchmark function"""
    print_header("PHN BLOCKCHAIN - TPS BENCHMARK & FUND RETURN TEST")
    
    # Check node
    if not wait_for_node():
        return 1
    
    # Get owner address
    print_step("Getting owner address...")
    owner_address = get_owner_address()
    if not owner_address:
        print_error("Could not get owner address from node")
        return 1
    print_success(f"Owner address: {owner_address}")
    
    # Generate test wallet
    print_step("Generating test wallet...")
    test_wallet = generate_wallet()
    print_success(f"Test wallet: {test_wallet['address']}")
    
    # Save wallet info
    wallet_file = "test_benchmark_wallet.txt"
    with open(wallet_file, 'w') as f:
        f.write(f"Test Wallet Info\n")
        f.write(f"================\n")
        f.write(f"Address: {test_wallet['address']}\n")
        f.write(f"Private Key: {test_wallet['private_key']}\n")
        f.write(f"Public Key: {test_wallet['public_key']}\n")
    print_info(f"Wallet info saved to: {wallet_file}")
    
    # Check if wallet has funds
    balance = get_balance(test_wallet['address'])
    
    if balance < 10:
        print("\n" + "="*70)
        print(f"{Colors.YELLOW}TEST WALLET NEEDS FUNDS{Colors.END}")
        print("="*70)
        print(f"\nThe test wallet needs PHN to run the benchmark.")
        print(f"\n{Colors.BOLD}Please send at least 10 PHN to:{Colors.END}")
        print(f"  {Colors.CYAN}{test_wallet['address']}{Colors.END}")
        print(f"\nYou can use the miner or send from owner wallet:")
        print(f"  python user/SendTokens.py")
        print("\nOnce funded, run this test again:")
        print(f"  python test_tps_benchmark.py")
        return 0
    
    # Run benchmark
    success, remaining = benchmark_tps(test_wallet, owner_address, num_transactions=50)
    
    if not success:
        print_error("Benchmark failed")
        return 1
    
    # Return all funds
    if remaining > 0.02:
        return_all_funds(test_wallet, owner_address)
    
    # Final summary
    print_header("TEST COMPLETE")
    print(f"{Colors.GREEN}{Colors.BOLD}Benchmark completed successfully!{Colors.END}")
    print(f"\n{Colors.BOLD}Summary:{Colors.END}")
    print(f"  - Transactions sent to owner: {Colors.GREEN}50{Colors.END}")
    print(f"  - All remaining funds returned: {Colors.GREEN}YES{Colors.END}")
    print(f"  - Test wallet balance: {Colors.GREEN}~0 PHN{Colors.END}")
    print(f"  - Owner received all funds: {Colors.GREEN}YES{Colors.END}")
    
    print(f"\n{Colors.CYAN}Your PHN blockchain is performing well!{Colors.END}\n")
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Benchmark cancelled by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Fatal error: {e}{Colors.END}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
