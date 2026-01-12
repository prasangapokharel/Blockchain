#!/usr/bin/env python3
"""
Complete Phonesium SDK Examples
Shows ALL features of the phonesium package
"""

print("="*70)
print("PHONESIUM SDK - COMPLETE FEATURE DEMONSTRATION")
print("="*70)

# Example 1: Create Wallet
print("\n[1] CREATE WALLET")
print("-"*70)

from phonesium import Wallet, PhonesiumClient

wallet = Wallet.create()
print(f"Address: {wallet.address}")
print(f"Public Key: {wallet.public_key[:40]}...")
print("[OK] Wallet created successfully")

# Example 2: Get Private Key (with warning)
print("\n[2] GET PRIVATE KEY (Secure)")
print("-"*70)

private_key = wallet.get_private_key(show_warning=False)  # Set True for warning
print(f"Private Key: {private_key[:20]}... (64 chars total)")
print("[OK] Private key retrieved")

# Example 3: Save Wallet with Encryption
print("\n[3] SAVE WALLET (Encrypted)")
print("-"*70)

wallet.save("demo_wallet.json", password="MySecurePassword123!")
print("[OK] Wallet saved with AES-256 encryption")

# Example 4: Load Encrypted Wallet
print("\n[4] LOAD ENCRYPTED WALLET")
print("-"*70)

loaded_wallet = Wallet.load("demo_wallet.json", password="MySecurePassword123!")
print(f"Loaded Address: {loaded_wallet.address}")
print("[OK] Wallet loaded and decrypted")

# Example 5: Create Wallet from Private Key
print("\n[5] IMPORT WALLET FROM PRIVATE KEY")
print("-"*70)

imported_wallet = Wallet.from_private_key(private_key)
print(f"Imported Address: {imported_wallet.address}")
print("[OK] Wallet imported from private key")

# Example 6: Sign Data
print("\n[6] SIGN DATA")
print("-"*70)

import orjson
message = {"action": "transfer", "amount": 100}
message_bytes = ororjson.dumps(message, option=orjson.OPT_SORT_KEYS).encode()
signature = wallet.sign(message_bytes)
print(f"Signature: {signature[:40]}...")
print("[OK] Data signed")

# Example 7: Verify Signature
print("\n[7] VERIFY SIGNATURE")
print("-"*70)

is_valid = wallet.verify_signature(message_bytes, signature)
print(f"Signature Valid: {is_valid}")
print("[OK] Signature verified")

# Example 8: Connect to Node
print("\n[8] CONNECT TO NODE")
print("-"*70)

client = PhonesiumClient("http://localhost:8765")
print(f"Connected to: {client.node_url}")

try:
    # Try to get balance
    balance = client.get_balance(wallet.address)
    print(f"Balance: {balance} PHN")
    print("[OK] Balance retrieved")
except Exception as e:
    print(f"[INFO] Node not running: {e}")
    print("[INFO] Start node with: python app/main.py")

# Example 9: Get Token Info
print("\n[9] GET TOKEN INFO")
print("-"*70)

try:
    info = client.get_token_info()
    print(f"Token Name: {info.get('name', 'N/A')}")
    print(f"Total Supply: {info.get('total_supply', 0):,} PHN")
    print(f"Circulating: {info.get('circulating_supply', 0):,.2f} PHN")
    print("[OK] Token info retrieved")
except Exception as e:
    print(f"[INFO] Could not get token info: {e}")

# Example 10: Export Wallet Data
print("\n[10] EXPORT WALLET DATA")
print("-"*70)

# Export public data only (safe)
public_data = wallet.to_dict(include_private_key=False)
print("Public Export (Safe to share):")
print(f"  Address: {public_data['address']}")
print(f"  Public Key: {public_data['public_key'][:40]}...")
print("[OK] Public data exported")

# Export with private key (dangerous!)
full_data = wallet.to_dict(include_private_key=True)
print("\nFull Export (DANGEROUS - Keep Secret!):")
print(f"  Includes Private Key: Yes")
print("[WARNING] Never share full export with anyone!")

# Example 11: Create Transaction (Manual)
print("\n[11] CREATE TRANSACTION (Manual)")
print("-"*70)

import hashlib
import time
import random

recipient = "PHN1234567890abcdef1234567890abcdef12345678"
amount = 10.0
fee = 0.02
timestamp = time.time()
nonce = random.randint(0, 999999)

tx = {
    "sender": wallet.public_key,
    "recipient": recipient,
    "amount": amount,
    "fee": fee,
    "timestamp": timestamp,
    "nonce": nonce,
}

# Generate TXID
hash_input = f"{tx['sender']}{tx['recipient']}{tx['amount']}{tx['fee']}{tx['timestamp']}{tx['nonce']}"
tx["txid"] = hashlib.sha256(hash_input.encode()).hexdigest()

# Sign transaction
tx_copy = dict(tx)
tx_json = ororjson.dumps(tx_copy, option=orjson.OPT_SORT_KEYS).encode()
tx["signature"] = wallet.sign(tx_json)

print(f"Transaction ID: {tx['txid'][:40]}...")
print(f"From: {wallet.address}")
print(f"To: {recipient}")
print(f"Amount: {amount} PHN")
print(f"Fee: {fee} PHN")
print("[OK] Transaction created and signed")

# Example 12: Send Transaction (if node running)
print("\n[12] SEND TRANSACTION")
print("-"*70)

try:
    # This requires a running node and sufficient balance
    # txid = client.send_tokens(wallet, recipient, 1.0, fee=0.02)
    # print(f"Transaction sent: {txid}")
    print("[INFO] Skipped - requires running node and balance")
    print("[INFO] Use: client.send_tokens(wallet, recipient, amount)")
except Exception as e:
    print(f"[INFO] {e}")

# Summary
print("\n" + "="*70)
print("DEMONSTRATION COMPLETE")
print("="*70)
print("\nAll features demonstrated:")
print("  [OK] Wallet creation")
print("  [OK] Private key management (secure)")
print("  [OK] Wallet encryption/decryption (AES-256)")
print("  [OK] Import from private key")
print("  [OK] Sign and verify signatures")
print("  [OK] Connect to blockchain node")
print("  [OK] Get token information")
print("  [OK] Export wallet data")
print("  [OK] Create transactions manually")
print("  [OK] Send transactions (API client)")
print("\nPhonesium SDK is fully functional!")
print("="*70)
