import json
import os


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


def load_defaults(codec_name: str) -> dict:
    """
    Загружает стандартные значения для указанного кодека из defaults.json.
    """
    script_dir = os.path.dirname(__file__)
    json_path = os.path.join(script_dir, "defaults.json")
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"{json_path} not found")

    with open(json_path, "r", encoding="utf-8") as f:
        all_defaults = json.load(f)

    return all_defaults.get(codec_name, {})


def create_defaults_json_if_missing():
    """
    Создаёт defaults.json с базовыми значениями кодеков,
    если файл не найден в корне проекта.
    """
    script_dir = os.path.dirname(__file__)
    json_path = os.path.join(script_dir, "defaults.json")

    if os.path.exists(json_path):
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

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(defaults, f, indent=4)
    print(f"Created defaults.json at {json_path}")


import my_codecs

def supported_codecs() -> list:
    """
    Возвращает список объектов Codec, доступных в my_codecs.
    """
    return [
        obj for name, obj in vars(my_codecs).items()
        if isinstance(obj, my_codecs.Codec)
    ]