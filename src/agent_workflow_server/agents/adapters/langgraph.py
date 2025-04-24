# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

from typing import Optional

from langchain_core.runnables import RunnableConfig
from langgraph.constants import INTERRUPT
from langgraph.graph.graph import CompiledGraph, Graph
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Command
from langgraph.graph import StateGraph

from agent_workflow_server.agents.base import BaseAdapter, BaseAgent
from agent_workflow_server.services.message import Message
from agent_workflow_server.storage.models import Run


class LangGraphAdapter(BaseAdapter):
    def load_agent(self, agent: object) -> Optional[BaseAgent]:
        if isinstance(agent, Graph):
            return LangGraphAgent(agent.compile())
        elif isinstance(agent, CompiledGraph):
            return LangGraphAgent(agent)
        return None


class LangGraphAgent(BaseAgent):
    def __init__(self, agent: CompiledGraph):
        self.agent = agent

    async def astream(self, run: Run):
        input = run["input"]
        config = run["config"]
        if config is None:
            config = {}
        configurable = config.get("configurable")
        if configurable is None:
            configurable = {}
        configurable.setdefault("thread_id", run["thread_id"])

        # If it's a CompiledStateGraph, validate (and deserialize) input
        if isinstance(self.agent, CompiledStateGraph) and hasattr(
            self.agent.builder.schema, "model_validate"
        ):
            input = self.agent.builder.schema.model_validate(input)

        # If there's an interrupt answer, ovverride the input
        if "interrupt" in run and "user_data" in run["interrupt"]:
            input = Command(resume=run["interrupt"]["user_data"])

        # If we have a StateGraph, we can validate the schema
        if isinstance(self.agent.builder, StateGraph):
            input = self.agent.builder.schema.model_validate(input)

        async for event in self.agent.astream(
            input=input,
            config=RunnableConfig(
                configurable=configurable,
                tags=config["tags"],
                recursion_limit=config["recursion_limit"],
            ),
        ):
            for k, v in event.items():
                if k == INTERRUPT:
                    yield Message(
                        type="interrupt",
                        event=k,
                        data=v[0].value,
                    )
                else:
                    yield Message(
                        type="message",
                        event=k,
                        data=v,
                    )
