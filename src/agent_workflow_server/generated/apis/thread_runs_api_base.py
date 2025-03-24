# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictBool, StrictInt, StrictStr, field_validator
from typing import Any, Dict, List, Optional
from typing_extensions import Annotated
from agent_workflow_server.generated.models.run import Run
from agent_workflow_server.generated.models.run_create_stateful import RunCreateStateful
from agent_workflow_server.generated.models.run_output_stream import RunOutputStream
from agent_workflow_server.generated.models.run_wait_response import RunWaitResponse


class BaseThreadRunsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseThreadRunsApi.subclasses = BaseThreadRunsApi.subclasses + (cls,)
    async def cancel_thread_run(
        self,
        thread_id: Annotated[StrictStr, Field(description="The ID of the thread.")],
        run_id: Annotated[StrictStr, Field(description="The ID of the run.")],
        wait: Optional[StrictBool],
        action: Annotated[Optional[StrictStr], Field(description="Action to take when cancelling the run. Possible values are `interrupt` or `rollback`. `interrupt` will simply cancel the run. `rollback` will cancel the run and delete the run and associated checkpoints afterwards.")],
    ) -> None:
        ...


    async def create_and_stream_thread_run_output(
        self,
        thread_id: Annotated[StrictStr, Field(description="The ID of the thread.")],
        run_create_stateful: RunCreateStateful,
    ) -> RunOutputStream:
        """Create a run on a thread and join its output stream. See &#39;GET /runs/{run_id}/stream&#39; for details on the return values."""
        ...


    async def create_and_wait_for_thread_run_output(
        self,
        thread_id: Annotated[StrictStr, Field(description="The ID of the thread.")],
        run_create_stateful: RunCreateStateful,
    ) -> RunWaitResponse:
        """Create a run on a thread and block waiting for its output. See &#39;GET /runs/{run_id}/wait&#39; for details on the return values."""
        ...


    async def create_thread_run(
        self,
        thread_id: Annotated[StrictStr, Field(description="The ID of the thread.")],
        run_create_stateful: RunCreateStateful,
    ) -> Run:
        """Create a run on a thread, return the run ID immediately. Don&#39;t wait for the final run output."""
        ...


    async def delete_thread_run(
        self,
        thread_id: Annotated[StrictStr, Field(description="The ID of the thread.")],
        run_id: Annotated[StrictStr, Field(description="The ID of the run.")],
    ) -> None:
        """Delete a run by ID."""
        ...


    async def get_thread_run(
        self,
        thread_id: Annotated[StrictStr, Field(description="The ID of the thread.")],
        run_id: Annotated[StrictStr, Field(description="The ID of the run.")],
    ) -> Run:
        """Get a run by ID."""
        ...


    async def list_thread_runs(
        self,
        thread_id: Annotated[StrictStr, Field(description="The ID of the thread.")],
        limit: Optional[StrictInt],
        offset: Optional[StrictInt],
    ) -> List[Run]:
        """List runs for a thread."""
        ...


    async def resume_thread_run(
        self,
        thread_id: Annotated[StrictStr, Field(description="The ID of the thread.")],
        run_id: Annotated[StrictStr, Field(description="The ID of the run.")],
        body: Dict[str, Any],
    ) -> Run:
        """Provide the needed input to a run to resume its execution. Can only be called for runs that are in the interrupted state Schema of the provided input must match with the schema specified in the agent specs under interrupts for the interrupt type the agent generated for this specific interruption."""
        ...


    async def stream_thread_run_output(
        self,
        thread_id: Annotated[StrictStr, Field(description="The ID of the thread.")],
        run_id: Annotated[StrictStr, Field(description="The ID of the run.")],
    ) -> RunOutputStream:
        """Join the output stream of an existing run. See &#39;GET /runs/{run_id}/stream&#39; for details on the return values."""
        ...


    async def wait_for_thread_run_output(
        self,
        thread_id: Annotated[StrictStr, Field(description="The ID of the thread.")],
        run_id: Annotated[StrictStr, Field(description="The ID of the run.")],
    ) -> RunWaitResponse:
        """Blocks waiting for the result of the run. See &#39;GET /runs/{run_id}/wait&#39; for details on the return values."""
        ...
