from abc import ABC, abstractmethod
from typing import Dict, Any
class IPayload(ABC):
    """
    Interface for CodeFurnace Payloads.
    """
    @property
    @abstractmethod
    def type(self) -> str:
        """Payload type: 'staged', 'stageless', etc."""
        pass
    @abstractmethod
    def generate(self, options: Dict[str, Any]) -> str:
        """
        Generates the payload artifact.
        Args:
            options: Dictionary containing LHOST, LPORT, etc.
        Returns:
            str: Path to the generated file.
        """
        pass
