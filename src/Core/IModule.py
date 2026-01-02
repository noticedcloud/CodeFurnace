from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
class IModule(ABC):
    """
    Interface for CodeFurnace modules (Exploits, Payloads, etc.)
    """
    @property
    @abstractmethod
    def type(self) -> str:
        """Module type: 'exploit', 'payload', 'auxiliary'"""
        pass
    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """
        Returns metadata about the module.
        Expected keys: 'name', 'author', 'description', 'version', 'ai_commands'
        """
        pass
    @abstractmethod
    def get_options(self) -> Dict[str, Any]:
        """Returns a dictionary of configurable options (key: default_value/description)"""
        pass
    @abstractmethod
    def set(self, options: Dict[str, str]) -> None:
        """Sets module options"""
        pass
    @abstractmethod
    def exploit(self) -> None:
        """The main entry point for execution"""
        pass
    def check(self) -> bool:
        """Verify target vulnerability (optional)"""
        return True
    def payload_gen(self, command: str) -> None:
        """Optional payload generation"""
        pass
    def exec(self, command: str) -> Any:
        """Arbitrary command execution handling"""
        pass
