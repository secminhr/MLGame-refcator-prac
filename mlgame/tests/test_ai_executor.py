from unittest.mock import Mock
from typing import Callable

import pytest

from mlgame.core.communication import MLCommManager

from mlgame.core.executor import AIClientExecutor, AIClient

class MLPlay:
    def __init__(self, *args, **kwargs):
        pass

    def update(self, scene_info, keyboard=None, *args, **kwargs):
        pass

    def reset(self):
        pass

class SendEnd:
    def send(self, msg):
        pass

class RecvEnd:
    def poll(self):
        pass

    def recv(self):
        pass


def fixed_ai_loader(ai: AIClient) -> Callable[[str, dict], AIClient]:
    return lambda ai_name, game_params: ai

class TestAIExecutor:
    @pytest.mark.parametrize(
        'game_status_list',
        [
            [({'status': 'GAME_ALIVE'}, {})] * 5 + [None],
            [({'status': 'GAME_ALIVE'}, {})] * 10 + [None]
        ]
    )
    def test_ai_reset(self, game_status_list):
        ai_comm = self._create_mocked_ai_comm(game_status_list)
        ai_client = self._patch_ai_client_reset()
        executor = AIClientExecutor('tester', ai_comm, ai_loader=fixed_ai_loader(ai_client))
        executor.run()

        assert ai_client.reset.call_count == len(game_status_list) - 1

    def _patch_ai_client_reset(self) -> AIClient:
        # patch ai client
        ai_client = MLPlay()
        ai_client.update = Mock(return_value="RESET")
        ai_client.reset = Mock()
        return ai_client

    @pytest.mark.parametrize(
        'game_status_list',
        [
            [({'status': 'GAME_ALIVE'}, {})] * 5 + [({'status': 'GAME_OVER'}, {}), None],
            [({'status': 'GAME_ALIVE'}, {})] * 10 + [({'status': 'GAME_OVER'}, {}), None]
        ]
    )
    def test_ai_game_end(self, game_status_list):
        ai_comm = self._create_mocked_ai_comm(game_status_list)
        ai_client = self._patch_ai_client()

        executor = AIClientExecutor('tester', ai_comm, ai_loader=fixed_ai_loader(ai_client))
        executor.run()

        ai_client.reset.assert_called_once()

    @pytest.mark.parametrize(
        'game_status_list',
        [
            [({'status': 'GAME_ALIVE'}, {})] * 5 + [({'status': 'GAME_OVER'}, {}), None],
            [({'status': 'GAME_ALIVE'}, {})] * 10 + [({'status': 'GAME_OVER'}, {}), None]
        ]
    )
    def test_ai_update(self, game_status_list):
        ai_comm = self._create_mocked_ai_comm(game_status_list)
        ai_client = self._patch_ai_client()

        executor = AIClientExecutor('tester', ai_comm, ai_loader=fixed_ai_loader(ai_client))
        executor.run()

        assert ai_client.update.call_count == len(game_status_list) - 1

    def _patch_ai_client(self) -> AIClient:
        # patch ai client
        ai_client = MLPlay()
        ai_client.update = Mock()
        ai_client.reset = Mock()
        return ai_client

    def _create_mocked_ai_comm(self, game_status_list):
        ai_comm = MLCommManager('tester')
        recv_end = RecvEnd()
        recv_end.recv = Mock(side_effect=game_status_list)
        ai_comm.set_comm_to_game(recv_end, SendEnd())
        return ai_comm