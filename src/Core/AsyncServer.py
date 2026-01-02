import asyncio
from typing import Callable, Optional
from Lib.Debugger import info, warning, error
from Core.SessionManager import session_manager
class AsyncServer:
    def __init__(self, callback: Optional[Callable] = None):
        self.server = None
        self.callback = callback
    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        session_id = session_manager.add_session(reader, writer, addr)
        try:
            if self.callback:
                if asyncio.iscoroutinefunction(self.callback):
                    await self.callback(reader, writer)
                else:
                    self.callback(reader, writer)
            await writer.wait_closed()
        except Exception as e:
            error(f"Error in session {session_id}: {e}")
        finally:
            session_manager.remove_session(session_id)
    async def start_listener(self, host: str, port: int, ssl=None) -> None:
        try:
            self.server = await asyncio.start_server(
                self.handle_client, host, port, ssl=ssl
            )
            addr = self.server.sockets[0].getsockname()
            info(f"Async Listener started on {addr}")
            async with self.server:
                await self.server.serve_forever()
        except OSError as e:
            error(f"Failed to start listener on {host}:{port} - {e}")
        except asyncio.CancelledError:
            info("Listener stopped")
    def stop_listener(self):
        if self.server:
            self.server.close()
