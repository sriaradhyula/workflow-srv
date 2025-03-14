# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictInt, StrictStr
from typing import Any, Dict, List, Optional
from typing_extensions import Annotated
from agent_workflow_server.generated.models.run import Run
from agent_workflow_server.generated.models.run_create import RunCreate
from agent_workflow_server.generated.models.run_output import RunOutput
from agent_workflow_server.generated.models.run_output_stream import RunOutputStream
from agent_workflow_server.generated.models.run_search_request import RunSearchRequest


class BaseRunsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseRunsApi.subclasses = BaseRunsApi.subclasses + (cls,)
    async def create_run(
        self,
        run_create: RunCreate,
    ) -> Run:
        """Create a run, return the run descriptor immediately. Don&#39;t wait for the final run output."""
        ...


    async def delete_run(
        self,
        run_id: Annotated[StrictStr, Field(description="The ID of the agent.")],
    ) -> Run:
        """Cancel a run."""
        ...


    async def get_run(
        self,
        run_id: Annotated[StrictStr, Field(description="The ID of the agent.")],
    ) -> Run:
        """Get a run from its ID. Don&#39;t wait for the final run output."""
        ...


    async def get_run_output(
        self,
        run_id: Annotated[StrictStr, Field(description="The ID of the run.")],
        block_timeout: Optional[StrictInt],
    ) -> RunOutput:
        """Retrieve the last output of the run.  The output can be:   * an interrupt, this happens when the agent run status is &#x60;interrupted&#x60;   * the final result of the run, this happens when the agent run status is &#x60;success&#x60;   * an error, this happens when the agent run status is &#x60;error&#x60; or &#x60;timeout&#x60;   If the block timeout is provided and the current run status is &#x60;pending&#x60;, this call blocks until the state changes or the timeout expires.  If no timeout is provided or the timeout has expired and  run status is &#x60;pending&#x60;, this call returns &#x60;204&#x60; with no content."""
        ...


    async def get_run_stream(
        self,
        run_id: Annotated[StrictStr, Field(description="The ID of the run.")],
    ) -> RunOutputStream:
        """Send a stream of events using Server-sent events (SEE). See &lt;https://html.spec.whatwg.org/multipage/server-sent-events.html&gt; for details."""
        ...


    async def resume_run(
        self,
        run_id: Annotated[StrictStr, Field(description="The ID of the agent.")],
        body: Dict[str, Any],
    ) -> Run:
        """Provide the needed input to a run to resume its execution. Can only be called for runs that are in the interrupted state Schema of the provided input must match with the schema specified in the agent specs under interrupts for the interrupt type the agent generated for this specific interruption."""
        ...


    async def search_runs(
        self,
        run_search_request: RunSearchRequest,
    ) -> List[Run]:
        """Search for runs.  This endpoint also functions as the endpoint to list all runs."""
        ...
