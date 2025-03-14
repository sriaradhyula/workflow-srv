# Agent Workflow Server

- [Documentation](https://agntcy.github.io/workflow-srv)

## About The Project

The Agent Workflow Server (AgWS) enables participation in the IoA. It accommodates agents from diverse frameworks and exposes them through ACP, regardless of their underlying implementation.

> [!NOTE]
> If you wish to use the Agent Workflow Server to run your Agent, please check out the user-facing [Agent Workflow Server Manager](https://github.com/cisco-eti/agent-workflow-cli) instead.

## Getting Started

1) Copy example env file and adapt if necessary: `cp .env.example .env`

1) Create a virtual environment and install the server dependencies: `poetry install`

    > **NOTE**: make sure to have poetry version 2+

1) Install an agent
    > e.g.: `pip install examples/agents/mailcomposer`

1) Start the server: `poetry run server`

### Generating API

1) If it's the first time you're cloning this repo, initialize submodule: `git submodule update --init --recursive`

1) Run `make generate-api`

Generated code (API routes template and modes) is under `src/agent_workflow_server/generated`. 

- If needed, API routes template could be manually copied and implemented under `src/agent_workflow_server/apis`
- Models should not be copied over different places nor modified, but referenced as they are

### Authentication

API Key authentication is optional:
- Set `API_KEY` environment variable to enable authentication
- Include the key in requests via `x-api-key` header

### OpenAPI Documentation

Once the Agent Workflow Server is running, interactive API docs are available under `/docs` endpoint, redoc documentation under `/redoc` endpoint

## Contributing

Contributions are what make the open source community such an amazing place to
learn, inspire, and create. Any contributions you make are **greatly
appreciated**. For detailed contributing guidelines, please see
[CONTRIBUTING.md](CONTRIBUTING.md)

## Copyright Notice

[Copyright Notice and License](LICENSE)

Copyright (c) 2025 Cisco and/or its affiliates.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

```plaintext
https://www.apache.org/licenses/LICENSE-2.0
```

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
