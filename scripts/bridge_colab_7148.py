import asyncio
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

from colab_mcp.websocket_server import ColabWebSocketServer, COLAB, COLAB_ALT_DOMAIN
import websockets
from websockets.typing import Subprotocol

TOKEN = "VlbC0Wm7DzcfDOH4Aurnsg"
PORT = 7148

class FixedColabServer(ColabWebSocketServer):
    def __init__(self):
        super().__init__()
        self.token = TOKEN
        self.port = PORT

    async def __aenter__(self):
        self._server = await websockets.serve(
            self._connection_handler,
            host=self.host,
            port=PORT,
            subprotocols=[Subprotocol("mcp")],
            origins=self.allowed_origins,
            process_request=self._validate_authorization,
        )
        self.port = PORT
        logging.info(f"🚀 FIXED SERVER READY: ws://localhost:{PORT}")
        logging.info(f"🔑 TOKEN LOCKED: {TOKEN}")
        logging.info("👉 WAITING FOR FOUNDER TO CLICK [CONNECT] IN COLAB...")
        return self

async def run():
    server = FixedColabServer()
    async with server:
        # Wait up to 120 seconds for connection
        try:
            await asyncio.wait_for(server.connection_live.wait(), timeout=120)
            logging.info("🎉 SUCCESS! COLAB FRONTEND CONNECTED!")
            while server.connection_live.is_set():
                await asyncio.sleep(1)
        except asyncio.TimeoutError:
            logging.warning("⚠️ Timeout waiting for connection (120s)")

if __name__ == "__main__":
    asyncio.run(run())
