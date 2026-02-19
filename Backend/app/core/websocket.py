from fastapi import WebSocket
from typing import Dict, List
import json

class WebSocketManager:
    def __init__(self):
        # Dict de asset_id -> lista de conexiones activas
        self.connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, asset_id: int):
        await websocket.accept()
        if asset_id not in self.connections:
            self.connections[asset_id] = []
        self.connections[asset_id].append(websocket)

    def disconnect(self, websocket: WebSocket, asset_id: int):
        if asset_id in self.connections:
            self.connections[asset_id].remove(websocket)
            if not self.connections[asset_id]:
                del self.connections[asset_id]

    async def broadcast_to_asset(self, asset_id: int, data: dict):
        if asset_id not in self.connections:
            return
        dead = []
        for ws in self.connections[asset_id]:
            try:
                await ws.send_text(json.dumps(data))
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.connections[asset_id].remove(ws)

    async def broadcast_all(self, data: dict):
        for asset_id in list(self.connections.keys()):
            await self.broadcast_to_asset(asset_id, data)

ws_manager = WebSocketManager()