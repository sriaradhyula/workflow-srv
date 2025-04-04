# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

import hashlib
import inspect
import json
from typing import Any, Dict, Optional

from llama_index.core.workflow import Context, Workflow
from llama_index.core.workflow.context_serializers import (
    JsonPickleSerializer,
)
from pydantic import BaseModel, ConfigDict, Field

from agent_workflow_server.agents.base import BaseAdapter, BaseAgent
from agent_workflow_server.services.message import Message
from agent_workflow_server.storage.models import Run


def _make_hash(context_str: str) -> str:
    h = hashlib.sha256()
    h.update(context_str.encode())
    return h.hexdigest()


class LlamaIndexAdapter(BaseAdapter):
    def load_agent(self, agent: object) -> Optional[BaseAgent]:
        if callable(agent) and len(inspect.signature(agent).parameters) == 0:
            result = agent()
            if isinstance(result, Workflow):
                return LlamaIndexAgent(result)
        if isinstance(agent, Workflow):
            return LlamaIndexAgent(agent)
        return None


class WorkflowState(BaseModel):
    """Holds the state of the workflow.

    Used to validate and pass message payloads.

    TODO: Should this be the general payload for all messages?
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    hash: Optional[str] = Field(
        default=None, description="Hash of the context, if any."
    )
    state: dict = Field(default_factory=dict, description="Pickled state, if any.")
    run_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Run kwargs needed to run the workflow."
    )
    session_id: Optional[str] = Field(
        default=None, description="Session ID for the current task."
    )
    task_id: str = Field(description="Task ID for the current run.")


class LlamaIndexAgent(BaseAgent):
    def __init__(self, agent: Workflow):
        self.agent = agent

    async def get_workflow_state(self, state: WorkflowState) -> Optional[Context]:
        """Load the existing context from the workflow state."""
        if state.session_id is None:
            return None

        state_dict = await self.get_session_state(state.session_id)
        if state_dict is None:
            return None

        workflow_state_json = state_dict.get(state.session_id, None)

        if workflow_state_json is None:
            return None

        workflow_state = WorkflowState.model_validate_json(workflow_state_json)
        if workflow_state.state is None:
            return None

        context_dict = workflow_state.state
        context_str = json.dumps(context_dict)
        context_hash = _make_hash(context_str)

        if workflow_state.hash is not None and context_hash != workflow_state.hash:
            raise ValueError("Context hash does not match!")

        return Context.from_dict(
            self.agent,
            workflow_state.state,
            serializer=JsonPickleSerializer(),
        )

    async def set_workflow_state(
        self, ctx: Context, current_state: WorkflowState
    ) -> None:
        """Set the workflow state for this session."""
        context_dict = ctx.to_dict(serializer=JsonPickleSerializer())
        context_str = json.dumps(context_dict)
        context_hash = _make_hash(context_str)

        workflow_state = WorkflowState(
            hash=context_hash,
            state=context_dict,
            run_kwargs=current_state.run_kwargs,
            session_id=current_state.session_id,
            task_id=current_state.task_id,
        )

        if current_state.session_id is None:
            raise ValueError("Session ID is None! Cannot set workflow state.")

        session_state = await self.get_session_state(current_state.session_id)
        if session_state:
            session_state[current_state.session_id] = workflow_state.model_dump_json()

            # Store the state in the control plane
            await self.update_session_state(current_state.session_id, session_state)

    async def astream(self, run: Run):
        input = run["input"]

        ctx = await self.get_workflow_state(run)

        handler = self.agent.run(ctx=ctx, input={**input})
        async for event in handler.stream_events():
            yield Message(
                type="message",
                data=event,
            )
        final_result = await handler
        yield Message(
            type="message",
            data=final_result,
        )
