# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from agent_workflow_server.generated.apis.runs_api_base import BaseRunsApi
import openapi_server.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from agent_workflow_server.generated.models.extra_models import TokenModel  # noqa: F401
from pydantic import Field, StrictInt, StrictStr
from typing import Any, Dict, List, Optional
from typing_extensions import Annotated
from agent_workflow_server.generated.models.run import Run
from agent_workflow_server.generated.models.run_create import RunCreate
from agent_workflow_server.generated.models.run_output import RunOutput
from agent_workflow_server.generated.models.run_output_stream import RunOutputStream
from agent_workflow_server.generated.models.run_search_request import RunSearchRequest


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/runs",
    responses={
        200: {"model": Run, "description": "Success"},
        404: {"model": str, "description": "Not Found"},
        409: {"model": str, "description": "Conflict"},
        422: {"model": str, "description": "Validation Error"},
    },
    tags=["Runs"],
    summary="Create Background Run",
    response_model_by_alias=True,
)
async def create_run(
    run_create: RunCreate = Body(None, description=""),
) -> Run:
    """Create a run, return the run descriptor immediately. Don&#39;t wait for the final run output."""
    if not BaseRunsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseRunsApi.subclasses[0]().create_run(run_create)


@router.delete(
    "/runs/{run_id}",
    responses={
        200: {"model": Run, "description": "Success"},
        404: {"model": str, "description": "Not Found"},
        409: {"model": str, "description": "Conflict"},
        422: {"model": str, "description": "Validation Error"},
    },
    tags=["Runs"],
    summary="Delete a run. If running, cancel and then delete.",
    response_model_by_alias=True,
)
async def delete_run(
    run_id: Annotated[StrictStr, Field(description="The ID of the agent.")] = Path(..., description="The ID of the agent."),
) -> Run:
    """Cancel a run."""
    if not BaseRunsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseRunsApi.subclasses[0]().delete_run(run_id)


@router.get(
    "/runs/{run_id}",
    responses={
        200: {"model": Run, "description": "Success"},
        404: {"model": str, "description": "Not Found"},
        409: {"model": str, "description": "Conflict"},
        422: {"model": str, "description": "Validation Error"},
    },
    tags=["Runs"],
    summary="Get a previously created Run",
    response_model_by_alias=True,
)
async def get_run(
    run_id: Annotated[StrictStr, Field(description="The ID of the agent.")] = Path(..., description="The ID of the agent."),
) -> Run:
    """Get a run from its ID. Don&#39;t wait for the final run output."""
    if not BaseRunsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseRunsApi.subclasses[0]().get_run(run_id)


@router.get(
    "/runs/{run_id}/output",
    responses={
        200: {"model": RunOutput, "description": "Success"},
        204: {"description": "No Output Available"},
        404: {"model": str, "description": "Not Found"},
        409: {"model": str, "description": "Conflict"},
        422: {"model": str, "description": "Validation Error"},
    },
    tags=["Runs"],
    summary="Retrieve last output of a run if available",
    response_model_by_alias=True,
)
async def get_run_output(
    run_id: Annotated[StrictStr, Field(description="The ID of the run.")] = Path(..., description="The ID of the run."),
    block_timeout: Optional[StrictInt] = Query(None, description="", alias="block_timeout"),
) -> RunOutput:
    """Retrieve the last output of the run.  The output can be:   * an interrupt, this happens when the agent run status is &#x60;interrupted&#x60;   * the final result of the run, this happens when the agent run status is &#x60;success&#x60;   * an error, this happens when the agent run status is &#x60;error&#x60; or &#x60;timeout&#x60;   If the block timeout is provided and the current run status is &#x60;pending&#x60;, this call blocks until the state changes or the timeout expires.  If no timeout is provided or the timeout has expired and  run status is &#x60;pending&#x60;, this call returns &#x60;204&#x60; with no content."""
    if not BaseRunsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseRunsApi.subclasses[0]().get_run_output(run_id, block_timeout)


@router.get(
    "/runs/{run_id}/stream",
    responses={
        200: {"model": RunOutputStream, "description": "Stream of agent results either as &#x60;RunResult&#x60; objects or custom objects, according to the specific streaming mode requested. Note that the stream of events is carried using the format specified in SSE spec &#x60;text/event-stream&#x60;"},
        204: {"description": "No Output Available"},
        404: {"model": str, "description": "Not Found"},
        409: {"model": str, "description": "Conflict"},
        422: {"model": str, "description": "Validation Error"},
    },
    tags=["Runs"],
    summary="Stream the run output",
    response_model_by_alias=True,
)
async def get_run_stream(
    run_id: Annotated[StrictStr, Field(description="The ID of the run.")] = Path(..., description="The ID of the run."),
) -> RunOutputStream:
    """Send a stream of events using Server-sent events (SEE). See &lt;https://html.spec.whatwg.org/multipage/server-sent-events.html&gt; for details."""
    if not BaseRunsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseRunsApi.subclasses[0]().get_run_stream(run_id)


@router.post(
    "/runs/{run_id}",
    responses={
        200: {"model": Run, "description": "Success"},
        404: {"model": str, "description": "Not Found"},
        409: {"model": str, "description": "Conflict"},
        422: {"model": str, "description": "Validation Error"},
    },
    tags=["Runs"],
    summary="Resume an interrupted Run",
    response_model_by_alias=True,
)
async def resume_run(
    run_id: Annotated[StrictStr, Field(description="The ID of the agent.")] = Path(..., description="The ID of the agent."),
    body: Dict[str, Any] = Body(None, description=""),
) -> Run:
    """Provide the needed input to a run to resume its execution. Can only be called for runs that are in the interrupted state Schema of the provided input must match with the schema specified in the agent specs under interrupts for the interrupt type the agent generated for this specific interruption."""
    if not BaseRunsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseRunsApi.subclasses[0]().resume_run(run_id, body)


@router.post(
    "/runs/search",
    responses={
        200: {"model": List[Run], "description": "Success"},
        422: {"model": str, "description": "Validation Error"},
    },
    tags=["Runs"],
    summary="Search Runs",
    response_model_by_alias=True,
)
async def search_runs(
    run_search_request: RunSearchRequest = Body(None, description=""),
) -> List[Run]:
    """Search for runs.  This endpoint also functions as the endpoint to list all runs."""
    if not BaseRunsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseRunsApi.subclasses[0]().search_runs(run_search_request)
