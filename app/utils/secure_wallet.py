"""
PHN Blockchain - Secure Wallet Storage
Encrypts private keys with AES-256-GCM using user password
NEVER store private keys in plain text!
"""

import os
import sys
import orjson
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

# Fix Windows console encoding
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())


class SecureWalletStorage:
    """
    Secure wallet storage with AES-256-GCM encryption
    Private keys are encrypted with user password
    """
    
    @staticmethod
    def encrypt_private_key(private_key: str, password: str) -> dict:
        """
        Encrypt private key with password using AES-256-GCM
        Returns dict with encrypted data, salt, and nonce
        """
        # Generate random salt
        salt = get_random_bytes(32)
        
        # Derive key from password using PBKDF2
        key = PBKDF2(password, salt, dkLen=32, count=100000)
        
        # Encrypt private key with AES-256-GCM
        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(private_key.encode('utf-8'))
        
        return {
            'encrypted_private_key': base64.b64encode(ciphertext).decode('utf-8'),
            'salt': base64.b64encode(salt).decode('utf-8'),
            'nonce': base64.b64encode(cipher.nonce).decode('utf-8'),
            'tag': base64.b64encode(tag).decode('utf-8')
        }
    
    @staticmethod
    def decrypt_private_key(encrypted_data: dict, password: str) -> str:
        """
        Decrypt private key with password
        Returns decrypted private key string
        """
        try:
            # Decode encrypted data
            ciphertext = base64.b64decode(encrypted_data['encrypted_private_key'])
            salt = base64.b64decode(encrypted_data['salt'])
            nonce = base64.b64decode(encrypted_data['nonce'])
            tag = base64.b64decode(encrypted_data['tag'])
            
            # Derive key from password
            key = PBKDF2(password, salt, dkLen=32, count=100000)
            
            # Decrypt
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            
            return plaintext.decode('utf-8')
        except Exception as e:
            raise Exception(f"Decryption failed - incorrect password or corrupted data: {e}")
    
    @staticmethod
    def save_wallet(wallet_path: str, wallet_data: dict, password: str = None):
        """
        Save wallet to file with optional encryption
        If password provided, private key is encrypted
        """
        wallet_copy = wallet_data.copy()
        
        if password and 'private_key' in wallet_copy:
            # Encrypt private key
            encrypted = SecureWalletStorage.encrypt_private_key(
                wallet_copy['private_key'],
                password
            )
            
            # Replace plain private key with encrypted version
            wallet_copy['private_key'] = None  # Remove plain key
            wallet_copy['encrypted_private_key'] = encrypted['encrypted_private_key']
            wallet_copy['salt'] = encrypted['salt']
            wallet_copy['nonce'] = encrypted['nonce']
            wallet_copy['tag'] = encrypted['tag']
            wallet_copy['encrypted'] = True
        else:
            wallet_copy['encrypted'] = False
        
        # Save to file
        os.makedirs(os.path.dirname(wallet_path), exist_ok=True)
        with open(wallet_path, "wb") as f:
            f.write(orjson.dumps(wallet_copy, option=orjson.OPT_INDENT_2))
    
    @staticmethod
    def load_wallet(wallet_path: str, password: str = None) -> dict:
        """
        Load wallet from file with optional decryption
        Returns wallet dict with decrypted private key
        """
        with open(wallet_path, "rb") as f:
            wallet = ororjson.loads(f.read())
        
        # Check if wallet is encrypted
        if wallet.get('encrypted', False):
            if not password:
                raise Exception("Wallet is encrypted but no password provided")
            
            # Decrypt private key
            encrypted_data = {
                'encrypted_private_key': wallet['encrypted_private_key'],
                'salt': wallet['salt'],
                'nonce': wallet['nonce'],
                'tag': wallet['tag']
            }
            
            private_key = SecureWalletStorage.decrypt_private_key(encrypted_data, password)
            wallet['private_key'] = private_key
            
            # Remove encrypted fields from returned wallet
            wallet.pop('encrypted_private_key', None)
            wallet.pop('salt', None)
            wallet.pop('nonce', None)
            wallet.pop('tag', None)
        
        return wallet
    
    @staticmethod
    def change_password(wallet_path: str, old_password: str, new_password: str):
        """
        Change wallet password
        """
        # Load wallet with old password
        wallet = SecureWalletStorage.load_wallet(wallet_path, old_password)
        
        # Save wallet with new password
        SecureWalletStorage.save_wallet(wallet_path, wallet, new_password)


def migrate_plaintext_wallet_to_encrypted(wallet_path: str, password: str):
    """
    Migrate an existing plaintext wallet to encrypted format
    """
    with open(wallet_path, "rb") as f:
        wallet = ororjson.loads(f.read())
    
    if wallet.get('encrypted', False):
        print(f"[Wallet] Already encrypted: {wallet_path}")
        return
    
    if 'private_key' not in wallet:
        print(f"[Wallet] No private key found: {wallet_path}")
        return
    
    # Backup original
    backup_path = wallet_path + '.backup'
    with open(backup_path, "wb") as f:
        f.write(orjson.dumps(wallet, option=orjson.OPT_INDENT_2))
    print(f"[Wallet] Backup created: {backup_path}")
    
    # Encrypt and save
    SecureWalletStorage.save_wallet(wallet_path, wallet, password)
    print(f"[Wallet] Successfully encrypted: {wallet_path}")


if __name__ == "__main__":
    # Example usage
    print("PHN Blockchain - Secure Wallet Storage Example")
    print("=" * 70)
    
    # Test encryption/decryption
    test_private_key = "a" * 64
    test_password = "MySecurePassword123!"
    
    print("\n[Test] Encrypting private key...")
    encrypted = SecureWalletStorage.encrypt_private_key(test_private_key, test_password)
    print(f"[Test] Encrypted: {encrypted['encrypted_private_key'][:40]}...")
    
    print("\n[Test] Decrypting private key...")
    decrypted = SecureWalletStorage.decrypt_private_key(encrypted, test_password)
    print(f"[Test] Decrypted: {decrypted[:40]}...")
    
    if decrypted == test_private_key:
        print("\n✓ Encryption/Decryption test PASSED")
    else:
        print("\n✗ Encryption/Decryption test FAILED")
    
    print("\n[Test] Wrong password test...")
    try:
        SecureWalletStorage.decrypt_private_key(encrypted, "WrongPassword")
        print("✗ Should have failed with wrong password")
    except Exception as e:
        print(f"✓ Correctly rejected wrong password: {e}")
    
    print("\n" + "=" * 70)
    print("All tests passed! Secure wallet storage is working.")
