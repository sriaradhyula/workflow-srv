from pytest_mock import MockerFixture

from agent_workflow_server.agents.load import load_agents, AGENTS
from tests.mock import MockAgent, MockAdapter, MOCK_AGENTS_REF

def test_load_agents(mocker: MockerFixture):
    mocker.patch.dict('os.environ', MOCK_AGENTS_REF)
    mocker.patch('agent_workflow_server.agents.load.ADAPTERS', [MockAdapter()])

    load_agents()

    assert len(AGENTS) == 1
    assert isinstance(AGENTS['mock_agent'].agent, MockAgent)