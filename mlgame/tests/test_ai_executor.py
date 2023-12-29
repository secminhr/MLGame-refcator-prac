from contextlib import contextmanager
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


@contextmanager
def assert_same(mock_calls):
    expected_calls = Mock()
    try:
        yield expected_calls
    finally:
        assert mock_calls == expected_calls.mock_calls


class TestAIExecutor:
    @pytest.mark.parametrize('game_alive_count', [5, 10])
    def test_ai_reset(self, game_alive_count):
        game_status_list = [({'status': 'GAME_ALIVE'}, {})] * game_alive_count + [None]
        ai_comm, send_to_game = self._create_mocked_ai_comm(game_status_list)
        ai_client = self._patch_ai_client('RESET')

        func_calls_test = Mock()
        func_calls_test.ai_client = ai_client
        func_calls_test.send_to_game = send_to_game.send

        executor = AIClientExecutor('tester', ai_comm, ai_loader=fixed_ai_loader(ai_client))
        executor.run()

        with assert_same(func_calls_test.mock_calls) as expect_calls:
            for i in range(game_alive_count):
                expect_calls.send_to_game('READY')
                expect_calls.ai_client.update({'status': 'GAME_ALIVE'}, {})
                expect_calls.ai_client.reset()
            expect_calls.send_to_game('READY')

    @pytest.mark.parametrize('game_alive_count', [5, 10])
    def test_ai_game_end(self, game_alive_count):
        game_status_list = [({'status': 'GAME_ALIVE'}, {})] * game_alive_count + [({'status': 'GAME_OVER'}, {}), None]
        ai_comm, send_to_game = self._create_mocked_ai_comm(game_status_list)
        ai_client = self._patch_ai_client('AI_COMMAND')

        func_calls_test = Mock()
        func_calls_test.ai_client = ai_client
        func_calls_test.send_to_game = send_to_game.send

        executor = AIClientExecutor('tester', ai_comm, ai_loader=fixed_ai_loader(ai_client))
        executor.run()

        with assert_same(func_calls_test.mock_calls) as expect_calls:
            expect_calls.send_to_game('READY')
            for i in range(game_alive_count):
                expect_calls.ai_client.update({'status': 'GAME_ALIVE'}, {})
                expect_calls.send_to_game({
                    'frame': i,
                    'command': 'AI_COMMAND'
                })
            expect_calls.ai_client.update({'status': 'GAME_OVER'}, {})
            expect_calls.ai_client.reset()
            expect_calls.send_to_game('READY')

    def _patch_ai_client(self, update_return_value) -> AIClient:
        ai_client = Mock(MLPlay)
        ai_client.update = Mock(return_value=update_return_value)

        return ai_client

    def _create_mocked_ai_comm(self, game_status_list):
        ai_comm = MLCommManager('tester')
        recv_end = RecvEnd()
        recv_end.recv = Mock(side_effect=game_status_list)
        send_end = SendEnd()
        send_end.send = Mock()
        ai_comm.set_comm_to_game(recv_end, send_end)
        return ai_comm, send_end

