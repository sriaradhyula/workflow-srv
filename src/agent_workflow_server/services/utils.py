# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0

from agent_workflow_server.storage.models import Run


def check_run_is_interrupted(run: Run):
    if run is None:
        raise ValueError("Run not found")
    if run["status"] != "interrupted":
        raise ValueError("Run is not in interrupted state")
    if run.get("interrupt") is None:
        raise ValueError(f"No interrupt found for run {run['run_id']}")
