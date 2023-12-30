import os
from unittest.mock import Mock

from mlgame.tests.test_executor.comm_mock_prototype import SendEnd, RecvEnd
from mlgame.tests.test_executor.test_helper import assert_same
from mlgame.view.view import PygameViewInterface

from mlgame.core.communication import GameCommManager

from mlgame.game.paia_game import PaiaGame

from mlgame.core.executor import GameExecutor


class TestPaiaGame(PaiaGame):

    def __init__(self):
        super().__init__(1)

    def update(self, commands: dict):
        pass

    def get_data_from_game_to_player(self) -> dict:
        return {'1P': 'game data'}

    def reset(self):
        super().reset()

    def get_scene_init_data(self) -> dict:
        return {'scene': 'aaannn'}

    def get_scene_progress_data(self) -> dict:
        return {"draw_data": "DRAW_DATA"}

    def get_game_result(self) -> dict:
        return {'attachment': [1, 2]}


class TestPygameView(PygameViewInterface):

    def __init__(self):
        super().__init__({})

    def reset(self):
        pass

    def draw(self, object_information):
        pass

    def get_keyboard_info(self) -> list:
        return {'info': 'kb'}

    def save_image(self, img_path: os.path.abspath):
        pass


def _mock_game(update_return) -> (PaiaGame, Mock):
    game = TestPaiaGame()
    game.update = Mock(side_effect=update_return)
    game.reset = Mock(wraps=game.reset)

    game_mock = Mock()
    game_mock.update = game.update
    game_mock.reset = game.reset

    return game, game_mock

def _mock_ml_comm(recv_from_ml) -> (RecvEnd, SendEnd):
    recv_end = RecvEnd()
    recv_end.recv = Mock(side_effect=recv_from_ml)
    send_end = Mock(SendEnd)
    return recv_end, send_end

def _mock_comm_manager(recv_from_ml) -> (GameCommManager, SendEnd, SendEnd):
    game_comm_manager = GameCommManager()
    ml_recv, ml_send = _mock_ml_comm(recv_from_ml)
    game_comm_manager.add_comm_to_ml("1P", ml_recv, ml_send)

    other_recv = RecvEnd()
    other_send = Mock(SendEnd)
    game_comm_manager.add_comm_to_others('other', other_recv, other_send)

    return game_comm_manager, ml_send, other_send

def _mock_view() -> (PygameViewInterface, Mock):
    view = TestPygameView()
    view.is_paused = Mock(return_value=False)
    view.draw = Mock()

    view_interface_mock = Mock()
    view_interface_mock.is_paused = view.is_paused
    view_interface_mock.draw = view.draw

    return view, view_interface_mock

def _gather_mocks(game_mock, view_mock, send_to_ml, send_to_other) -> Mock:
    mock = Mock()
    mock.game_mock = game_mock
    mock.view_mock = view_mock
    mock.send_to_ml = send_to_ml
    mock.send_to_other = send_to_other
    return mock

class TestGameExecutor:
    def test_single_ai_client_no_display(self):
        game, game_mock = _mock_game(['UPDATE'] * 5 + ['QUIT'])
        game_comm_manager, send_to_ml, send_to_other = _mock_comm_manager(
            ['READY'] + [{'command': 'AI_COMMAND', 'frame': i} for i in range(6)]
        )
        view, view_mock = _mock_view()
        func_calls_test = _gather_mocks(game_mock, view_mock, send_to_ml, send_to_other)

        executor = GameExecutor(
            game,
            game_comm_manager,
            view,
            no_display=True
        )

        executor.run()

        with assert_same(func_calls_test.mock_calls) as expect_calls:
            expect_calls.send_to_other.send({'type': 'system_message', 'data': {'message': 'AI準備中'}})
            expect_calls.send_to_other.send({'type': 'game_info', 'data': {'scene': 'aaannn'}})
            expect_calls.send_to_other.send({'type': 'system_message', 'data': {'message': '遊戲啟動'}})
            for i in range(1, 7):
                expect_calls.view_mock.is_paused()
                expect_calls.send_to_ml.send(('game data', {'info': 'kb'}))
                expect_calls.game_mock.update({'1P': 'AI_COMMAND'})
                expect_calls.view_mock.draw({'draw_data': 'DRAW_DATA', 'frame': i})
                expect_calls.send_to_other.send({'type': 'game_progress', 'data': {'draw_data': 'DRAW_DATA', 'frame': i}})

            # last game update return QUIT
            expect_calls.send_to_ml.send(('game data', []))
            expect_calls.send_to_other.send({'type': 'system_message', 'data': {'message': '遊戲結束'}})
            expect_calls.send_to_other.send({'type': 'game_result', 'data': {'attachment': [1, 2]}})
            expect_calls.send_to_other.send({'type': 'system_message', 'data': {'message': '關閉遊戲'}})
            expect_calls.send_to_other.send(None)

    def test_single_ai_client_no_display_2_games(self):
        game, game_mock = _mock_game(['UPDATE'] * 5 + ['RESET'] + ['UPDATE'] * 5 + ['QUIT'])
        game_comm_manager, send_to_ml, send_to_other = _mock_comm_manager(
            ['READY'] + [{'command': 'AI_COMMAND', 'frame': i} for i in range(6)] +
            ['READY'] + [{'command': 'AI_COMMAND', 'frame': i} for i in range(6)]
        )
        view, view_mock = _mock_view()
        func_calls_test = _gather_mocks(game_mock, view_mock, send_to_ml, send_to_other)

        executor = GameExecutor(
            game,
            game_comm_manager,
            view,
            no_display=True
        )

        executor.run()

        with assert_same(func_calls_test.mock_calls) as expect_calls:
            expect_calls.send_to_other.send({'type': 'system_message', 'data': {'message': 'AI準備中'}})
            expect_calls.send_to_other.send({'type': 'game_info', 'data': {'scene': 'aaannn'}})
            expect_calls.send_to_other.send({'type': 'system_message', 'data': {'message': '遊戲啟動'}})

            # they somehow choose to send total frame instead of frame in a game to view
            total_frame = 1
            for game in range(2):
                for i in range(1, 7):
                    expect_calls.view_mock.is_paused()
                    expect_calls.send_to_ml.send(('game data', {'info': 'kb'}))
                    expect_calls.game_mock.update({'1P': 'AI_COMMAND'})
                    expect_calls.view_mock.draw({'draw_data': 'DRAW_DATA', 'frame': total_frame})
                    expect_calls.send_to_other.send({'type': 'game_progress', 'data': {'draw_data': 'DRAW_DATA', 'frame': total_frame}})
                    total_frame += 1
                expect_calls.send_to_ml.send(('game data', []))
                if game == 0:
                    expect_calls.game_mock.reset()

            # last game update return QUIT
            expect_calls.send_to_other.send({'type': 'system_message', 'data': {'message': '遊戲結束'}})
            expect_calls.send_to_other.send({'type': 'game_result', 'data': {'attachment': [1, 2]}})
            expect_calls.send_to_other.send({'type': 'system_message', 'data': {'message': '關閉遊戲'}})
            expect_calls.send_to_other.send(None)

