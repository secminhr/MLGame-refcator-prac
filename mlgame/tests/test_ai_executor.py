from unittest.mock import Mock

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


class TestAIExecutor:
    @pytest.mark.parametrize(
        'game_status_list',
        [
            [({'status': 'GAME_ALIVE'}, {})] * 5 + [None],
            [({'status': 'GAME_ALIVE'}, {})] * 10 + [None]
        ]
    )
    def test_ai_reset(self, game_status_list):
        # setup communication
        ai_comm = MLCommManager('tester')
        recv_end = RecvEnd()
        recv_end.recv = Mock(side_effect=game_status_list)
        ai_comm.set_comm_to_game(recv_end, SendEnd())

        executor = AIClientExecutor('tester', ai_comm, ai_loader=self._patch_ai_client_reset)
        executor.run()

        assert self.ai_client.reset.call_count == len(game_status_list) - 1

    def _patch_ai_client_reset(self, ai_name: str, game_params: dict) -> AIClient:
        # patch ai client
        self.ai_client = MLPlay()
        self.ai_client.update = Mock(return_value="RESET")
        self.ai_client.reset = Mock()
        return self.ai_client

