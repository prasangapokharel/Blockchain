"""
Comprehensive test suite for Phonesium SDK
Tests all wallet and client functionality
"""
import pytest
import os
import tempfile
import orjson
from phonesium import Wallet, PhonesiumClient
from phonesium.exceptions import WalletError, NetworkError


class TestWalletCreation:
    """Test wallet creation and initialization"""
    
    def test_create_new_wallet(self):
        """Test creating a new wallet"""
        wallet = Wallet.create()
        assert wallet.address.startswith("PHN")
        assert len(wallet.address) == 43
        assert wallet.private_key is not None
        assert len(wallet.private_key) == 64  # 32 bytes in hex
    
    def test_multiple_wallets_unique(self):
        """Test that multiple wallets have unique addresses"""
        wallet1 = Wallet.create()
        wallet2 = Wallet.create()
        assert wallet1.address != wallet2.address
        assert wallet1.private_key != wallet2.private_key
    
    def test_wallet_from_private_key(self):
        """Test creating wallet from existing private key"""
        original = Wallet.create()
        private_key = original.get_private_key()
        
        # Create new wallet from same private key
        restored = Wallet.from_private_key(private_key)
        assert restored.address == original.address
        assert restored.get_private_key() == private_key


class TestWalletEncryption:
    """Test wallet encryption and security features"""
    
    def test_save_and_load_wallet(self):
        """Test saving and loading encrypted wallet"""
        wallet = Wallet.create()
        password = "test_password_123"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            # Save wallet
            wallet.save(temp_file, password)
            assert os.path.exists(temp_file)
            
            # Load wallet
            loaded = Wallet.load(temp_file, password)
            assert loaded.address == wallet.address
            assert loaded.get_private_key() == wallet.get_private_key()
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_wrong_password_fails(self):
        """Test that wrong password fails to decrypt"""
        wallet = Wallet.create()
        password = "correct_password"
        wrong_password = "wrong_password"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            wallet.save(temp_file, password)
            
            with pytest.raises(WalletError):
                Wallet.load(temp_file, wrong_password)
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_encrypted_file_format(self):
        """Test that saved file contains encrypted data"""
        wallet = Wallet.create()
        password = "test_password"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            wallet.save(temp_file, password)
            
            # Read raw file
            with open(temp_file, 'r') as f:
                data = orjson.loads(f.read())
            
            # Verify encryption fields exist
            assert 'private_key' in data  # Encrypted private key field
            assert 'encrypted' in data
            assert 'address' in data
            
            # Verify private key is not in plaintext
            assert wallet.get_private_key() not in orjson.dumps(data)
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)


class TestWalletSigning:
    """Test transaction signing and verification"""
    
    def test_sign_message(self):
        """Test signing a message"""
        wallet = Wallet.create()
        message = "Test transaction data"
        
        signature = wallet.sign(message)
        assert signature is not None
        assert len(signature) > 0
    
    def test_verify_valid_signature(self):
        """Test verifying a valid signature"""
        wallet = Wallet.create()
        message = "Test transaction"
        
        signature = wallet.sign(message)
        assert wallet.verify_signature(message, signature) is True
    
    def test_verify_invalid_signature(self):
        """Test that invalid signature fails verification"""
        wallet = Wallet.create()
        message = "Test message"
        wrong_signature = "invalid_signature_abc123"
        
        assert wallet.verify_signature(message, wrong_signature) is False
    
    def test_signature_tamper_detection(self):
        """Test that modified message fails verification"""
        wallet = Wallet.create()
        original_message = "Original message"
        tampered_message = "Tampered message"
        
        signature = wallet.sign(original_message)
        assert wallet.verify_signature(tampered_message, signature) is False
    
    def test_cross_wallet_signature_fails(self):
        """Test that signature from one wallet fails on another"""
        wallet1 = Wallet.create()
        wallet2 = Wallet.create()
        message = "Test message"
        
        signature = wallet1.sign(message)
        assert wallet2.verify_signature(message, signature) is False


class TestWalletExport:
    """Test wallet export functionality"""
    
    def test_export_public_data(self):
        """Test exporting wallet without private key"""
        wallet = Wallet.create()
        exported = wallet.export_wallet(include_private_key=False)
        
        assert 'address' in exported
        assert 'public_key' in exported
        assert 'private_key' not in exported
        assert exported['address'] == wallet.address
    
    def test_export_full_data(self):
        """Test exporting wallet with private key"""
        wallet = Wallet.create()
        exported = wallet.export_wallet(include_private_key=True)
        
        assert 'address' in exported
        assert 'public_key' in exported
        assert 'private_key' in exported
        assert exported['private_key'] == wallet.get_private_key()
    
    def test_export_private_key(self):
        """Test exporting private key directly"""
        wallet = Wallet.create()
        private_key = wallet.export_private_key(confirm=True)
        
        assert private_key == wallet.get_private_key()
        assert len(private_key) == 64


class TestPhonesiumClient:
    """Test API client functionality"""
    
    def test_client_initialization(self):
        """Test creating API client"""
        client = PhonesiumClient(node_url="http://localhost:8000")
        assert client.node_url == "http://localhost:8000"
    
    def test_client_custom_port(self):
        """Test client with custom port"""
        client = PhonesiumClient(node_url="http://localhost:9000")
        assert client.node_url == "http://localhost:9000"


class TestTransactionCreation:
    """Test manual transaction creation"""
    
    def test_create_transaction_dict(self):
        """Test creating transaction dictionary"""
        wallet = Wallet.create()
        recipient = "PHNrecipient123456789012345678901234567890123"
        
        tx = wallet.create_transaction(
            recipient=recipient,
            amount=100.5,
            fee=1.0
        )
        
        assert tx['sender'] == wallet.address
        assert tx['recipient'] == recipient
        assert tx['amount'] == 100.5
        assert tx['fee'] == 1.0
        assert 'timestamp' in tx
        assert 'nonce' in tx
        assert 'txid' in tx
        assert 'signature' in tx
    
    def test_transaction_signature_valid(self):
        """Test that created transaction has valid signature"""
        wallet = Wallet.create()
        recipient = "PHNrecipient123456789012345678901234567890123"
        
        tx = wallet.create_transaction(
            recipient=recipient,
            amount=50.0,
            fee=0.5
        )
        
        # Reconstruct message that was signed
        tx_data = f"{tx['sender']}{tx['recipient']}{tx['amount']}{tx['fee']}{tx['timestamp']}{tx['nonce']}"
        
        # Verify signature
        assert wallet.verify_signature(tx_data, tx['signature']) is True
    
    def test_transaction_nonce_unique(self):
        """Test that each transaction has unique nonce"""
        wallet = Wallet.create()
        recipient = "PHNrecipient123456789012345678901234567890123"
        
        tx1 = wallet.create_transaction(recipient=recipient, amount=10, fee=1)
        tx2 = wallet.create_transaction(recipient=recipient, amount=10, fee=1)
        
        assert tx1['nonce'] != tx2['nonce']
        assert tx1['txid'] != tx2['txid']


class TestWalletValidation:
    """Test validation and error handling"""
    
    def test_invalid_private_key_format(self):
        """Test that invalid private key format raises error"""
        with pytest.raises(WalletError):
            Wallet.from_private_key("invalid_key")
    
    def test_empty_private_key(self):
        """Test that empty private key raises error"""
        with pytest.raises(WalletError):
            Wallet.from_private_key("")
    
    def test_short_private_key(self):
        """Test that short private key raises error"""
        with pytest.raises(WalletError):
            Wallet.from_private_key("abc123")


class TestWalletSecurity:
    """Test security features and warnings"""
    
    def test_private_key_access_returns_string(self):
        """Test that private key is returned as string"""
        wallet = Wallet.create()
        private_key = wallet.get_private_key()
        
        assert isinstance(private_key, str)
        assert len(private_key) == 64
    
    def test_wallet_has_security_attributes(self):
        """Test that wallet has necessary security attributes"""
        wallet = Wallet.create()
        
        assert hasattr(wallet, 'address')
        assert hasattr(wallet, 'public_key')
        assert hasattr(wallet, 'private_key')
        assert hasattr(wallet, 'sign')
        assert hasattr(wallet, 'verify_signature')


# Performance tests
class TestPerformance:
    """Test SDK performance"""
    
    def test_wallet_creation_speed(self):
        """Test creating multiple wallets quickly"""
        wallets = []
        for _ in range(10):
            wallet = Wallet.create()
            wallets.append(wallet)
        
        assert len(wallets) == 10
        # Verify all unique
        addresses = [w.address for w in wallets]
        assert len(set(addresses)) == 10
    
    def test_signing_speed(self):
        """Test signing multiple messages"""
        wallet = Wallet.create()
        signatures = []
        
        for i in range(100):
            message = f"Transaction {i}"
            signature = wallet.sign(message)
            signatures.append(signature)
        
        assert len(signatures) == 100
    
    def test_verification_speed(self):
        """Test verifying multiple signatures"""
        wallet = Wallet.create()
        
        # Create 100 signed messages
        test_data = []
        for i in range(100):
            message = f"Message {i}"
            signature = wallet.sign(message)
            test_data.append((message, signature))
        
        # Verify all
        for message, signature in test_data:
            assert wallet.verify_signature(message, signature) is True


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
