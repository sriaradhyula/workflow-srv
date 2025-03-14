# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictStr
from typing import Any, Dict, List
from typing_extensions import Annotated
from agent_workflow_server.generated.models.run import Run
from agent_workflow_server.generated.models.thread import Thread
from agent_workflow_server.generated.models.thread_create import ThreadCreate
from agent_workflow_server.generated.models.thread_search_request import ThreadSearchRequest


class BaseThreadsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseThreadsApi.subclasses = BaseThreadsApi.subclasses + (cls,)
    async def create_thread(
        self,
        thread_create: ThreadCreate,
    ) -> Thread:
        """Create an empty thread. This is useful to associate metadata to a thread."""
        ...


    async def delete_thread(
        self,
        thread_id: Annotated[StrictStr, Field(description="The ID of the thread.")],
    ) -> Thread:
        """Delete a thread."""
        ...


    async def get_run_threadstate(
        self,
        run_id: Annotated[StrictStr, Field(description="The ID of the run.")],
    ) -> object:
        """This call can be used only for agents that support thread, i.e. for Runs that specify a thread ID. It can be called only on runs that are in &#x60;success&#x60; status. It returns the thread state at the end of the Run. Can be used to reconstruct the evolution of the thread state in its history."""
        ...


    async def get_thread(
        self,
        thread_id: Annotated[StrictStr, Field(description="The ID of the thread.")],
    ) -> Thread:
        """Get a thread from its ID. """
        ...


    async def get_thread_history(
        self,
        thread_id: Annotated[StrictStr, Field(description="The ID of the thread.")],
    ) -> List[Run]:
        """Retrieve ordered list of runs for this thread in chronological order."""
        ...


    async def get_thread_state(
        self,
        thread_id: Annotated[StrictStr, Field(description="The ID of the thread.")],
    ) -> object:
        """Retrieve the the current state associated with the thread"""
        ...


    async def search_threads(
        self,
        thread_search_request: ThreadSearchRequest,
    ) -> List[Thread]:
        """Search for threads.  This endpoint also functions as the endpoint to list all threads."""
        ...
