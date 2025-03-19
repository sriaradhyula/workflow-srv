from pytest_mock import MockerFixture

from agent_workflow_server.agents.load import AGENTS, load_agents
from tests.mock import MOCK_AGENTS_REF_ENV, MOCK_MANIFEST_ENV, MockAdapter, MockAgent


def test_load_agents(mocker: MockerFixture):
    mocker.patch.dict("os.environ", MOCK_AGENTS_REF_ENV)
    mocker.patch.dict("os.environ", MOCK_MANIFEST_ENV)
    mocker.patch("agent_workflow_server.agents.load.ADAPTERS", [MockAdapter()])

    load_agents()

    assert len(AGENTS) == 1
    assert isinstance(AGENTS["mock_agent"].agent, MockAgent)
