from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator, Optional


class BaseAgent(ABC):
    @abstractmethod
    async def astream(self, input: dict, config: dict) -> AsyncGenerator[Any, None]:
        """Invokes the agent with the given input and configuration and streams (returns) events asynchronously.
        The last event includes the final result."""
        pass


class BaseAdapter(ABC):
    @abstractmethod
    def load_agent(self, agent: Any) -> Optional[BaseAgent]:
        """Checks the type of the agent and if it is supported, returns an instance of the agent."""
        pass
