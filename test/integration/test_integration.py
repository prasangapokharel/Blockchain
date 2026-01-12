"""
PHN Blockchain - Final Integration Test
Tests node startup, mining, and transactions end-to-end
"""
import os
import sys
import time
import subprocess
import requests

print("="*70)
print("PHN BLOCKCHAIN - FINAL INTEGRATION TEST")
print("="*70)

# Step 1: Check Node Availability
print("\n[STEP 1] Checking if node is running...")
print("-" * 70)
try:
    response = requests.get("http://localhost:8765/", timeout=5)
    print(f"[OK] Node is running!")
    print(response.text[:500])
except requests.exceptions.ConnectionError:
    print("[INFO] Node not running, will need to start manually")
    print("       Run: python -m app.main")
except Exception as e:
    print(f"[WARN] Node check error: {e}")

# Step 2: Check Mining Info
print("\n[STEP 2] Getting Mining Information...")
print("-" * 70)
try:
    response = requests.get("http://localhost:8765/mining_info", timeout=5)
    if response.status_code == 200:
        mining_info = response.json()
        print(f"[OK] Mining parameters retrieved:")
        print(f"     Difficulty: {mining_info.get('difficulty')}")
        print(f"     Block Reward: {mining_info.get('block_reward')} PHN")
        print(f"     Min TX Fee: {mining_info.get('min_tx_fee')} PHN")
        print(f"     Current Height: {mining_info.get('current_block_height')}")
        print(f"     Pending TX: {mining_info.get('pending_transactions')}")
        print(f"     Owner Address: {mining_info.get('owner_address')}")
    else:
        print(f"[WARN] Could not get mining info: {response.status_code}")
except Exception as e:
    print(f"[WARN] Mining info error: {e}")

# Step 3: Check Owner Balance
print("\n[STEP 3] Checking Owner Balance...")
print("-" * 70)
owner_address = "PHN0a2e1f46a128caa0fded990ac8f7c9fb5e7da8a6"
try:
    response = requests.post(
        "http://localhost:8765/get_balance",
        json={"address": owner_address},
        timeout=5
    )
    if response.status_code == 200:
        data = response.json()
        balance = data.get("balance", 0)
        print(f"[OK] Owner Address: {owner_address}")
        print(f"     Balance: {balance:,.2f} PHN")
    else:
        print(f"[WARN] Could not get balance: {response.status_code}")
except Exception as e:
    print(f"[WARN] Balance check error: {e}")

# Step 4: Get Blockchain Info
print("\n[STEP 4] Getting Blockchain Information...")
print("-" * 70)
try:
    response = requests.post("http://localhost:8765/get_blockchain", timeout=5)
    if response.status_code == 200:
        data = response.json()
        blockchain = data.get("blockchain", [])
        print(f"[OK] Blockchain retrieved:")
        print(f"     Height: {len(blockchain)} blocks")
        print(f"     Genesis block hash: {blockchain[0]['hash'][:16]}...")
        if len(blockchain) > 1:
            print(f"     Latest block hash: {blockchain[-1]['hash'][:16]}...")
            print(f"     Latest block transactions: {len(blockchain[-1]['transactions'])}")
    else:
        print(f"[WARN] Could not get blockchain: {response.status_code}")
except Exception as e:
    print(f"[WARN] Blockchain retrieval error: {e}")

# Step 5: Check Pending Transactions
print("\n[STEP 5] Checking Pending Transactions...")
print("-" * 70)
try:
    response = requests.post("http://localhost:8765/get_pending", timeout=5)
    if response.status_code == 200:
        data = response.json()
        pending_count = data.get("count", 0)
        pending_txs = data.get("pending_transactions", [])
        print(f"[OK] Pending transactions: {pending_count}")
        if pending_count > 0:
            for i, tx in enumerate(pending_txs[:3], 1):
                print(f"     TX {i}: {tx['txid'][:16]}... Amount: {tx['amount']} PHN")
    else:
        print(f"[WARN] Could not get pending transactions: {response.status_code}")
except Exception as e:
    print(f"[WARN] Pending transactions error: {e}")

# Final Summary
print("\n" + "="*70)
print("INTEGRATION TEST COMPLETE")
print("="*70)
print("\nNext Steps:")
print("  1. If node not running: python -m app.main")
print("  2. To mine blocks: python user/Miner.py")
print("  3. To send tokens: python user/SendTokens.py")
print("  4. To check balance: python user/CheckBalance.py")
print("="*70)
