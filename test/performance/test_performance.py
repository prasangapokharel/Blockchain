"""
Performance test for PHN Blockchain
Tests transaction throughput (TPS)
"""
import time
import requests
import secrets
from phonesium import Wallet


def test_transaction_performance(num_transactions=100):
    """
    Test transaction creation and submission performance
    
    Args:
        num_transactions: Number of transactions to create
    """
    print(f"\n{'='*60}")
    print(f"PHN BLOCKCHAIN PERFORMANCE TEST")
    print(f"{'='*60}")
    print(f"Target: {num_transactions} transactions\n")
    
    # Create sender wallet
    print("[1/5] Creating sender wallet...")
    sender = Wallet.create()
    print(f"[OK] Sender: {sender.address}")
    
    # Create recipient wallet
    print("\n[2/5] Creating recipient wallet...")
    recipient = Wallet.create()
    print(f"[OK] Recipient: {recipient.address}")
    
    # Create transactions
    print(f"\n[3/5] Creating {num_transactions} transactions...")
    start_create = time.time()
    transactions = []
    
    for i in range(num_transactions):
        tx = sender.create_transaction(
            recipient=recipient.address,
            amount=1.0,
            fee=0.1
        )
        transactions.append(tx)
        
        if (i + 1) % 100 == 0:
            print(f"  Created {i + 1} transactions...")
    
    create_time = time.time() - start_create
    create_tps = num_transactions / create_time
    
    print(f"[OK] Created {num_transactions} transactions in {create_time:.2f}s")
    print(f"[OK] Creation rate: {create_tps:.2f} TPS")
    
    # Verify signatures
    print(f"\n[4/5] Verifying {num_transactions} signatures...")
    start_verify = time.time()
    valid_count = 0
    
    for i, tx in enumerate(transactions):
        tx_data = f"{tx['sender']}{tx['recipient']}{tx['amount']}{tx['fee']}{tx['timestamp']}{tx['nonce']}"
        if sender.verify_signature(tx_data, tx['signature']):
            valid_count += 1
        
        if (i + 1) % 100 == 0:
            print(f"  Verified {i + 1} signatures...")
    
    verify_time = time.time() - start_verify
    verify_tps = num_transactions / verify_time
    
    print(f"[OK] Verified {valid_count}/{num_transactions} signatures in {verify_time:.2f}s")
    print(f"[OK] Verification rate: {verify_tps:.2f} TPS")
    
    # Test node submission (if node is running)
    print(f"\n[5/5] Testing node submission...")
    node_url = "http://localhost:8000"
    
    try:
        # Check if node is running
        response = requests.get(f"{node_url}/info", timeout=2)
        if response.status_code == 200:
            print(f"[OK] Node is running at {node_url}")
            
            # Submit a few test transactions
            test_count = min(5, num_transactions)
            print(f"  Submitting {test_count} test transactions...")
            
            start_submit = time.time()
            success_count = 0
            
            for i in range(test_count):
                try:
                    response = requests.post(
                        f"{node_url}/send_tx",
                        json=transactions[i],
                        timeout=5
                    )
                    if response.status_code == 200:
                        success_count += 1
                    time.sleep(0.1)  # Small delay between submissions
                except Exception as e:
                    print(f"  Warning: Transaction {i+1} failed: {e}")
            
            submit_time = time.time() - start_submit
            
            print(f"[OK] Submitted {success_count}/{test_count} transactions")
            print(f"[OK] Submission time: {submit_time:.2f}s")
        else:
            print(f"[WARN] Node returned status {response.status_code}")
            print(f"  Skipping node submission test")
    
    except requests.exceptions.RequestException:
        print(f"[WARN] Node not running at {node_url}")
        print(f"  Skipping node submission test")
        print(f"  Tip: Start node with 'python app/main.py'")
    
    # Summary
    print(f"\n{'='*60}")
    print("PERFORMANCE SUMMARY")
    print(f"{'='*60}")
    print(f"Total Transactions:     {num_transactions:,}")
    print(f"Creation Time:          {create_time:.2f}s")
    print(f"Creation TPS:           {create_tps:.2f}")
    print(f"Verification Time:      {verify_time:.2f}s")
    print(f"Verification TPS:       {verify_tps:.2f}")
    print(f"Valid Signatures:       {valid_count}/{num_transactions}")
    print(f"{'='*60}\n")
    
    # Return results
    return {
        "total": num_transactions,
        "create_time": create_time,
        "create_tps": create_tps,
        "verify_time": verify_time,
        "verify_tps": verify_tps,
        "valid_signatures": valid_count
    }


def test_wallet_generation_performance(num_wallets=1000):
    """
    Test wallet creation performance
    
    Args:
        num_wallets: Number of wallets to create
    """
    print(f"\n{'='*60}")
    print(f"WALLET GENERATION PERFORMANCE TEST")
    print(f"{'='*60}")
    print(f"Target: {num_wallets} wallets\n")
    
    start = time.time()
    wallets = []
    
    for i in range(num_wallets):
        wallet = Wallet.create()
        wallets.append(wallet)
        
        if (i + 1) % 100 == 0:
            print(f"Created {i + 1} wallets...")
    
    elapsed = time.time() - start
    wps = num_wallets / elapsed
    
    print(f"\n[OK] Created {num_wallets} wallets in {elapsed:.2f}s")
    print(f"[OK] Generation rate: {wps:.2f} wallets/second")
    
    # Verify uniqueness
    addresses = [w.address for w in wallets]
    unique_addresses = len(set(addresses))
    
    print(f"[OK] Unique addresses: {unique_addresses}/{num_wallets}")
    print(f"{'='*60}\n")
    
    return {
        "total": num_wallets,
        "time": elapsed,
        "rate": wps,
        "unique": unique_addresses
    }


if __name__ == "__main__":
    import sys
    
    # Get transaction count from command line or use default
    if len(sys.argv) > 1:
        try:
            tx_count = int(sys.argv[1])
        except ValueError:
            print("Usage: python test_performance.py [num_transactions]")
            sys.exit(1)
    else:
        tx_count = 100
    
    # Run wallet generation test
    wallet_results = test_wallet_generation_performance(1000)
    
    # Run transaction performance test
    tx_results = test_transaction_performance(tx_count)
    
    print("\n[OK] All performance tests completed successfully!")
    print(f"\nTo test 10,001 transactions, run:")
    print(f"  python test/test_performance.py 10001")
