class ResolutionFixer:
    @staticmethod
    def pad():
        return "pad=width=ceil(iw/2)*2:height=ceil(ih/2)*2"

    @staticmethod
    def crop():
        return "scale=trunc(iw/2)*2:trunc(ih/2)*2"

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

import json
import os

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
