import pytest

from mlgame.view.view_model import *


class TestViewModel:
    def test_asset_init(self):
        assert create_asset_init_data("img_id", 10, 10, "file_path", "github_url") == {
            "type": "image",
            "image_id": "img_id",
            "width": 10,
            "height": 10,
            "file_path": "file_path",
            "url": "github_url"
        }

    def test_scene_view(self):
        assert create_scene_view_data(10, 10, "#FFFFFF", 1, 2) == {
            "width": 10,
            "height": 10,
            "color": "#FFFFFF",
            "bias_x": 1,
            "bias_y": 2
        }

    def test_scene_view_default(self):
        assert create_scene_view_data(10, 10) == {
            "width": 10,
            "height": 10,
            "color": "#000000",
            "bias_x": 0,
            "bias_y": 0
        }

    def test_scene_progress(self):
        assert create_scene_progress_data(
            10, ['bg'], ['objects'], ['toggle'], ['toggle_bias'], ['fg'], ['user'], {'game': 'sys info'}
        ) == {
            "frame": 10,
            "background": ['bg'],
            "object_list": ['objects'],
            "toggle": ['toggle'],
            "toggle_with_bias": ['toggle_bias'],
            "foreground": ['fg'],
            "user_info": ['user'],
            "game_sys_info": {'game': 'sys info'}
        }

    def test_scene_progress_default(self):
        assert create_scene_progress_data() == {
            "frame": 0,
            "background": [],
            "object_list": [],
            "toggle": [],
            "toggle_with_bias": [],
            "foreground": [],
            "user_info": [],
            "game_sys_info": {}
        }

