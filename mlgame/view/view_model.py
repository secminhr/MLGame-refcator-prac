import abc
import random


class View(abc.ABC):
    @abc.abstractmethod
    def to_data(self):
        pass


class Scene(View):
    def __init__(self, width: int, height: int, color: str = "#000000", bias_x=0, bias_y=0):
        """
        This is a value object
        :param width:
        :param height:
        :param color:
        """
        self.width = width
        self.height = height
        self.color = color
        self.bias_x = bias_x
        self.bias_y = bias_y

    def to_data(self):
        return {
            "width": self.width,
            "height": self.height,
            "color": self.color,
            "bias_x": self.bias_x,
            "bias_y": self.bias_y
        }


class Asset(View):
    def __init__(self, image_id: str, width: int, height: int, file_path: str, github_raw_url: str):
        self.image_id = image_id
        self.width = width
        self.height = height
        self.file_path = file_path
        self.github_raw_url = github_raw_url

    def to_data(self):
        return {
            "type": "image",
            "image_id": self.image_id,
            "width": self.width,
            "height": self.height,
            "file_path": self.file_path,
            "url": self.github_raw_url
        }


class Image(View):
    """
    這是一個用來繪製圖片的資料格式，
    "type"表示不同的類型
    "x" "y" 表示物體左上角的座標
    "width" "height"表示其大小
    "image_id"表示其圖片的識別號，需在
    "angle"表示其順時針旋轉的角度
    """
    def __init__(self, image_id: str, x: int, y: int, width: int, height: int, angle: int = 0):
        self.image_id = image_id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle

    def to_data(self):
        return {
            "type": "image",
            "image_id": self.image_id,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "angle": self.angle
        }


class Rect(View):
    """
    這是一個用來繪製矩形的資料格式，
    "type"表示不同的類型
    "name"用來描述這個物件
    "x""y"表示其位置，位置表示物體左上角的座標
    "size"表示其大小
    "image"表示其圖片
    "angle"表示其順時針旋轉的角度
    "color"以字串表示
    :return:
    """
    def __init__(self, name: str, x: int, y: int, width: int, height: int, color: str, angle: int = 0):
        # TODO angle
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.angle = angle

    def to_data(self):
        return {
            "type": "rect",
            "name": self.name,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "color": self.color,
            "angle": self.angle
        }


class Line(View):
    """
    這是一個用來繪製直線的資料格式，
    "x1","y1"表示起點位置，位置表示物體左上角的座標
    "x2","y2"表示終點位置，位置表示物體左上角的座標
    "color"以字串表示
    "width" 表示寬度
    :return:
    """
    def __init__(self, name: str, x1: int, y1: int, x2: int, y2: int, color: str, width: int = 2):
        self.name = name
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.width = width

    def to_data(self):
        return {
            "type": "line",
            "name": self.name,
            "x1": self.x1,
            "y1": self.y1,
            "x2": self.x2,
            "y2": self.y2,
            "width": self.width,
            "color": self.color
        }


class Polygon(View):
    """
    這是一個用來繪製多邊形的資料格式，
    points欄位至少三個 # [[100,101],[52.1,31.3],[53.1,12.3]]
    :return:dict
    """
    def __init__(self, name: str, points: list, color: str):
        assert len(points) >= 3
        self.name = name
        self.points = points
        self.color = color

    def to_data(self):
        return {
            "type": "polygon",
            "name": self.name,
            "color": self.color,
            "points": list(map(lambda p: {"x": p[0], "y": p[1]}, self.points))
        }


class AAPolygon(View):
    """
    這是一個用來繪製多邊形的資料格式，
    points欄位至少三個 # [[100,101],[52.1,31.3],[53.1,12.3]]
    :return:dict
    """
    def __init__(self, name: str, points: list, color: str):
        assert len(points) >= 3
        self.name = name
        self.points = points
        self.color = color

    def to_data(self):
        return {
            "type": "aapolygon",
            "name": self.name,
            "color": self.color,
            "points": list(map(lambda p: {"x": p[0], "y": p[1]}, self.points))
        }


class Text(View):
    """
    這是一個用來繪製文字的資料格式，
    "content"表示文字內容
    "x","y"表示其位置，位置表示物體左上角的座標
    "color"以字串表示
    "font-style"表示字體樣式
    :return:
    """
    def __init__(self, content: str, x: int, y: int, color: str, font_style="24px Arial"):
        self.content = content
        self.x = x
        self.y = y
        self.color = color
        self.font_style = font_style

    def to_data(self):
        return {
            "type": "text",
            "content": self.content,
            "color": self.color,
            "x": self.x,
            "y": self.y,
            "font-style": self.font_style
        }

def create_asset_init_data(image_id: str, width: int, height: int, file_path: str, github_raw_url: str):
    # assert file_path is valid
    return Asset(image_id, width, height, file_path, github_raw_url).to_data()

def create_scene_view_data(width: int, height: int, color: str = "#000000", bias_x=0, bias_y=0):
    return Scene(width, height, color, bias_x, bias_y).to_data()


def create_scene_progress_data(frame: int = 0, background=None, object_list=None,
                               toggle=None, toggle_with_bias=None, foreground=None, user_info=None,
                               game_sys_info=None):
    if background is None:
        background = []
    if object_list is None:
        object_list = []
    if toggle is None:
        toggle = []
    if toggle_with_bias is None:
        toggle_with_bias = []
    if foreground is None:
        foreground = []
    if user_info is None:
        user_info = []
    if game_sys_info is None:
        game_sys_info = {}
    return {
        # background view data will be draw first
        "frame": frame,
        "background": background,
        # game object view data will be draw on screen by order , and it could be shifted by WASD
        "object_list": object_list,
        "toggle_with_bias": toggle_with_bias,
        "toggle": toggle,
        "foreground": foreground,
        # other information to display on web
        "user_info": user_info,
        # other information to display on web
        "game_sys_info": game_sys_info
    }


def create_image_view_data(image_id, x, y, width, height, angle=0):
    return Image(image_id, x, y, width, height, angle).to_data()

def create_rect_view_data(name: str, x: int, y: int, width: int, height: int, color: str, angle: int = 0):
    return Rect(name, x, y, width, height, color, angle).to_data()


def create_line_view_data(name: str, x1: int, y1: int, x2: int, y2: int, color: str, width: int = 2):
    return Line(name, x1, y1, x2, y2, color, width).to_data()


def create_polygon_view_data(name: str, points: list, color: str):
    return Polygon(name, points, color).to_data()

def create_aapolygon_view_data(name: str, points: list, color: str):
    return AAPolygon(name, points, color).to_data()


def create_text_view_data(content: str, x: int, y: int, color: str, font_style="24px Arial"):
    return Text(content, x, y, color, font_style).to_data()


def get_scene_init_sample_data() -> dict:
    """
    :rtype: dict
    :return:  遊戲場景初始化的資料
    """

    scene = Scene(800, 600)
    assets = [
        {
            "type": "image",
            "image_id": 'car_01',
            "width": 50,
            "height": 50,
            "url": 'https://raw.githubusercontent.com/yen900611/Maze_Car/master/game_core/image/car_01.png'
        }, {
            "type": "image",
            "image_id": 'car_02',
            "width": 50,
            "height": 50,
            "url": 'https://raw.githubusercontent.com/yen900611/Maze_Car/master/game_core/image/car_02.png'
        }
    ]

    return {
        "scene": scene.__dict__,
        "assets": assets,
        # "audios": {}
    }


def get_dummy_progress_data():
    background = create_image_view_data("background", 0, 0, 800, 600)
    score_text = create_text_view_data("Score = 1", 650, 50, "#FF0000")
    rect = create_rect_view_data("dummy_rect", 200, 300, 100, 200, "#FFFAAA", 30)
    line = create_line_view_data("dummy_line", 10, 30, 100, 300, "#AAAFFF", 5)
    points = gen_points(5)
    polygon = create_polygon_view_data("dummy_polygon", points, "#FFAAFF")

    scene_progress = {
        # background view data will be draw first
        "frame":1,
        "background": [
            background,

        ],
        # game object view data will be draw on screen by order , and it could be shifted by WASD
        "object_list": [
            rect,
            line
        ],
        "toggle": [
            polygon
        ],
        "foreground": [
            score_text
        ],
        # other information to display on web
        "user_info": [],
        # other information to display on web
        "game_sys_info": {}
    }
    return scene_progress


def gen_points(point_num: int = 4) -> list:
    """
    points should be [x,y] ex [100.3,300.231]
    """
    result = []
    for i in range(point_num):
        result.append([random.randint(0, 100), random.randint(0, 100)])
    return result
