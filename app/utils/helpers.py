# helpers.py - Utility functions for Phonesium blockchain
import orjson
import os
import shutil
import hashlib
from filelock import FileLock
from app.settings import settings
import time

def atomic_write(obj, filename: str, lockfile: str):
    tmp = filename + ".tmp"
    lock = FileLock(lockfile)
    with lock:
        os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
        with open(tmp, "wb") as f:
            f.write(orjson.dumps(obj, option=orjson.OPT_INDENT_2))
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, filename)
        if settings.BACKUP_ON_SAVE:
            backup_file(filename)

def backup_file(filename: str):
    try:
        os.makedirs(settings.BACKUP_DIR, exist_ok=True)
        ts = time.strftime("%Y%m%d_%H%M%S")
        base = os.path.basename(filename)
        dest = os.path.join(settings.BACKUP_DIR, f"{base}.{ts}.bak")
        shutil.copy2(filename, dest)
    except Exception:
        pass

def load_json(filename: str):
    try:
        with open(filename, "rb") as f:
            return ororjson.loads(f.read())
    except Exception:
        return None

def hash_block(block: dict) -> str:
    b = dict(block)
    b.pop("hash", None)
    s = orjson.dumps(b, option=orjson.OPT_SORT_KEYS)
    return hashlib.sha256(s.encode()).hexdigest()
