from typing import Dict, Optional, Tuple, Any
import asyncio
from Lib.Debugger import info, warning, error
class SessionManager:
    def __init__(self):
        self.sessions: Dict[int, Dict[str, Any]] = {}
        self.current_session_id: int = 1
    def add_session(self, reader, writer, client_info: Tuple[str, int]) -> int:
        session_id = self.current_session_id
        self.sessions[session_id] = {
            "reader": reader,
            "writer": writer,
            "address": client_info,
            "info": {},
            "active": True
        }
        info(f"New session {session_id} opened from {client_info}")
        self.current_session_id += 1
        return session_id
    def remove_session(self, session_id: int) -> None:
        if session_id in self.sessions:
            session = self.sessions[session_id]
            try:
                session["writer"].close()
            except Exception:
                pass
            del self.sessions[session_id]
            info(f"Session {session_id} closed")
    def get_session(self, session_id: int) -> Optional[Dict[str, Any]]:
        return self.sessions.get(session_id)
    def list_sessions(self) -> Dict[int, Dict[str, Any]]:
        return self.sessions
    async def broadcast(self, message: bytes) -> None:
        for session_id, session in self.sessions.items():
            try:
                session["writer"].write(message)
                await session["writer"].drain()
            except Exception as e:
                error(f"Failed to broadcast to session {session_id}: {e}")
session_manager = SessionManager()
