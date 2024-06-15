from sqlalchemy import insert, select
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from core import db_helper
from .models import Message

router = APIRouter(prefix="/chat", tags=["Chat"])


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, add_to_db: bool):
        if add_to_db:
            await self.add_message_to_database(message=message)
        for connection in self.active_connections:
            await connection.send_text(message)

    @staticmethod
    async def add_message_to_database(message: str):
        async with db_helper.session_factory() as session:
            stmt = insert(Message).values(message=message)
            await session.execute(stmt)
            await session.commit()


manager = ConnectionManager()


@router.get("/last_messages")
async def get_last_msg(session: AsyncSession = Depends(db_helper.session_dependency)):
    query = select(Message).order_by(Message.id.desc()).limit(5)
    result = await session.execute(query)
    messages = result.scalars().all()
    messages_list = [m.as_dict() for m in messages]
    return messages_list


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id} says: {data}", add_to_db=True)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat", add_to_db=False)
