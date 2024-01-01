import abc
import math
import os.path
import time
from functools import lru_cache

import pygame

from mlgame.view.decorator import K_BACKGROUND, K_SCENE
from mlgame.view.view_model import SceneInfo, Text

KEYS = [
    pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_i,
    pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_m, pygame.K_n, pygame.K_o, pygame.K_p, pygame.K_q, pygame.K_r,
    pygame.K_s, pygame.K_t, pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x, pygame.K_y, pygame.K_z,
    pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
    pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0,
    pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
]

LINE = "line"
TEXT = "text"
NAME = "name"
TYPE = "type"
ANGLE = "angle"
SIZE = "size"
COLOR = "color"
IMAGE = "image"
RECTANGLE = "rect"
POLYGON = "polygon"
AAPOLYGON = "aapolygon"


@lru_cache
def transfer_hex_to_rgb(hex_str: str) -> tuple:
    h = hex_str.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


@lru_cache
def transfer_hex_to_rgba(hex_str: str) -> tuple:
    temp_str = str(hex_str)
    if len(hex_str) == 7:
        temp_str += "FF"
    h = temp_str.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4, 6))


@lru_cache
def scale_bias_of_coordinate(obj_length, scale):
    return obj_length / 2 * (1 - scale)


@lru_cache
def rotate_img(scaled_img, radian_angle):
    return pygame.transform.rotate(
        scaled_img,
        (radian_angle * 180 / math.pi) % 360
    )


@lru_cache
def scale_img(img, origin_width, origin_height, scale_ratio):
    return pygame.transform.scale(
        img, (int(origin_width * scale_ratio), int(origin_height * scale_ratio))
    )


class PygameViewInterface(abc.ABC):
    def __init__(self, game_info: dict):
        pass

    @abc.abstractmethod
    def reset(self):
        pass

    @abc.abstractmethod
    def draw(self, object_information):
        pass

    @abc.abstractmethod
    def get_keyboard_info(self) -> list:
        return []

    @abc.abstractmethod
    def save_image(self, img_path: os.path.abspath):
        pass

    def is_paused(self):
        return False


class DummyPygameView(PygameViewInterface):
    def __init__(self, game_info: dict):
        super().__init__(game_info)

    def reset(self):
        pass

    def draw(self, object_information):
        pass

    def save_image(self, img_path: os.path.abspath):
        pass

    def get_keyboard_info(self) -> list:
        return []


class PygameView(PygameViewInterface):
    def __init__(self, game_info: dict):
        super().__init__(game_info)
        self._pause_state = False
        self._last_pause_btn_clicked_time = 0
        pygame.display.init()
        pygame.font.init()
        self.scene_init_data = game_info
        self.background_color = transfer_hex_to_rgb(self.scene_init_data[K_SCENE][COLOR])
        self.address = "GameView"
        self._fixed_backgound_objs = self.scene_init_data.get(K_BACKGROUND, [])

        width = self.scene_init_data[K_SCENE]["width"]
        height = self.scene_init_data[K_SCENE]["height"]
        screen = pygame.display.set_mode(
            (width, height),
            flags=pygame.RESIZABLE | pygame.SCALED)
        self.scene_info = SceneInfo(screen, self.loading_image(), {}, width, height)
        # self.map_width = game_info["map_width"]
        # self.map_height = game_info["map_height"]
        self.origin_bias_point = [self.scene_init_data[K_SCENE]["bias_x"], self.scene_init_data[K_SCENE]["bias_y"]]
        self.bias_point_var = [0, 0]
        self.bias_point = self.origin_bias_point.copy()

        self.scale = 1
        # if "images" in game_info.keys():
        #     self.image_dict = self.loading_image(game_info["images"])
        self._toggle_on = True
        self._toggle_last_time = 0

    def reset(self):
        self.bias_point_var = [0, 0]
        self.bias_point = self.origin_bias_point.copy()

        self.scale = 1
        self._toggle_on = True
        self._toggle_last_time = 0

    def loading_image(self):
        result = {}
        if "assets" in self.scene_init_data:
            for file in self.scene_init_data["assets"]:
                # print(file)
                if file[TYPE] == IMAGE:
                    image = pygame.image.load(file["file_path"]).convert_alpha()
                    result[file["image_id"]] = image
        return result

    def draw(self, object_information):
        self.scene_info.display.fill(self.background_color)
        self.adjust_pygame_screen()

        if "view_center_coordinate" in object_information["game_sys_info"]:
            self.origin_bias_point = [
                object_information["game_sys_info"]["view_center_coordinate"][0],
                object_information["game_sys_info"]["view_center_coordinate"][1]
            ]
            self.bias_point[0] = self.origin_bias_point[0] + self.bias_point_var[0]
            self.bias_point[1] = self.origin_bias_point[1] + self.bias_point_var[1]

        # in draw()
        for game_object in self._fixed_backgound_objs:
            game_object.draw(
                self.scene_info,
                self.bias_point[0], self.bias_point[1], self.scale
            )
        try:
            for game_object in object_information["background"]:
                game_object.draw(
                    self.scene_info,
                    self.bias_point[0], self.bias_point[1], self.scale
                )
            for game_object in object_information["object_list"]:
                # let object could be shifted
                game_object.draw(
                    self.scene_info,
                    self.bias_point[0], self.bias_point[1], self.scale
                )
            if self._toggle_on:
                for game_object in object_information["toggle_with_bias"]:
                    # let object could be shifted
                    game_object.draw(
                        self.scene_info,
                        self.bias_point[0], self.bias_point[1], self.scale
                    )
                for game_object in object_information["toggle"]:
                    game_object.draw(self.scene_info)
            for game_object in object_information["foreground"]:
                # object should not be shifted
                game_object.draw(self.scene_info)
        except Text.FontNotFoundError as e:
            font_style_list = e.font_style.split(" ", -1)
            size = int(font_style_list[0].replace("px", "", 1))
            font_type = font_style_list[1].lower()
            if "BOLD" in font_style_list:
                font = pygame.font.Font(pygame.font.match_font(font_type, bold=True), size * self.scale)
            else:
                font = pygame.font.Font(pygame.font.match_font(font_type), size * self.scale)
            self.scene_info.fonts[e.font_style] = font

            # retry
            self.draw(object_information)
        pygame.display.flip()

    def save_image(self, img_path: os.path.abspath):
        pygame.image.save(self.scene_info.display, img_path)
        pass

    def adjust_pygame_screen(self):
        """
        zoom in zoom out and shift the window.
        """
        key_state = pygame.key.get_pressed()
        # 上下左右 放大縮小
        if key_state[pygame.K_i]:
            self.bias_point_var[1] += 10
            self.bias_point[1] = self.origin_bias_point[1] + self.bias_point_var[1]
        elif key_state[pygame.K_k]:
            self.bias_point_var[1] -= 10
            self.bias_point[1] = self.origin_bias_point[1] + self.bias_point_var[1]
        elif key_state[pygame.K_j]:
            self.bias_point_var[0] += 10
            self.bias_point[0] = self.origin_bias_point[0] + self.bias_point_var[0]
        elif key_state[pygame.K_l]:
            self.bias_point_var[0] -= 10
            self.bias_point[0] = self.origin_bias_point[0] + self.bias_point_var[0]

        if key_state[pygame.K_o]:
            self.scale += 0.01
        elif key_state[pygame.K_u]:
            self.scale -= 0.01
            if self.scale < 0.05:
                self.scale = 0.05
        # 隱藏鍵
        if key_state[pygame.K_h] and (time.time() - self._toggle_last_time) > 0.3:
            self._toggle_on = not self._toggle_on
            self._toggle_last_time = time.time()

    def get_keyboard_info(self) -> list:
        keyboard_info = []
        pressed_keys = pygame.key.get_pressed()
        if True in pressed_keys:
            for k in KEYS:
                if pressed_keys[k]:
                    keyboard_info.append(k)
        return keyboard_info

    def is_paused(self) -> bool:
        # 隱藏鍵
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_p] and (time.time() - self._last_pause_btn_clicked_time) > 0.3:
            self._pause_state = not self._pause_state
            self._last_pause_btn_clicked_time = time.time()
        return self._pause_state
