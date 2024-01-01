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

    def test_image_view(self):
        assert create_image_view_data("img_id", 10, 20, 1, 2, 90) == {
            "type": "image",
            "image_id": "img_id",
            "x": 10,
            "y": 20,
            "width": 1,
            "height": 2,
            "angle": 90
        }

    def test_image_view_default(self):
        assert create_image_view_data("img_id", 10, 20, 1, 2) == {
            "type": "image",
            "image_id": "img_id",
            "x": 10,
            "y": 20,
            "width": 1,
            "height": 2,
            "angle": 0
        }

    def test_rect_view(self):
        assert create_rect_view_data("rect_name", 10, 20, 1, 2, "#FFFFFF", 90) == {
            "type": "rect",
            "name": "rect_name",
            "x": 10,
            "y": 20,
            "width": 1,
            "height": 2,
            "color": "#FFFFFF",
            "angle":  90
        }

    def test_rect_view_default(self):
        assert create_rect_view_data("rect_name", 10, 20, 1, 2, "#FFFFFF") == {
            "type": "rect",
            "name": "rect_name",
            "x": 10,
            "y": 20,
            "width": 1,
            "height": 2,
            "color": "#FFFFFF",
            "angle": 0
        }

    def test_line_view(self):
        assert create_line_view_data("line_name", 10, 20, 1, 2, "#FFFFFF", 5) == {
            "type": "line",
            "name": "line_name",
            "x1": 10,
            "y1": 20,
            "x2": 1,
            "y2": 2,
            "color": "#FFFFFF",
            "width": 5
        }

    def test_line_view_default(self):
        assert create_line_view_data("line_name", 10, 20, 1, 2, "#FFFFFF") == {
            "type": "line",
            "name": "line_name",
            "x1": 10,
            "y1": 20,
            "x2": 1,
            "y2": 2,
            "color": "#FFFFFF",
            "width": 2
        }

    def test_polygon_view(self):
        assert create_polygon_view_data("polygon_name", [(10, 20), (1, 2), (3, 4)], "#FFFFFF") == {
            "type": "polygon",
            "name": "polygon_name",
            "points": [{"x": 10, "y": 20}, {"x": 1, "y": 2}, {"x": 3, "y": 4}],
            "color": "#FFFFFF"
        }

    def test_polygon_require_three_more_points(self):
        with pytest.raises(AssertionError):
            create_polygon_view_data("polygon_name", [(10, 20), (1, 2)], "#FFFFFF")

    def test_text_view(self):
        assert create_text_view_data("content", 10, 20, "#FFFFFF", "font") == {
            "type": "text",
            "content": "content",
            "x": 10,
            "y": 20,
            "color": "#FFFFFF",
            "font-style": "font"
        }

    def test_text_view_default(self):
        assert create_text_view_data("content", 10, 20, "#FFFFFF") == {
            "type": "text",
            "content": "content",
            "x": 10,
            "y": 20,
            "color": "#FFFFFF",
            "font-style": "24px Arial"
        }

