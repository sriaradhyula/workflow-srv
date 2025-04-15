# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

import inspect
from typing import Dict, Optional

from llama_index.core.workflow import (
    Context,
    HumanResponseEvent,
    InputRequiredEvent,
    Workflow,
)

from agent_workflow_server.agents.base import BaseAdapter, BaseAgent
from agent_workflow_server.services.message import Message
from agent_workflow_server.storage.models import Run


class LlamaIndexAdapter(BaseAdapter):
    def load_agent(self, agent: object) -> Optional[BaseAgent]:
        if callable(agent) and len(inspect.signature(agent).parameters) == 0:
            result = agent()
            if isinstance(result, Workflow):
                return LlamaIndexAgent(result)
        if isinstance(agent, Workflow):
            return LlamaIndexAgent(agent)
        return None


class LlamaIndexAgent(BaseAgent):
    def __init__(self, agent: Workflow):
        self.agent = agent
        self.contexts: Dict[str, Context] = {}

    async def astream(self, run: Run):
        input = run["input"]

        print("thread_id", run["thread_id"])

        ctx = self.contexts.get(run["thread_id"])

        # if ctx is not None:
        #     print("ctx", json.dumps(ctx.to_dict(serializer=JsonPickleSerializer())))

        handler = self.agent.run(ctx=ctx, input={**input})
        if handler.ctx is None:
            # This should never happen, workflow.run actually sets the Context
            raise ValueError("Context cannot be None.")

        if "interrupt" in run and "user_data" in run["interrupt"]:
            user_data = run["interrupt"]["user_data"]

            # FIXME: workaround to extract the user response from a dict/obj. Needed for input validation, remove once not needed anymore.
            if isinstance(user_data, dict):
                user_data = list(user_data.values())[0]
            handler.ctx.send_event(HumanResponseEvent(response=user_data))

        async for event in handler.stream_events():
            print("event", event)
            # print(
            #     "handler.ctx",
            #     json.dumps(handler.ctx.to_dict(serializer=JsonPickleSerializer())),
            # )
            if isinstance(event, InputRequiredEvent):
                # Send the interrupt

                self.contexts[run["thread_id"]] = handler.ctx
                # print("await cancel_run")
                # await handler.cancel_run()
                # print("after await cancel_run")

                # PROBLEM: with cancel_run(): I get a StopEvent() in the next iteration, and context does not match (I get a warning)
                # BUT: without cancel_run() I get a timeout after run succeds

                # FIXME: workaround to wrap the prefix (str) in a dict/obj. Needed for output validation, remove once not needed anymore.
                yield Message(type="interrupt", data={"interrupt": event.prefix})
            else:
                self.contexts[run["thread_id"]] = handler.ctx
                yield Message(
                    type="message",
                    data=event,
                )
        print("await handler")
        final_result = await handler
        print("after await handler")
        self.contexts[run["thread_id"]] = handler.ctx
        yield Message(
            type="message",
            data=final_result,
        )
