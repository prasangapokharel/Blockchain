import os
from pathlib import Path
from dotenv import load_dotenv
from typing import List

load_dotenv()

class Settings:
    def __init__(self):
        # Network
        self.NODE_HOST: str = os.getenv("NODE_HOST", "localhost")
        self.NODE_PORT: int = int(os.getenv("NODE_PORT", "8765"))
        peers_str = os.getenv("PEERS", "")
        self.PEERS: List[str] = [p.strip() for p in peers_str.split(",") if p.strip()] if peers_str else []

        # Files - Updated for LMDB and removed address book
        self.BACKUP_DIR: str = os.getenv("BACKUP_DIR", "backups")
        self.OWNER_FILE: str = os.getenv("OWNER_FILE", "owner.txt")
        self.LMDB_DIR: str = os.getenv("LMDB_DIR", "lmdb_data")

        # Blockchain params - Halving every 10% of minable supply (90M PHN per halving)
        self.DIFFICULTY: int = int(os.getenv("DIFFICULTY", "3"))
        self.STARTING_BLOCK_REWARD: float = float(os.getenv("STARTING_BLOCK_REWARD", "50.0"))  # Initial reward
        self.HALVING_INTERVAL: int = int(os.getenv("HALVING_INTERVAL", "1800000"))  # Every 1.8M blocks = 10% of supply
        self.MIN_TX_FEE: float = float(os.getenv("MIN_TX_FEE", "0.02"))
        self.BACKUP_ON_SAVE: bool = False

        # Node metadata
        self.NODE_VERSION: str = os.getenv("NODE_VERSION", "1.0.0")
        self.API_SECRET: str = os.getenv("API_SECRET", "your-api-secret")
        self.SUPER_SECRET_KEY: str = os.getenv("SUPER_SECRET_KEY", "your-super-secret-key")

        # Token info - Updated to 1 billion total supply
        self.TOKEN_NAME: str = os.getenv("TOKENNAME", "Phonesium")
        self.TOKEN_SYMBOL: str = os.getenv("SYMBOL", "PHN")
        self.LOGO_URL: str = os.getenv("LOGOURL", "")
        self.TOTAL_SUPPLY_STR: str = os.getenv("TOTALSUPPLY", "1000000000")  # 1 billion

        # Logo path
        self.LOGO_PATH: Path = Path(__file__).parent / "phn.png"

        # Coin logo ASCII art
        self.COIN_LOGO: str = r"""
           ____  _  _ _   _  _   _ 
          |  _ \| || | \ | |/ \ | |
          | |_) | || |  \| / _ \| |
          |  __/|__   _|\  / ___ \ |
          |_|      |_|   \/ /   \_|
              PHN NETWORK NODE
        """

    def parse_supply(self, supply_str: str) -> int:
        s = supply_str.strip().upper()
        if s.endswith("M"):
            return int(float(s[:-1]) * 1_000_000)
        if s.endswith("K"):
            return int(float(s[:-1]) * 1_000)
        return int(float(s))

    @property
    def TOTAL_SUPPLY(self) -> int:
        return self.parse_supply(self.TOTAL_SUPPLY_STR)

settings = Settings()
