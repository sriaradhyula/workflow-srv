# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: Apache-2.0
import argparse
import asyncio
import json
import logging
import os
import pathlib
import signal
import sys

import uvicorn
import uvicorn.logging
from dotenv import load_dotenv
from fastapi import Depends, FastAPI

import agent_workflow_server.logging.logger  # noqa: F401
from agent_workflow_server.agents.load import load_agents
from agent_workflow_server.apis.agents import public_router as PublicAgentsApiRouter
from agent_workflow_server.apis.agents import router as AgentsApiRouter
from agent_workflow_server.apis.authentication import (
    authentication_with_api_key,
    setup_api_key_auth,
)
from agent_workflow_server.apis.stateless_runs import router as StatelessRunsApiRouter
from agent_workflow_server.services.queue import start_workers

load_dotenv()

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000

logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    app = FastAPI(
        title="Agent Workflow Server",
        version="0.1",
    )

    setup_api_key_auth(app)

    app.include_router(
        router=AgentsApiRouter,
        dependencies=[Depends(authentication_with_api_key)],
    )
    app.include_router(
        router=PublicAgentsApiRouter,
    )
    app.include_router(
        router=StatelessRunsApiRouter,
        dependencies=[Depends(authentication_with_api_key)],
    )
    return app

def signal_handler(sig, frame):
    logger.warning(f"Received {signal.Signals(sig).name}. Exiting...")
    sys.exit(0)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Agent Workflow Server")
    parser.add_argument('--host', default=os.getenv("API_HOST", DEFAULT_HOST))
    parser.add_argument('--port', type=int, default=int(os.getenv("API_PORT", DEFAULT_PORT)))
    parser.add_argument('--num-workers', type=int, default=int(os.environ.get("NUM_WORKERS", 5)))
    parser.add_argument('--agent-manifest-path', action='append', type=pathlib.Path, default=[os.getenv('AGENT_MANIFEST_PATH', "manifest.json")])
    parser.add_argument('--agents-ref', default=os.getenv('AGENTS_REF', None))
    parser.add_argument('--reload', action='store_true')
    #parser.add_argument('--log-level', default=logging.DEBUG)
    return parser.parse_args()

def start():
    try:
        args = parse_args()

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        load_agents(args.agents_ref, args.agent_manifest_path)
        n_workers = args.num_workers

        loop = asyncio.get_event_loop()
        loop.create_task(start_workers(n_workers))

        config = uvicorn.Config(
            create_app(),
            host=args.host,
            port=args.port,
            loop="asyncio",
            reload=args.reload,
        )
        server = uvicorn.Server(config)
        loop.run_until_complete(server.serve())
    except SystemExit as e:
        logger.warning(f"Agent Workflow Server exited with code: {e}")
    except Exception as e:
        logger.error(f"Exiting due to an unexpected error: {e}")


if __name__ == "__main__":
    start()
