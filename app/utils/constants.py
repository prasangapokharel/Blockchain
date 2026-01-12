from app.settings import settings
import os

# In-memory state
blockchain = []
pending_txs = []
peers = set(settings.PEERS)  # peers populated from settings

def load_owner_address():
    """Load owner address from owner.txt in backups folder"""
    owner_file = os.path.join("backups", "owner.txt")
    try:
        with open(owner_file, "r") as f:
            lines = f.read().splitlines()
            return lines[2].strip() if len(lines) > 2 else ""
    except (FileNotFoundError, IndexError):
        return ""

OWNER_ADDRESS = load_owner_address()
