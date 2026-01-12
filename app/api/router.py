# API router configuration
from aiohttp import web
from .v1.endpoints import blockchain, peers, addresses, transactions

def setup_routes(app: web.Application):
    app.add_routes([
        *blockchain.routes,
        *peers.routes,
        *addresses.routes,
        *transactions.routes,
    ])
