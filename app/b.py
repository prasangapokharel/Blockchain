import orjson
import os
from typing import Dict, List

def load_blockchain_data() -> List[Dict]:
    """Load blockchain data from backup file"""
    blockchain_path = os.path.join("backups", "blockchain.json")
    try:
        with open(blockchain_path, "rb") as f:
            return ororjson.loads(f.read())
    except FileNotFoundError:
        print(f"Blockchain file not found at {blockchain_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing blockchain JSON: {e}")
        return []

def calculate_address_balance(address: str, blockchain_data: List[Dict]) -> float:
    """Calculate balance for a specific address by going through all transactions"""
    balance = 0.0
    transaction_count = 0
    
    print(f"\nCalculating balance for address: {address}")
    print("=" * 80)
    
    for block in blockchain_data:
        block_index = block.get('index', 0)
        transactions = block.get('transactions', [])
        
        for tx in transactions:
            sender = tx.get('sender', '')
            recipient = tx.get('recipient', '')
            amount = float(tx.get('amount', 0))
            fee = float(tx.get('fee', 0))
            txid = tx.get('txid', '')[:16] + "..."  # Shortened for display
            
            # Check if this address received tokens
            if recipient == address:
                balance += amount
                transaction_count += 1
                print(f"Block {block_index:2d}: +{amount:12.6f} PHN (received) - TX: {txid}")
            
            # Check if this address sent tokens
            if sender == address:
                balance -= amount
                balance -= fee  # Subtract transaction fee
                transaction_count += 1
                print(f"Block {block_index:2d}: -{amount:12.6f} PHN (sent) - TX: {txid}")
                if fee > 0:
                    print(f"Block {block_index:2d}: -{fee:12.6f} PHN (fee) - TX: {txid}")
    
    print("=" * 80)
    print(f"Total transactions involving this address: {transaction_count}")
    print(f"Final balance: {balance:.6f} PHN")
    
    return balance

def get_company_address() -> str:
    """Get the company address from address book"""
    address_book_path = os.path.join("backups", "address_book.json")
    try:
        with open(address_book_path, "rb") as f:
            address_book = ororjson.loads(f.read())
            # Find the company address (PHNc23f3f4b493f342a19d88167ea98d54ddd99a47e)
            for short_addr, full_addr in address_book.items():
                if short_addr == "PHNc23f3f4b493f342a19d88167ea98d54ddd99a47e":
                    return full_addr
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading address book: {e}")
    
    # Return the known company address if address book fails
    return "380c6104c2e761dcaed07008309e11429918180def901c180e879af9a6d04ff4eed9e83476b5daceeb8f2e575361cfba696a8610cb03a7824e640038ee30056c"

def main():
    """Main function to calculate and display company balance"""
    print("PHN BLOCKCHAIN BALANCE CALCULATOR")
    print("=" * 50)
    
    # Load blockchain data
    blockchain_data = load_blockchain_data()
    if not blockchain_data:
        print("No blockchain data available!")
        return
    
    print(f"Loaded {len(blockchain_data)} blocks from blockchain")
    
    # Get company address
    company_address = get_company_address()
    print(f"Company address: {company_address}")
    
    # Calculate balance
    balance = calculate_address_balance(company_address, blockchain_data)
    
    # Summary
    print("\n" + "=" * 50)
    print("COMPANY BALANCE SUMMARY")
    print("=" * 50)
    print(f"Address: PHNc23f3f4b493f342a19d88167ea98d54ddd99a47e")
    print(f"Balance: {balance:.6f} PHN")
    print(f"Balance: {balance:,.2f} PHN (formatted)")
    
    # Save result to file
    result = {
        "address": company_address,
        "short_address": "PHNc23f3f4b493f342a19d88167ea98d54ddd99a47e",
        "balance": balance,
        "timestamp": blockchain_data[-1]['timestamp'] if blockchain_data else 0,
        "total_blocks": len(blockchain_data)
    }
    
    with open("company_balance.json", "wb") as f:
        f.write(orjson.dumps(result, option=orjson.OPT_INDENT_2))
    
    print(f"\nBalance calculation saved to company_balance.json")

if __name__ == "__main__":
    main()
