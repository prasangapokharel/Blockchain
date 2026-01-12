from fastapi import APIRouter
from app.api.v1.endpoints import addresses, blockchain, peers, transactions, wallet

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(addresses.router, prefix="/addresses", tags=["addresses"])
api_router.include_router(blockchain.router, prefix="/blockchain", tags=["blockchain"])
api_router.include_router(peers.router, prefix="/peers", tags=["peers"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(wallet.router, prefix="/wallet", tags=["wallet"])
