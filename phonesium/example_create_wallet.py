#!/usr/bin/env python3
"""
Example 1: Create a wallet and check balance

This shows how easy it is to create a wallet and check balance using phonesium package.
"""

from phonesium import Wallet, PhonesiumClient

def main():
    print("="*60)
    print("Phonesium SDK - Example 1: Create Wallet & Check Balance")
    print("="*60)
    
    # Step 1: Create a new wallet
    print("\n[1] Creating new wallet...")
    wallet = Wallet.create()
    print(f"    Address: {wallet.address}")
    print(f"    Public Key: {wallet.public_key[:20]}...")
    
    # Step 2: Save wallet
    print("\n[2] Saving wallet...")
    wallet.save("example_wallet.json")
    print("    Saved to: example_wallet.json")
    
    # Step 3: Connect to node
    print("\n[3] Connecting to PHN node...")
    client = PhonesiumClient("http://localhost:8765")
    print(f"    Connected to: {client.node_url}")
    
    # Step 4: Check balance
    print("\n[4] Checking balance...")
    try:
        balance = client.get_balance(wallet.address)
        print(f"    Balance: {balance} PHN")
    except Exception as e:
        print(f"    Error: {e}")
    
    # Step 5: Get token info
    print("\n[5] Getting token info...")
    try:
        info = client.get_token_info()
        print(f"    Total Supply: {info.get('total_supply', 0):,} PHN")
        print(f"    Circulating: {info.get('circulating_supply', 0):,.2f} PHN")
    except Exception as e:
        print(f"    Error: {e}")
    
    print("\n" + "="*60)
    print("Done! Your wallet is ready to use.")
    print("="*60)

if __name__ == "__main__":
    main()
