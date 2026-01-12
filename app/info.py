#!/usr/bin/env python3
"""
Token Information Module
Provides functions to get and display token information
"""

import orjson
from app.core.blockchain import get_balance, calculate_total_mined, load_owner_address
from app.settings import settings

def get_token_info():
    """Get comprehensive token information"""
    total_mined = calculate_total_mined()
    supply_left = settings.TOTAL_SUPPLY - total_mined
    company_holdings = get_balance(load_owner_address())
    
    return {
        "name": settings.TOKEN_NAME,
        "symbol": settings.TOKEN_SYMBOL,
        "total_supply": settings.TOTAL_SUPPLY,
        "company_holdings": company_holdings,
        "circulating_supply": total_mined,
        "supply_left": supply_left,
        "current_block_reward": settings.STARTING_BLOCK_REWARD,
        "difficulty": settings.DIFFICULTY,
        "owner_address": load_owner_address(),
        "logo_url": settings.LOGO_URL
    }

def display_token_info():
    """Display token information in a formatted way"""
    info = get_token_info()
    
    print("=" * 50)
    print(f"TOKEN INFORMATION - {info['name']} ({info['symbol']})")
    print("=" * 50)
    print(f"Total Supply:      {info['total_supply']:,.6f} {info['symbol']}")
    print(f"Circulating:       {info['circulating_supply']:,.6f} {info['symbol']}")
    print(f"Supply Left:       {info['supply_left']:,.6f} {info['symbol']}")
    print(f"Company Holdings:  {info['company_holdings']:,.6f} {info['symbol']}")
    print(f"Block Reward:      {info['current_block_reward']:,.6f} {info['symbol']}")
    print(f"Difficulty:        {info['difficulty']}")
    print(f"Owner Address:     {info['owner_address']}")
    if info['logo_url']:
        print(f"Logo URL:          {info['logo_url']}")
    print("=" * 50)
    
    return info

def get_token_stats():
    """Get basic token statistics"""
    info = get_token_info()
    circulation_percentage = (info['circulating_supply'] / info['total_supply']) * 100
    
    return {
        "circulation_percentage": circulation_percentage,
        "tokens_mined": info['circulating_supply'],
        "tokens_remaining": info['supply_left'],
        "company_percentage": (info['company_holdings'] / info['total_supply']) * 100 if info['total_supply'] > 0 else 0
    }

if __name__ == "__main__":
    from app.core.blockchain import load_blockchain, load_address_book
    from app.utils.constants import blockchain
    
    print("Loading blockchain data...")
    load_blockchain()
    load_address_book()
    
    # Display token information
    token_info = display_token_info()
    
    # Display additional stats
    stats = get_token_stats()
    print(f"\nADDITIONAL STATISTICS:")
    print(f"Circulation Rate:  {stats['circulation_percentage']:.2f}%")
    print(f"Company Holdings:  {stats['company_percentage']:.2f}%")
    
    # Save to JSON file for external use
    with open("token_info.json", "wb") as f:
        f.write(orjson.dumps(token_info, option=orjson.OPT_INDENT_2))
    print(f"\nToken info saved to token_info.json")
