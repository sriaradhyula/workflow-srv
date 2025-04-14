# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

import hashlib
import inspect
import json
from typing import Any, Dict, Optional

from llama_index.core.workflow import (
    Context,
    HumanResponseEvent,
    InputRequiredEvent,
    Workflow,
)
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
    """Holds the state of the workflow."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    hash: Optional[str] = Field(
        default=None, description="Hash of the context, if any."
    )
    state: dict = Field(default_factory=dict, description="Pickled state, if any.")
    run_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Run kwargs needed to run the workflow."
    )
    session_id: Optional[str] = Field(
        default=None, description="Session ID for the current Run"
    )


class LlamaIndexAgent(BaseAgent):
    def __init__(self, agent: Workflow):
        self.agent = agent
        self.sessions_state: Dict[str, str] = {}

    def _get_ctx(self, session_id: str) -> Optional[Context]:
        """Load the existing context from the workflow state, if any."""

        workflow_state_json: Optional[str] = self.sessions_state.get(session_id, None)

        if workflow_state_json is None:
            return None

        workflow_state = WorkflowState.model_validate_json(workflow_state_json)
        if workflow_state.state is None:
            return None

        context_dict = workflow_state.state
        context_str = json.dumps(context_dict)
        context_hash = _make_hash(context_str)

        if workflow_state.hash is not None and context_hash != workflow_state.hash:
            raise ValueError("Context hash does not match.")

        return Context.from_dict(
            self.agent,
            workflow_state.state,
            serializer=JsonPickleSerializer(),
        )

    def _set_ctx(
        self, ctx: Context, session_id: str, run_kwargs: Dict[str, Any]
    ) -> None:
        if session_id is None:
            raise ValueError("Session ID is None. Cannot set workflow state.")

        """Set the workflow state for this session."""
        context_dict = ctx.to_dict(serializer=JsonPickleSerializer())
        context_str = json.dumps(context_dict)
        context_hash = _make_hash(context_str)

        workflow_state = WorkflowState(
            hash=context_hash,
            state=context_dict,
            run_kwargs=run_kwargs,
            session_id=session_id,
        )

        session_state = workflow_state.model_dump_json()
        self.sessions_state[session_id] = session_state

    async def astream(self, run: Run):
        input = run["input"]

        ctx = self._get_ctx(run["thread_id"])

        handler = self.agent.run(ctx=ctx, input={**input})
        if handler.ctx is None:
            # This should never happen, workflow.run actually sets the Context
            raise ValueError("Context cannot be None.")

        async for event in handler.stream_events():
            if isinstance(event, InputRequiredEvent):
                # If I have a user_data, I send it to the workflow
                if "interrupt" in run and "user_data" in run["interrupt"]:
                    user_data = run["interrupt"]["user_data"]

                    # FIXME: workaround to extract the user response from a dict/obj. Needed for input validation, remove once not needed anymore.
                    if isinstance(user_data, dict):
                        user_data = list(user_data.values())[0]
                    handler.ctx.send_event(HumanResponseEvent(response=user_data))
                    # TODO: maybe need to delete user_data from the run
                else:
                    # otherwise, I send the interrupt
                    # FIXME: workaround to wrap the prefix (str) in a dict/obj. Needed for output validation, remove once not needed anymore.
                    yield Message(type="interrupt", data={"interrupt": event.prefix})
            else:
                yield Message(
                    type="message",
                    data=event,
                )
        final_result = await handler
        yield Message(
            type="message",
            data=final_result,
        )
        self._set_ctx(
            ctx=handler.ctx,
            session_id=run["thread_id"],
            run_kwargs={**input},
        )
