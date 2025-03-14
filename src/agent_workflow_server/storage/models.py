from dataclasses import dataclass
import json
from typing import Any, Dict, Optional, TypedDict, Literal
from uuid import UUID
from datetime import datetime

RunStatus = Literal['pending', 'error', 'success', 'timeout', 'interrupted']

class Run(TypedDict):
    """Definition for a Run record"""
    run_id: str
    agent_id: str
    thread_id: str
    input: Dict[str, Any]
    config: Dict[str, Any]
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    status: RunStatus

class RunInfo(TypedDict):
    """Definition of statistics information about a Run"""
    run_id: str
    attempts: Optional[int]
    started_at: Optional[datetime]
    ended_at: Optional[datetime]
    exec_s: Optional[float]
    queue_s: Optional[float]
