import json
import os
import shutil
import sys

import my_codecs


class ResolutionFixer:
    @staticmethod
    def pad():
        return "pad=width=ceil(iw/2)*2:height=ceil(ih/2)*2"

    @staticmethod
    def crop():
        return "crop=trunc(iw/2)*2:trunc(ih/2)*2"

    @staticmethod
    def validate_resolution(width: int, height: int, even: bool = True) -> bool:
        if even:
            return width % 2 == 0 and height % 2 == 0
        return True

    @staticmethod
    def parse_resolution(res_str: str) -> tuple[int, int] | None:
        """
        Разбирает строку разрешения вида "WxH" или "-1:H" / "W:-1".
        Возвращает (width, height) как числа или None, если не удалось.
        """
        if not res_str:
            return None
        try:
            w_str, h_str = res_str.split(":")
            width = int(w_str) if w_str != "-1" else -1
            height = int(h_str) if h_str != "-1" else -1
            return width, height
        except (ValueError, AttributeError):
            return None


script_dir = os.path.dirname(__file__)
options_path = os.path.join(script_dir, "options.json")
defaults_path = os.path.join(script_dir, "defaults.json")


def load_options(codec_name: str) -> dict:
    if not os.path.exists(options_path):
        create_options_json()

    with open(options_path, "r", encoding="utf-8") as f:
        all_defaults = json.load(f)

    return all_defaults.get(codec_name, {})


def create_options_json():
    if not os.path.exists(defaults_path):
        raise FileNotFoundError(f"{defaults_path} not found")
    shutil.copyfile(defaults_path, options_path)


def create_defaults_json_if_missing():
    """
    Создаёт defaults.json с базовыми значениями кодеков,
    если файл не найден в корне проекта.
    """

    if os.path.exists(defaults_path):
        return  # Файл уже есть, ничего не делаем

    defaults = {
        "vp9": {
            "crf": 35,
            "scale": "don't change",
            "preset": "good",
            "fps": "don't change",
            "pixel_format": "yuv420p",
            "passes": "Two-Pass",
            "container": "webm",
            "audio bitrate": 128
        },
        "svt-av1": {
            "crf": 28,
            "scale": "don't change",
            "preset": "8",
            "fps": "don't change",
            "pixel_format": "yuv420p",
            "passes": "Two-Pass",
            "container": "mkv",
            "audio bitrate": 128
        },
        "hevc": {
            "crf": 23,
            "scale": "don't change",
            "preset": "medium",
            "fps": "don't change",
            "pixel_format": "yuv420p",
            "passes": "Two-Pass",
            "container": "mp4",
            "audio bitrate": 128
        }
    }

    with open(defaults_path, "w", encoding="utf-8") as f:
        json.dump(defaults, f, indent=4)
    print(f"Created defaults.json at {defaults_path}")


def supported_codecs() -> list:
    """
    Возвращает список объектов Codec, доступных в my_codecs.
    """
    return [
        obj for name, obj in vars(my_codecs).items()
        if isinstance(obj, my_codecs.Codec)
    ]


def set_terminal_title(title: str):
    if os.name == "nt":  # Windows
        os.system(f"title {title}")
    else:  # Linux / macOS
        sys.stdout.write(f"\033]0;{title}\007")
        sys.stdout.flush()
